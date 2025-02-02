package entities.paths;

import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;

import algorithms.paths.DP_Anyk_Iterator;
import algorithms.paths.DP_Recursive;
import entities.Join_Predicate;
import entities.Relation;
import entities.State_Node;
import entities.Tuple;
import factorization.Binary_Partitioning;
import factorization.Equality;
import factorization.Multiway_Partitioning;
import factorization.Node_Connector;
import factorization.Shared_Ranges;
import util.Common;

/**
 * A class for DP problems that are theta-join path queries.
 * The goal of DP is to find the minimum total weight of a query result.
 * The joining pairs of tuples between two consecutive relations are encoded
 * (factorized)
 * via the methods of @link{}.
 * The DP states may correspond to tuples or may be artifical ones that do not
 * contain any information.
 * In the first case, it is safe to downcast
 * {@link entities.paths.DP_State_Node#state_info} to {@link entities.Tuple}.
 * 
 * @author anonymous anonymous
 */
public class DP_Path_ThetaJoin_Instance extends DP_Problem_Instance {
    /**
     * The query that creates the DP problem.
     */
    Path_ThetaJoin_Query path_query;

    /**
     * For each tuple, we create a DP state.
     * Additional states may be created to make the state space more efficient while
     * preserving the same solutions.
     * Every relation maps to a stage of DP.
     * The starting node is artificial and the terminal node is implicit.
     * The cost of transitioning to a tuple is the cost of that tuple.
     * 
     * @param query  A theta-join query.
     * @param method Sets a particular method for the factorization of the join. If
     *               null, method selection is automatic.
     */
    public DP_Path_ThetaJoin_Instance(Path_ThetaJoin_Query query, String method) {
        super();
        this.path_query = query;
        Node_Connector.problem_setting = "DP";

        DP_State_Node new_node;
        Tuple right_tuple;
        ArrayList<DP_State_Node> new_stage, prev_stage;
        Relation relation;
        int relation_index;
        int l = path_query.length;

        // The tuples of the last relation in the path correspond
        // to states that all reach the terminal node with zero cost
        relation = path_query.relations.get(l - 1);
        new_stage = new ArrayList<DP_State_Node>(relation.tuples.size());
        for (Tuple t : relation.tuples) {
            new_node = new DP_State_Node(t);
            new_node.set_to_terminal();
            new_stage.add(new_node);
        }

        // For all the other relations, insert a stage to the left
        // To construct the paths that encode the solutions between the new stage and
        // the previous one,
        // we resort to the methods in @link{factorization}.
        for (int sg = l - 1; sg >= 1; sg--) {
            relation_index = sg - 1; // because indexing of path_query.relations starts with 0

            relation = path_query.relations.get(relation_index);
            prev_stage = new_stage;
            new_stage = new ArrayList<DP_State_Node>(relation.tuples.size());
            // Materialize a node for each tuple
            for (Tuple t : relation.tuples) {
                new_node = new DP_State_Node(t);
                new_stage.add(new_node);
            }

            List<List<Join_Predicate>> join_condition = path_query.join_conditions.get(relation_index);
            // Handle equi-join without intermediate nodes
            if (Common.is_conjunction_of_simple_equalities(join_condition)) {
                // Convert predicates to lists of indexes of the attributes in the schema
                int[] join_attributes_new = join_condition.get(0).stream().mapToInt(p -> p.attr_idx_1).toArray();
                int[] join_attributes_prev = join_condition.get(0).stream().mapToInt(p -> p.attr_idx_2).toArray();

                // Hash the nodes of the prev stage and the new stage so that they are grouped
                // by the join attribute values
                HashMap<List<Double>, List<State_Node>> prev_hash = Common.hash_stage(prev_stage,
                        join_attributes_prev);
                HashMap<List<Double>, List<State_Node>> new_hash = Common.hash_stage(new_stage,
                        join_attributes_new);

                // For each bucket in prev
                for (Map.Entry<List<Double>, List<State_Node>> map_entry : prev_hash.entrySet()) {
                    List<Double> join_values = map_entry.getKey();
                    List<State_Node> prev_nodes = map_entry.getValue();

                    // Look up bucket in new
                    List<State_Node> matching_nodes_new = new_hash.get(join_values);
                    if (matching_nodes_new != null) {
                        int j = 0;
                        for (State_Node matching_node_new : matching_nodes_new) {
                            DP_State_Node matching_node_new_dp = (DP_State_Node) matching_node_new;
                            if (j == 0) {
                                for (State_Node prev_node : prev_nodes) {
                                    DP_State_Node prev_node_dp = (DP_State_Node) prev_node;
                                    matching_node_new_dp.add_decision(prev_node_dp,
                                            ((Tuple) prev_node_dp.state_info).cost);
                                }
                            } else {
                                // Share the same decisions with the first node in the bucket of matching nodes
                                // in new stage
                                matching_node_new_dp.share_decisions(((DP_State_Node) matching_nodes_new.get(0)));
                            }
                            j += 1;
                        }
                    }
                }
            } else {

                // The join condition between the two relations is given in DNF form
                // To handle the disjunctions, construct a graph independently for each one
                for (List<Join_Predicate> conjunction : path_query.join_conditions.get(relation_index)) {
                    // Analyze the type of conjunction between the two relations to decide
                    // how the join will be handled
                    int ineq_cnt = 0, neq_cnt = 0, band_cnt = 0;
                    for (Join_Predicate p : conjunction) {
                        if (p.type.equals("E")) {
                            if (ineq_cnt != 0 || neq_cnt != 0 || band_cnt != 0) {
                                System.err.println("Equality conditions must precede others!");
                                System.exit(1);
                            }
                        } else if (p.type.equals("IL") || p.type.equals("IG"))
                            ineq_cnt += 1;
                        else if (p.type.equals("N"))
                            neq_cnt += 1;
                        else if (p.type.equals("B"))
                            band_cnt += 1;
                        else {
                            System.err.println("Join condition currently unsupported!");
                            System.exit(1);
                        }
                    }
                    // Encode the state-space of joining tuples between the relations efficiently
                    // according to the type of join conditions
                    if (ineq_cnt == 0 && neq_cnt == 0 && band_cnt == 0) {
                        // Only equalities here or no conditions at all which means cartesian product
                        // Use the equality class
                        Equality.factorize_equality(new_stage, prev_stage, conjunction);
                    } else if (method == null) {
                        if (ineq_cnt == 1 && neq_cnt == 0 && band_cnt == 0) {
                            // A single inequality condition and maybe some equalities
                            // Use the multi-way partitioning class for lower memory consumption
                            Multiway_Partitioning.factorize_inequality(new_stage, prev_stage, conjunction);
                        } else if (ineq_cnt == 0 && neq_cnt == 1 && band_cnt == 0) {
                            // A single non-equality condition and maybe some equalities
                            // Use the multi-way partitioning class for lower memory consumption
                            Multiway_Partitioning.factorize_nonequality(new_stage, prev_stage, conjunction);
                        } else if (ineq_cnt == 0 && neq_cnt == 0 && band_cnt == 1) {
                            // A single band condition and maybe some equalities
                            // Use the multi-way partitioning class for lower memory consumption
                            Multiway_Partitioning.factorize_band(new_stage, prev_stage, conjunction);
                        } else {
                            // A conjunction of inequalities, etc.
                            // Use the binary partitioning class
                            Binary_Partitioning.factorize_conjunction(new_stage, prev_stage, conjunction);
                        }
                    } else if (method.equals("binary_part")) {
                        Binary_Partitioning.factorize_conjunction(new_stage, prev_stage, conjunction);
                    } else if (method.equals("multi_part")) {
                        if (ineq_cnt == 1 && neq_cnt == 0 && band_cnt == 0) {
                            Multiway_Partitioning.factorize_inequality(new_stage, prev_stage, conjunction);
                        } else if (ineq_cnt == 0 && neq_cnt == 1 && band_cnt == 0) {
                            Multiway_Partitioning.factorize_nonequality(new_stage, prev_stage, conjunction);
                        } else if (ineq_cnt == 0 && neq_cnt == 0 && band_cnt == 1) {
                            Multiway_Partitioning.factorize_band(new_stage, prev_stage, conjunction);
                        } else {
                            System.err.println(
                                    "Multiway Partitioning is currently supported only for a single ineq/non-eq/band predicate");
                            System.exit(1);
                        }
                    } else if (method.equals("shared_ranges")) {
                        if (ineq_cnt == 1 && neq_cnt == 0 && band_cnt == 0) {
                            // A single inequality condition and maybe some equalities
                            Shared_Ranges.factorize_inequality(new_stage, prev_stage, conjunction);
                            set_bottom_up_implementation("iterative");
                        } else {
                            System.err
                                    .println(
                                            "Shared ranges is currently supported only for a single inequality predicate");
                            System.exit(1);
                        }
                    } else {
                        System.err.println("Unrecognized method");
                        System.exit(1);
                    }
                }
            }

            // Print new relation sizes
            /*
             * if (method != null && method.equals("binary_part"))
             * {
             * System.out.println("Initial Relation Size = " + new_stage.size());
             * 
             * int fact_rel_1_size = 0;
             * for (DP_State_Node left_node : new_stage) fact_rel_1_size +=
             * left_node.get_number_of_children();
             * System.out.println("New Relation 1 Size = " + fact_rel_1_size);
             * 
             * int fact_rel_2_size = 0;
             * HashSet<DP_State_Node> fact_rel_1_nodes = new HashSet<DP_State_Node>();
             * for (DP_State_Node left_node : new_stage)
             * fact_rel_1_nodes.addAll(left_node.get_children());
             * for (DP_State_Node fact_rel_1_node : fact_rel_1_nodes) fact_rel_2_size +=
             * fact_rel_1_node.get_number_of_children();
             * System.out.println("New Relation 2 Size = " + fact_rel_2_size);
             * }
             */

            // Remove dangling nodes
            new_stage.removeIf(node -> node.get_number_of_children() == 0);
        }

        // Finally, instantiate the starting node and connect it to all the states of
        // stage 1
        // except those that do not have any children.
        // (We don't want to create dead-ends)
        // The starting node has no local information (null)
        starting_node = new DP_State_Node(null);
        prev_stage = new_stage;
        for (DP_State_Node right_node : prev_stage) {
            if (right_node.get_number_of_children() > 0 || right_node.is_terminal()) {
                right_tuple = ((Tuple) right_node.state_info); // cast so that we can lookup the cost
                starting_node.add_decision(right_node, right_tuple.cost);
            }
        }
    }

    public static void main(String args[]) {
        // Run an example with inequalities and equalities
        // Path_ThetaJoin_Query example_query = new Path_ThetaJoin_Query(1);
        // Run a example with a binary inequality
        Path_ThetaJoin_Query example_query = new Path_ThetaJoin_Query(2);
        // Run a example with a band
        // Path_ThetaJoin_Query example_query = new Path_ThetaJoin_Query(3);
        DP_Path_ThetaJoin_Instance instance = new DP_Path_ThetaJoin_Instance(example_query, "shared_ranges");
        // Transfrom to quadratic equi-join
        // Path_Equijoin_Query equijoin = example_query.to_Quadratic_Equijoin();
        // DP_Path_Equijoin_Instance instance = new DP_Path_Equijoin_Instance(equijoin);

        instance.bottom_up();
        // Print the cost of the optimal solution
        System.out.println("Optimal cost = " + instance.starting_node.get_opt_cost());

        // Print the optimal solution
        System.out.print("Optimal solution:");
        DP_State_Node curr = instance.starting_node.get_best_child();
        while (true) {
            System.out.print(" " + curr);
            if (curr.get_best_decision() == null)
                break;
            curr = curr.get_best_child();

        }
        System.out.println("");

        // Print the whole graph
        instance.print_edges();

        // Ranked enumeration
        DP_Anyk_Iterator iter = new DP_Recursive(instance, null);
        // DP_Anyk_Iterator iter = new DP_Lazy(instance, null);
        DP_Solution sol;
        while (true) {
            sol = iter.get_next();
            if (sol != null)
                System.out.println(sol + " " + sol.cost);
            else
                break;
        }

        System.out.println("No_of_solutions: " + instance.count_solutions());
        System.out.println("Graph size = " + instance.graph_size());
    }
}
