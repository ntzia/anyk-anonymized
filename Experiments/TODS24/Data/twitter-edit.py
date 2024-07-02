#!/usr/bin/env python

import networkx as nx
import sys 
import os


def sample(dir, max_id, fout_name):
	## Read the file and keep only ids lower than max_id
	graphfile = os.path.join(dir, "twitter_reduced" + ".csv")

	## Create the graph in networkx
	G = nx.DiGraph()

	with open(graphfile) as f:
		lines = f.readlines()
	for line in lines:
		node_fro = int(line.split(',')[0])
		node_to = int(line.split(',')[1])
		if node_fro <= max_id and node_to <= max_id:
			G.add_edge(node_fro, node_to)


	print "===== " + fout_name + " ===="
	print "Number of nodes = " + str(nx.number_of_nodes(G))
	print "Number of edges = " + str(nx.number_of_edges(G))
	degrees = nx.degree(G)
	degree_list = [d for (_, d) in degrees]
	print "Max degree = " + str(max(degree_list))
	avg_degree = sum(degree_list) * 1.0 / len(degree_list)
	print "Average degree = " + str(avg_degree)
	# print "Degree histogram: " + str(nx.degree_histogram(G))

	## Compute edge weights with PageRank

	score = nx.pagerank(G)

	fout = open(fout_name + ".in", 'w')
	fout.write("Relation Edges\n")
	fout.write("From To\n")
	for (fromNode, toNode) in list(G.edges()):
		cost = (1.0 - score[fromNode]) + (1.0 - score[toNode])
		fromNode = int(fromNode)
		toNode = int(toNode)
		fout.write(str(fromNode) + " " + str(toNode) + " " + str(cost) + "\n")
	fout.write("End of Edges" + '\n')


if __name__ == "__main__":
	# sample(".", 8000, "twitter_small")
	# sample(".", 80000, "twitter_large")

	# sample(".", 128, "twitter_sample_27")
	# sample(".", 256, "twitter_sample_28")
	# sample(".", 512, "twitter_sample_29")
	# sample(".", 1024, "twitter_sample_210")
	# sample(".", 2048, "twitter_sample_211")
	# sample(".", 4096, "twitter_sample_212")
	# sample(".", 8192, "twitter_sample_213")
	# sample(".", 2**14, "twitter_sample_214")
	# sample(".", 2**15, "twitter_sample_215")
	# sample(".", 2**16, "twitter_sample_216")
	sample(".", 131072, "twitter_sample_217")