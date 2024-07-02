#!/usr/bin/env python

import networkx as nx
import sys

def sample(dir, fout_name, max_id = sys.maxint):
	with open('soc-sign-bitcoinotc.csv', 'r') as fin:
		with open(fout_name, 'w') as fout:
			G = nx.DiGraph()
			fout.write("Relation Edges" + '\n')
			fout.write("From To" + '\n')
			for line in fin:
				n1, n2, rating, time = line.split(',')
				if int(n1) <= max_id and int(n2) <= max_id:
					fout.write(str(n1) + ' ' + str(n2) + ' ' + str(10 - int(rating)) + '\n')
					G.add_edge(int(n1), int(n2))
			fout.write("End of Edges" + '\n')
			fout.close()

			print "===== BitcoinOTC ==== (max node id = " + str(max_id) + ")"  
			print "Number of nodes = " + str(nx.number_of_nodes(G))
			print "Number of edges = " + str(nx.number_of_edges(G))
			degrees = nx.degree(G)
			degree_list = [d for (_, d) in degrees]
			print "Max degree = " + str(max(degree_list))
			avg_degree = sum(degree_list) * 1.0 / len(degree_list)
			print "Average degree = " + str(avg_degree)


if __name__ == "__main__":
	sample(".", 'bitcoinotc.in')

	sample(".", 'bitcoinotc_sample_26.in', max_id=64)
	sample(".", 'bitcoinotc_sample_27.in', max_id=128)
	sample(".", 'bitcoinotc_sample_28.in', max_id=256)
	sample(".", 'bitcoinotc_sample_29.in', max_id=512)
	sample(".", 'bitcoinotc_sample_210.in', max_id=1024)
	sample(".", 'bitcoinotc_sample_211.in', max_id=2048)
	sample(".", 'bitcoinotc_sample_212.in', max_id=4096)
	sample(".", 'bitcoinotc_sample_all.in')