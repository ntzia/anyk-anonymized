#!/usr/bin/env python

import sys 
import os
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

## -- Read input
import argparse
parser = argparse.ArgumentParser(description='Plotting script')

parser.add_argument('-a', nargs='+', dest="alg_list", default=[], help="list of algorithms")
parser.add_argument('-std', nargs='+', dest="std_list", default=[], help="list of standard deviations (x-axis)")
parser.add_argument('-x', nargs='+', dest="x_labels_list", default=[], help="list of labels for x-axis")
parser.add_argument('-k', action='store', dest="k_to_plot", default=[], help="the value k for which we plot TT(k)")
parser.add_argument('-q', action='store', dest="query", default=[], help="the id of the query")
parser.add_argument('-n', action="store", dest="n", default="-1", help="relation size")
parser.add_argument('-l', action='store', dest="l", default=[], help="the length of the query")
parser.add_argument('-o', action="store", dest="outFileName", default="out", help="Name of output file")
parser.add_argument('-i', action="store", dest="inFileName", default="out", help="Name of input file")
parser.add_argument('-t', action="store", dest="title", default="", help="Title of figure")


arg_results = parser.parse_args()
algorithms = arg_results.alg_list
inFileName = arg_results.inFileName
outFileName = arg_results.outFileName
title = arg_results.title
std_list = arg_results.std_list
x_labels_list = arg_results.x_labels_list
k_to_plot = int(arg_results.k_to_plot)
l = arg_results.l
n = arg_results.n
query = arg_results.query

algorithm_labels = {}
algorithm_labels["Batch"] = "Batch(No sort)"
algorithm_labels["BatchSorting"] = "JoinFirst"
algorithm_labels["YannakakisSorting"] = "JoinFirst"
algorithm_labels["BatchHeap"] = "Batch(Heap) Lower Bound"
algorithm_labels["QEq_Lazy"] = "QuadEqui Lower Bound"
algorithm_labels["Lazy"] = "Factorized Any-k"
algorithm_labels["psql"] = "PSQL"
algorithm_labels["sysx"] = "System X"
algorithm_labels["duckdb"] = "DuckDB"
algorithm_labels["QuickPlus"] = "Any-k"
algorithm_labels["Quick"] = "Any-k"
algorithm_labels["Recursive"] = "Any-k"

# Initialize plot
# marker_list = ["1", "2", "3", "x"]
plt.rcParams.update({'font.size': 19})
fig, ax = plt.subplots()

markers=['x', '^', '*', 'd', 'o', '', '']
markersizes=[11, 12, 14, 9, 13, 0, 0]
fillstyles=['full', 'full', 'full', 'full', 'none', 'full', 'full']
linewidths=[1.5, 1.5, 1.5, 1.5, 1.5, 2, 2]
alphas=[1, 1, 0.9, 1, 1, 1, 1]
lns = []

times = {}			# times is a dictionary that for each algorithm contains a list of runtimes (one for each n)
times_std = {}		# times is a dictionary that for each algorithm contains a list of runtimes (one for each n)

for i in range(len(algorithms)):
	alg = algorithms[i]
	times[alg] = []
	times_std[alg] = []

	for std in std_list:
		
		times_aux = []		# times_aux contains a list runtimes for a given n (one for each repetition)
		prev_k = -1			# records the last k we read so that we can find the maximal k for each repetition

		# Read file
		try:
			fp1 = open(inFileName + "_std" + str(std) + "_" + alg + ".out")
		except IOError:
			times[alg].append(None)
			times_std[alg].append(None)
			continue

		if (alg == "psql"):
			line = fp1.readline()
			while line:

				if line.startswith(" Execution time"):
					tokens = line.split()
					runtime = float(tokens[2]) / 1000.0
					times_aux.append(runtime)

				line = fp1.readline()
			fp1.close()
		elif (alg == "sysx"):
			line = fp1.readline()
			while line:

				if line.startswith("   CPU time ="):
					tokens = line.split()
					runtime = float(tokens[3]) / 1000.0
					times_aux.append(runtime)

				line = fp1.readline()
			fp1.close()
		else:
			line = fp1.readline()
			while line:

				if line.startswith("k="):
					tokens = line.split()
					k = int(tokens[1])
					runtime = float(tokens[3])
					if (k == k_to_plot):
						times_aux.append(runtime)

					# Store for checking in the next iteration
					prev_k = k
					prev_runtime = runtime

				line = fp1.readline()
			fp1.close()

		# We now have a list of runtimes for n gathered in times_aux
		# Take the median and append to times
		if len(times_aux):
			median_runtime = np.median(times_aux)
			std = np.std(times_aux)
			times[alg].append(median_runtime)
			times_std[alg].append(std)
		else:
			times[alg].append(None)
			times_std[alg].append(None)

# Plot the algorithms
for i in range(len(algorithms)):
	alg = algorithms[i]
	alg_label = algorithm_labels[alg]
	if x_labels_list:
		ax.plot(x_labels_list, times[alg], label=alg_label, marker = markers[i], markersize = markersizes[i], fillstyle=fillstyles[i])
	else:
		ax.plot(std_list, times[alg], label=alg_label, marker = markers[i], markersize = markersizes[i], fillstyle=fillstyles[i])
	# print alg, times[alg]
	#ax.errorbar(n_list, times[alg], yerr=times_std[alg], label=alg_label, marker = markers[i], markersize = markersizes[i], capsize=5, capthick=1)
	# marker=marker_list[i], markersize=8

#plt.legend()


## Add text for OOM exceptions
# cmap = plt.get_cmap("tab10")
# for i in range(len(algorithms)):
# 	alg = algorithms[i]
# 	# Find the index where we first get a None if it exists
# 	found_None = False
# 	for idx in range(len(times[alg])):
# 		if times[alg][idx] is None:
# 			found_None = True
# 			break
# 	if idx != 0 and found_None and alg != "psql" and alg != "sysx":
# 		if "SynQ1, l=2" in title:
# 			ax.text(n_list[idx], times[alg][idx - 1] * 1.2, "OOM", color = cmap(i), size=17)
# 		else:
# 			ax.text((n_list[idx] + n_list[idx-1]) / 2.0, times[alg][idx - 1] * 2, "OOM", color = cmap(i), size=17)

ax.set_yscale('log', base=10)
# ax.set_xscale('log', base=2)
ax.set_ylim([None, 1500])

if k_to_plot == 1000:
	ax.set(xlabel="standard deviation of Gaussian", ylabel="TT($10^3$) sec")
	ax.xaxis.label.set_size(20)
else:
	ax.set(xlabel="standard deviation of Gaussian", ylabel="TT(" + str(k_to_plot) + ") sec")

#plt.title(title)
# plt.legend()
ax.grid()

plt.savefig(outFileName + ".pdf", format="pdf", bbox_inches="tight")
plt.savefig(outFileName + ".png", format="png", bbox_inches="tight")
plt.savefig(outFileName + ".svg", format="svg", bbox_inches="tight")

## Legend
# plt.rc('text', usetex=True)  
# plt.rc('font', family='serif', size=20) 
# h, l = ax.get_legend_handles_labels()
# figlegend = plt.figure(figsize=(4 * len(algorithms), 0.5))
# ax_leg = figlegend.add_subplot(111)
# ax_leg.legend(h, l, loc='center', ncol=len(algorithms), fancybox=True, shadow=True, prop={'size':30}, markerscale=2)
# ax_leg.axis('off')
# figlegend.savefig("plots/legend.pdf", format="pdf", bbox_inches="tight")