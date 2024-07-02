#!/usr/bin/env python

import networkx as nx
import sys

def sample(input_file, fout_name, max_id = sys.maxint, invert_weights = False):
	with open(input_file, 'r') as fin:
		with open(fout_name, 'w') as fout:
			G = nx.DiGraph()
			fout.write("Relation Edges" + '\n')
			fout.write("From To" + '\n')
			for line in fin:
				if line.startswith('% ') or line.strip() == '':
					continue

				n1, n2, weight = line.split()
				if int(n1) <= max_id and int(n2) <= max_id:

					if invert_weights:
						fout.write(str(n1) + ' ' + str(n2) + ' -' + str(weight) + '\n')
					else:
						fout.write(str(n1) + ' ' + str(n2) + ' ' + str(weight) + '\n')
					G.add_edge(int(n1), int(n2))
			fout.write("End of Edges" + '\n')
			fout.close()

			print "===== " + input_file.split("/")[1] + " ==== (max node id = " + str(max_id) + ")"  
			print "Number of nodes = " + str(nx.number_of_nodes(G))
			print "Number of edges = " + str(nx.number_of_edges(G))
			degrees = nx.degree(G)
			degree_list = [d for (_, d) in degrees]
			print "Max degree = " + str(max(degree_list))
			avg_degree = sum(degree_list) * 1.0 / len(degree_list)
			print "Average degree = " + str(avg_degree)


if __name__ == "__main__":
	sample('Airport-dataset/out.opsahl-usairport', 'airport.in', invert_weights = True)
	sample('Friendship-dataset/out.moreno_health_health', 'friendship.in', invert_weights = True)
	sample('Foodweb-dataset/out.foodweb-baydry', 'foodweb.in', invert_weights = True)
	