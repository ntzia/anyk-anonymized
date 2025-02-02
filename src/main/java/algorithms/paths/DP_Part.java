package algorithms.paths;

import java.util.ArrayList;
import java.util.Collection;
import java.util.List;
import java.util.PriorityQueue;
import java.util.Stack;

import org.jheaps.dag.HollowHeap;
import org.jheaps.tree.FibonacciHeap;
import org.jheaps.tree.PairingHeap;

import algorithms.Configuration;
import entities.paths.DP_Decision;
import entities.paths.DP_DecisionSet;
import entities.paths.DP_Prefix_Solution;
import entities.paths.DP_Problem_Instance;
import entities.paths.DP_Solution;
import entities.paths.DP_State_Node;
import util.CompileTimeConfig;
/** 
 * Implementation of Anyk-Part for DP, a ranked enumeration algorithm that relies on the Lawler procedure.
 * The different variants are implemented as subclasses, each one implementing the abstract methods differently.<br>
 * Brief description of the algorithm: 
 * A global PQ holds candidate solutions that are incomplete (prefixes)
 * but their future cost can be computed in constant time after the DP bottom-up phase.
 * In each iteration a prefix is popped, expanded and returned as the top-k'th solution.
 * To get the top-(k+1)'th solution, 
 * we generate new candidates from the last returned solution by taking its successors at each stage.
 * The successors are computed according to a partial order on the decisions available at each state.
 * Each variant has a different way of computing a partial order among the available decisions.
 * This partial order is the one that specifies the successors.
 * The variants are concrete subclasses of this abstract class and share the core method {@link #get_next}.
 * @see <a href="https://doi.org/10.1287/mnsc.18.7.401">Lawler procedure</a>
 * @author anonymous anonymous
*/
public abstract class DP_Part extends DP_Anyk_Iterator
{
	/** 
	 * Maintains all the prefix solutions that are candidates for the next best solution.
	*/
	protected PriorityQueue<DP_Prefix_Solution> global_pq_binary_heap;
	protected FibonacciHeap<DP_Prefix_Solution,Object> global_pq_fibonacci_heap;
	protected PairingHeap<DP_Prefix_Solution,Object> global_pq_pairing_heap;
	protected HollowHeap<DP_Prefix_Solution,Object> global_pq_hollow_heap;

	/** 
	 * Stores the solution returned in the previous call of {@link #get_next}.
	 * This is required because candidates generated from the top-k'th solution 
	 * are found and inserted into the PQ in the (k+1)'th call.
	*/
	protected DP_Prefix_Solution latest_solution;
	/** 
	 * The stage in which {@link #latest_solution} made a sidetrack (by going to a successor).
	 * It is the same as the length of the prefix that we popped in the previous call of {@link #get_next},
	 * that was then expanded to {@link #latest_solution}.
	 * By convention, latest_sidetrack_stage of the top-1 solution is 1.
	*/	
	protected int latest_sidetrack_stage;

	/** 
	 * @param inst The DP problem to run any-k on.
	 * @param conf A configuration of execution parameters.
	*/		
	public DP_Part(DP_Problem_Instance inst, Configuration conf)
    {
    	super(inst, conf);
    	this.latest_solution = null;
		this.latest_sidetrack_stage = -1;
		
    	// Initialize the global PQ with an empty prefix (that contains only the starting node)
		// this.global_pq = new Priority_Queue<DP_Prefix_Solution>(this.heap_type);
		// Just use a simple binary heap
		if (CompileTimeConfig.heap_type == "binary_heap")
			this.global_pq_binary_heap = new PriorityQueue<DP_Prefix_Solution>();
		else if (CompileTimeConfig.heap_type == "fibonacci_heap")
			this.global_pq_fibonacci_heap = new FibonacciHeap<DP_Prefix_Solution,Object>();
		else if (CompileTimeConfig.heap_type == "pairing_heap")
			this.global_pq_pairing_heap = new PairingHeap<DP_Prefix_Solution,Object>();
		else if (CompileTimeConfig.heap_type == "hollow_heap")
			this.global_pq_hollow_heap = new HollowHeap<DP_Prefix_Solution,Object>();
		// The prefix we start with contains only the best decision to go from starting_node to stage 1
    	// That way, we guarantee that for top-2 we start taking successor solutions from stage 1
    	if (instance.starting_node.get_opt_cost() != Double.POSITIVE_INFINITY)	// Corner case: if no path can reach the terminal node, leave the pq empty
    	{
	    	DP_Prefix_Solution starting_prefix = new DP_Prefix_Solution(instance.starting_node.get_best_decision());
	    	if (CompileTimeConfig.heap_type == "binary_heap")
				this.global_pq_binary_heap.add(starting_prefix);    	
			else if (CompileTimeConfig.heap_type == "fibonacci_heap")
				this.global_pq_fibonacci_heap.insert(starting_prefix);
			else if (CompileTimeConfig.heap_type == "pairing_heap")
				this.global_pq_pairing_heap.insert(starting_prefix);
			else if (CompileTimeConfig.heap_type == "hollow_heap")
				this.global_pq_hollow_heap.insert(starting_prefix);
		}

		// By default, initialize the data structures needed lazily
		// (i.e., the first time they are accesed)
		if ((conf != null) && !conf.initialization_laziness)
			initialize_data_structures();
    }

    public DP_Solution get_next()
    {
    	DP_Prefix_Solution curr, new_candidate, popped_solution, expanded_solution;
    	Collection<DP_Prefix_Solution> new_candidates = new ArrayList<DP_Prefix_Solution>();

    	// If no latest_solution has been stored, then this is the first call to this method
    	// In that case, the PQ contains only one prefix solution (the empty one) 
    	// which when expanded will give the top-1 solution.  
    	// In all other cases, we first need to generate successor solutions.  	
    	if (latest_solution != null)
    	{
    		// We have to generate successor solutions for all stages which are between 
    		// the last stage and the stage where the latest solution made its final sidetrack (indicated by its length)
			curr = latest_solution;
			int last_stage = curr.length;
			for (int sg = last_stage; sg >= latest_sidetrack_stage; sg--)
    		{
				//System.out.println("Taking successors of decisions between " + (sg - 1) + " and " + sg);
    			// In stage sg, we take the successors of decisions between sg-1 and sg.
    			// Consider the successors of the latest decision and generate one solution for each one.
    			for (DP_Decision succ : get_successors(curr.get_latest_decision()))
    			{
    				new_candidate = curr.create_successor(succ);
					new_candidates.add(new_candidate);
					//System.out.println("New Candidate: " + new_candidate);
				}
    			// Shorten the current solution by cutting off one decision
    			curr = curr.get_shorter();
			}
			// If the PQ is empty heapify instead of pushing
			// Especially helpful in the second iteration of DP_Min
			if (CompileTimeConfig.heap_type == "binary_heap" && global_pq_binary_heap.isEmpty())
                global_pq_binary_heap = new PriorityQueue<DP_Prefix_Solution>(new_candidates);
            else
                // global_pq.bulk_push(new_candidates);
				add_candidates(new_candidates);
    	}

    	// Pop the best solution from the global PQ
		// If the PQ is empty, then we have enumerated all solutions
		if (CompileTimeConfig.heap_type == "binary_heap")
		{
			if (global_pq_binary_heap.isEmpty()) return null;
			popped_solution = global_pq_binary_heap.poll();
		}
		else if (CompileTimeConfig.heap_type == "fibonacci_heap")
		{
			if (global_pq_fibonacci_heap.isEmpty()) return null;
			popped_solution = global_pq_fibonacci_heap.deleteMin().getKey();
		}
		else if (CompileTimeConfig.heap_type == "pairing_heap")
		{
			if (global_pq_pairing_heap.isEmpty()) return null;
			popped_solution = global_pq_pairing_heap.deleteMin().getKey();
		}
		else if (CompileTimeConfig.heap_type == "hollow_heap")
		{
			if (global_pq_hollow_heap.isEmpty()) return null;
			popped_solution = global_pq_hollow_heap.deleteMin().getKey();
		}
		// Record its length so that we know from which stage onwards 
		// we have to generate successor solutions in the next call
		latest_sidetrack_stage = popped_solution.length;
		// Expand the prefix solution to a full solution
		expanded_solution = expand(popped_solution);
		// Record it so that we consider its successor solutions in the next call
		latest_solution = expanded_solution;

		return expanded_solution;
	}

    
	/** 
	 * Expands the prefix solution into a full solution by following an optimal sequence of decisions.
	 * The full solution reaches a terminal node.
	 * @param pref A prefix solution to be expanded optimally.
	 * @return DP_Prefix_Solution A new object that is a full solution.
	 */
    protected DP_Prefix_Solution expand(DP_Prefix_Solution pref)
    {
    	DP_Prefix_Solution current;
    	DP_Decision next_best_decision;
    	current = pref;
    	while (!current.latest_decision.target.is_terminal())
    	{
    		next_best_decision = current.latest_decision.target.get_best_decision();
    		current = new DP_Prefix_Solution(current, next_best_decision);
		}
		// Precision may be a problem here, hence the precision cutoff
		//System.out.println(String.format("%.4f", (pref.get_cost() + pref.latest_decision.target.get_opt_cost())));
		//System.out.println(String.format("%.4f", current.get_cost()));
    	//assert String.format("%.4f", (pref.get_cost() + pref.latest_decision.target.get_opt_cost())).equals(String.format("%.4f", current.get_cost())); 
    	return current;
    }
	
	private void add_candidates(Collection<DP_Prefix_Solution> cands)
	{
		if (CompileTimeConfig.heap_type == "binary_heap")
		{
			for (DP_Prefix_Solution cand : cands)
				global_pq_binary_heap.add(cand);
		}
		else if (CompileTimeConfig.heap_type == "fibonacci_heap")
		{
			for (DP_Prefix_Solution cand : cands)
				global_pq_fibonacci_heap.insert(cand);
		}
		else if (CompileTimeConfig.heap_type == "pairing_heap")
		{
			for (DP_Prefix_Solution cand : cands)
				global_pq_pairing_heap.insert(cand);
		}
		else if (CompileTimeConfig.heap_type == "hollow_heap")
		{
			for (DP_Prefix_Solution cand : cands)
				global_pq_hollow_heap.insert(cand);
		}
	}

	/** 
	 * Initialization of the data structures needed at each DP_DesicionSet
	 * in order to compute a partial order among decisions.
	 * @param decisions The set of decisions whose data structures will be initialized.
	 */
    public abstract void initialize_partial_order(DP_DecisionSet decisions);

	/** 
	 * Find the successors of a given decision among the other decisions in the {@link entities.paths.DP_DecisionSet}.
	 * The way that successors are computed depends on the variant (subclass).
	 * @param dec The decision whose successors will be computed.
	 * @return DP_Decision The successor decisions according to the (partial) order.
	 */
    public abstract List<DP_Decision> get_successors(DP_Decision dec);

	/** 
	 * Initializes the data structures needed for all nodes.
	 * Visits all the nodes in a DFS traversal.
	 */
    public void initialize_data_structures()
	{
		Stack<DP_State_Node> dfs_stack = new Stack<DP_State_Node>();
		dfs_stack.push(instance.starting_node);

		DP_State_Node curr_node;
		while (!dfs_stack.isEmpty())
		{
			curr_node = dfs_stack.pop();
			initialize_partial_order(curr_node.decisions);
			for (DP_Decision dec : curr_node.get_decisions())
			{
				if (!dec.target.decisions.partial_order_computed)
					dfs_stack.push(dec.target);
			}
		}
	}
}