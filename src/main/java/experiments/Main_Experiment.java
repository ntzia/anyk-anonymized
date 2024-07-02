package experiments;

import java.io.IOException;
import java.util.Iterator;

import org.apache.commons.cli.CommandLine;
import org.apache.commons.cli.CommandLineParser;
import org.apache.commons.cli.DefaultParser;
import org.apache.commons.cli.HelpFormatter;
import org.apache.commons.cli.Option;
import org.apache.commons.cli.Options;
import org.apache.commons.cli.ParseException;

import distributed_tools.JsonOption;
import distributed_tools.JsonOptionParser;
import distributed_tools.JsonParserTree;
import entities.trees.Tree_ThetaJoin_Query;

public class Main_Experiment {
    public static String getName() {
        String className = Thread.currentThread().getStackTrace()[2].getClassName();
        return className;
    }

    public static void main(String args[]) throws IOException {
        Options options = new Options();

        Option query_file = new Option("q", "query", true, "path of reddit_query.json file");
        query_file.setRequired(true);
        options.addOption(query_file);

        Option option_file = new Option("o", "options", true, "path of reddit_option.json file");
        option_file.setRequired(true);
        options.addOption(option_file);

        Option result_file_path = new Option("f", "file", false, "path of reddit_option.json file");
        option_file.setRequired(true);
        options.addOption(option_file);

        CommandLineParser parser = new DefaultParser();
        HelpFormatter formatter = new HelpFormatter();
        CommandLine cmd = null;
        try {
            cmd = parser.parse(options, args);
        } catch (ParseException e) {
            System.err.println(e.getMessage());
            formatter.printHelp(getName(), options);
            System.exit(1);
        }

        // TODO: find file path from file name without requiring an absolute path
        String query_file_path = cmd.getOptionValue(query_file);
        String option_file_path = cmd.getOptionValue(option_file);

        System.out.println("query file path: " + query_file_path);
        System.out.println("option file path: " + option_file_path);
        JsonOptionParser jsonOptionParser = new JsonOptionParser(option_file_path);
        JsonOption jsonOption = jsonOptionParser.getJsonOption();

        JsonParserTree treeParser = new JsonParserTree(query_file_path);
        Tree_ThetaJoin_Query tree_query = treeParser.parseQuery();
        treeParser.runSequentialAnyK(tree_query, jsonOption);
    }

    // print everything in the iterator
    public static void printElement(Iterator iter) {
        int cutoff = 0;
        System.out.println("Printing elements...");
        while (iter.hasNext() && cutoff < 10) {
            System.out.println(iter.next());
            cutoff++;
        }

    }

    // take reddit_query.json and reddit_option.json filepath and iterator from spark program
    public static void runFromSparkToFile(String query_file_path, String option_file_path,
                                          Iterator iter, String region_key)
            throws IOException {

        JsonOptionParser jsonOptionParser = new JsonOptionParser(option_file_path);
        JsonOption jsonOption = jsonOptionParser.getJsonOption();

        JsonParserTree treeParser = new JsonParserTree(query_file_path);
        Tree_ThetaJoin_Query tree_query = treeParser.parseQueryFromSpark(iter);

        // write solutions directly to files without returning the solution lists
        treeParser.writeSolutionToFile(tree_query, jsonOption, region_key);

    }


    // take reddit_query.json and reddit_option.json filepath and iterator from spark program
    public static void runFromSparkToKafka(String topicName,
                                           String query_file_path,
                                           String option_file_path,
                                           Iterator iter,
                                           String region_key) throws IOException {

        JsonOptionParser jsonOptionParser = new JsonOptionParser(option_file_path);
        JsonOption jsonOption = jsonOptionParser.getJsonOption();

        JsonParserTree treeParser = new JsonParserTree(query_file_path);
        Tree_ThetaJoin_Query tree_query = treeParser.parseQueryFromSpark(iter);

        treeParser.writeSolutionToKafka(topicName, tree_query, jsonOption, region_key);
    }
}
