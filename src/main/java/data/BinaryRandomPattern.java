package data;

import java.util.Comparator;
import java.util.Set;
import java.util.TreeSet;
import java.util.concurrent.ThreadLocalRandom;

import org.apache.commons.cli.CommandLine;
import org.apache.commons.cli.CommandLineParser;
import org.apache.commons.cli.DefaultParser;
import org.apache.commons.cli.HelpFormatter;
import org.apache.commons.cli.Option;
import org.apache.commons.cli.Options;
import org.apache.commons.cli.ParseException;

import entities.Relation;
import entities.Tuple;

/** 
 * A subclass of the data generator {@link data.Database_Query_Generator}.
 * The relations are generated with two attributes.
 * The join pattern between the relations is uniform in the sense that 
 * we sample uniformly at random the attribute values from a fixed domain, given as a parameter.
 * A small domain size will result in a very dense join pattern.
 * A large domain size will result in many tuples not being part of the join result.
 * @author anonymous anonymous
*/
public class BinaryRandomPattern extends Database_Query_Generator
{	
	/** 
	 * The size of the domain of the attributes.
	*/
	private int domain;
	/** 
	 * The type of the query (path, star, etc.).
	 * Only affects the names of the attributes.
	*/
	private String query;

	public BinaryRandomPattern(int n, int l, int domain, String query, WeightAssigner weight_assigner)
	{
		super(n, l, weight_assigner);

		// CAUTION: if the domain is too small, then this method would enter an endless loop
		// The maximum n we can generate with domain is by choosing all the domain values in the first col
		// followed by n values in the second col
		long allowed_pairs = (long) domain * (long) domain;
		if (allowed_pairs < n)
		{
			System.err.println("Domain too small for the specified n!");
			System.exit(1);
		}

		this.domain = domain;
		this.query = query;
	}

	public BinaryRandomPattern(int n, int l, int domain, String query)
	{
		super(n, l);

		// CAUTION: if the domain is too small, then this method would enter an endless loop
		// The maximum n we can generate with domain is by choosing all the domain values in the first col
		// followed by n values in the second col
		long allowed_pairs = (long) domain * (long) domain;
		if (allowed_pairs < n)
		{
			System.err.println("Domain too small for the specified n!");
			System.exit(1);
		}

		this.domain = domain;
		this.query = query;
	}
	
	@Override
	protected void populate_database()
	{
		Relation r;
		double[] tup_vals;
		double tup_weight;
		int attribute_no = 1;
		Set<Tuple> non_duplicate_tuples;
		Tuple new_tuple;
		int n;

		// In iteration relation_no, we populate relation relation_no with random values
		for (int relation_no = 1; relation_no <= l; relation_no++)
		{
			n = n_list.get(relation_no - 1);
			
			// Instantiate relation object
			if (query.equals("path"))
			{
				// In a path, the attribute of the left relation is the same as the attribute of the right relation
				r = new Relation("R" + relation_no, new String[]{"A" + attribute_no, "A" + (attribute_no + 1)});
				attribute_no += 1;
			}
			else if (query.equals("star"))
			{
				// In a star, all the relations join on A1, the first attribute of R1
				r = new Relation("R" + relation_no, new String[]{"A1", "A" + (attribute_no + 1)});
				attribute_no += 1;
			}
			else if (query.equals("onebranch"))
			{
				// A onebranch is like a path, but the third-to-last relation branches into two others
				if (relation_no <= l - 1)
					r = new Relation("R" + relation_no, new String[]{"A" + attribute_no, "A" + (attribute_no + 1)});
				else 
					r = new Relation("R" + relation_no, new String[]{"A" + (attribute_no - 2), "A" + (attribute_no + 1)});
				attribute_no += 1;
			}
			else if (query.equals("cycle"))
			{
				// In a cycle, do the same as the path except for the last relation that must join back to the first one
				if (relation_no != l)
				{
					r = new Relation("R" + relation_no, new String[]{"A" + attribute_no, "A" + (attribute_no + 1)});
					attribute_no += 1;
				}
				else
				{
					r = new Relation("R" + relation_no, new String[]{"A" + attribute_no, "A1"});
				}
			}
			else
			{
				// If none of the above is specified, just make each relation have separate attributes
				r = new Relation("R" + relation_no, new String[]{"A" + attribute_no, "A" + (attribute_no + 1)});
				attribute_no += 1;				
			}

			// Add the random tuples to a set in order to avoid duplicates
			non_duplicate_tuples = new TreeSet<Tuple>(new Comparator<Tuple>() 
			{
				public int compare(Tuple t1, Tuple t2) 
				{
					if (t1.values[0] > t2.values[0]) return 1;
					else if (t1.values[0] < t2.values[0]) return -1;

					if (t1.values[1] > t2.values[1]) return 1;
					else if (t1.values[1] < t2.values[1]) return -1;
				
					return 0;
				}
			});
			while (non_duplicate_tuples.size() < n)
			{
				// Instantiate a random tuple
				tup_vals = new double[2];
				tup_vals[0] = ThreadLocalRandom.current().nextInt(domain);
				tup_vals[1] = ThreadLocalRandom.current().nextInt(domain);
				tup_weight = this.weight_assigner.get_tuple_weight(non_duplicate_tuples.size(), relation_no);
				new_tuple = new Tuple(tup_vals, tup_weight, r);

				non_duplicate_tuples.add(new_tuple);
			}

			// Go through the set and add the tuples to the relation
			for (Tuple t : non_duplicate_tuples) r.insert(t);
			database.add(r);
		}
	}
	
	public static void main(String[] args) 
	{
        // Parse the command line
        Options options = new Options();

		// First parse the options that are common to all generators
		for (Option option : common_command_line_options()) options.addOption(option);

		// Generator-specific options below
		Option q_option = new Option("q", "queryType", true, "the type of the query (path, star, cycle)");
        q_option.setRequired(true);
		options.addOption(q_option);

        Option dom_option = new Option("dom", "domain", true, "size of domain to sample attribute values from");
        dom_option.setRequired(false);
        options.addOption(dom_option);


        CommandLineParser parser = new DefaultParser();
        HelpFormatter formatter = new HelpFormatter();
        CommandLine cmd = null;
        try
        {
            cmd = parser.parse(options, args);
        } 
        catch (ParseException e) 
        {
            System.err.println(e.getMessage());
            formatter.printHelp(getName(), options);
            System.exit(1);
        }

		String query = cmd.getOptionValue("queryType");
		int n = -1;
		if (cmd.hasOption("relationSize")) n = Integer.parseInt(cmd.getOptionValue("relationSize"));
		else
		{
			System.err.println("-n has to be set!");
            System.exit(1);
		}
		int l = Integer.parseInt(cmd.getOptionValue("relationNo"));
		int domain;
        if (cmd.hasOption("domain")) domain = Integer.parseInt(cmd.getOptionValue("domain"));
        else domain = n;
        Database_Query_Generator gen = new BinaryRandomPattern(n, l, domain, query);
		gen.parse_common_args(cmd);
        gen.create();
        gen.print_database();
	}
}
