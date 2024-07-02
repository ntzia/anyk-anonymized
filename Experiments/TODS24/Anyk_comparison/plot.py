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
parser.add_argument('-o', action="store", dest="outFileName", default="out", help="Name of output file")
parser.add_argument('-i', action="store", dest="inFileName", default="out", help="Name of input file")
parser.add_argument('-t', action="store", dest="title", default="", help="Title of figure")
parser.add_argument('-n', action="store", dest="n", default="-1", help="n")
parser.add_argument('-l', action="store", dest="l", default="-1", help="l")
parser.add_argument('-d', action="store", dest="d", default="-1", help="d")
parser.add_argument('-c', action="store", dest="cutoff", default=sys.maxsize, help="Use to stop plotting after some k")


arg_results = parser.parse_args()
algorithms = arg_results.alg_list
inFileName = arg_results.inFileName
outFileName = arg_results.outFileName
title = arg_results.title
n = int(arg_results.n)
l = int(arg_results.l)
d = int(arg_results.d)
cutoff = int(arg_results.cutoff)

# algorithms = ["BatchSorting", "MLE", "MLM", "MLH", "MLL", "REA"]
# algorithms = ["MLE", "MLM", "MLH", "MLL", "REA"]

algorithm_labels = {}
algorithm_labels["Batch"] = "Batch(No sort)"
algorithm_labels["BatchSorting"] = "Batch"
algorithm_labels["Eager"] = "Eager"
algorithm_labels["All"] = "All"
algorithm_labels["Take2"] = "Take2"
algorithm_labels["Lazy"] = "Lazy"
algorithm_labels["Quick"] = "AnyK-Part"
algorithm_labels["QuickMemoized"] = "AnyK-Part+"
algorithm_labels["QuickPlus"] = "AnyK-Part+"
algorithm_labels["Recursive"] = "AnyK-Rec"
algorithm_labels["NPRR"] = "Batch(No sort)"
algorithm_labels["NPRR_Sort"] = "Batch"
algorithm_labels["YannakakisSorting"] = "JoinFirst"
algorithm_labels["psql"] = "PSQL"
algorithm_labels["sysx"] = "System X"
algorithm_labels["duckdb"] = "DuckDB"

linestyles = {}
for alg in algorithms:
	linestyles[alg] = 'solid'
# linestyles["Recursive"] = (0, (5, 1))
# linestyles["Batch"] = 'dashdot'
# linestyles["BatchSorting"] = 'dashdot'
# linestyles["NPRR"] = 'dashdot'
# linestyles["NPRR_Sort"] = 'dashdot'

# Initialize plot
plt.rcParams.update({'font.size': 17})
fig, ax = plt.subplots()

markers=['x', '^', '*', 'd', 'o', 's', 'v']
markersizes=[11, 12, 14, 9, 13, 13, 12]
fillstyles=['full', 'full', 'full', 'full', 'none', 'none', 'full']
linewidths=[1.5, 1.5, 1.5, 1.5, 1.5, 2, 1.5]
alphas=[1, 1, 0.9, 1, 1, 1, 1]
lns = []
times = {}	# times[alg] contains a list of runtimes (one for each k)

for i in range(len(algorithms)):
	alg = algorithms[i]		
	times_aux = []		# times_aux contains a list of lists of runtimes (one list for each k contains all the runtimes for that k)

	inFileName_dbms = inFileName
	if "bitcoinotc" in inFileName_dbms:
		inFileName_dbms = inFileName_dbms.replace("path", "QBC1")
		inFileName_dbms = inFileName_dbms.replace("star", "QBC2")
	if "friendship" in inFileName_dbms or "foodweb" in inFileName_dbms:
		inFileName_dbms = inFileName_dbms.replace("path", "QWG_path")
		inFileName_dbms = inFileName_dbms.replace("star", "QWG_star")

	# Read file
	try:
		if alg == "psql" or alg == "sysx" or alg == "duckdb":
			fp1 = open(inFileName_dbms + "_" + alg + ".out")
		else:
			fp1 = open(inFileName + "_" + alg + ".out")
	except IOError:
		print("Could not open file " + inFileName + "_" + alg + ".out")
		continue

	if alg == "psql":
		line = fp1.readline()
		while line:
			if line.startswith(" Execution time"):
				tokens = line.split()
				runtime = float(tokens[2]) / 1000.0
				if times_aux == []:
					times_aux.append([])
				times_aux[0].append(runtime)
			line = fp1.readline()
		fp1.close()

		# If no data points were read, return an error
		if not times_aux:
			print("No data points to plot found for " + title + " , " + alg)
			times[alg] = [None for k in k_list]
		else:
			# Print the number of instances (only once)
			if (i == 0):
				print(str(instances_no) + " instances of " + title)

			# Now build one list by taking the median
			times[alg] = []
			index = 0
			for k in k_list:
				times[alg].append(np.median(times_aux[0]))     

	elif alg == "sysx":
		line = fp1.readline()
		while line:
			if line.startswith("   CPU time ="):
				tokens = line.split()
				runtime = float(tokens[3]) / 1000.0
				if times_aux == []:
					times_aux.append([])
				times_aux[0].append(runtime)
			line = fp1.readline()
		fp1.close()

		# If no data points were read, return an error
		if not times_aux:
			print("No data points to plot found for " + title + " , " + alg)
			times[alg] = [None for k in k_list]
		else:
			# Print the number of instances (only once)
			if (i == 0):
				print(str(instances_no) + " instances of " + title + " , " + alg)

			# Now build one list by taking the median
			times[alg] = []
			index = 0
			for k in k_list:
				times[alg].append(np.median(times_aux[0]))

	elif alg == "duckdb":
		line = fp1.readline()
		while line:
			if line.startswith("Time="):
				tokens = line.split()
				runtime = float(tokens[1])
				if times_aux == []:
					times_aux.append([])
				times_aux[0].append(runtime)
			line = fp1.readline()
		fp1.close()

		# If no data points were read, return an error
		if not times_aux:
			print("No data points to plot found for " + title + " , " + alg)
			times[alg] = [None for k in k_list]
		else:
			# Print the number of instances (only once)
			if (i == 0):
				print(str(instances_no) + " instances of " + title + " , " + alg)

			# Now build one list by taking the median
			times[alg] = []
			index = 0
			for k in k_list:
				times[alg].append(np.median(times_aux[0]))     

	else:
		k_list = []
		max_k = 0

		# Read file
		try:
			fp1 = open(inFileName + "_" + alg + ".out")
		except IOError:
			print("Could not open file " + inFileName + "_" + alg + ".out")
			continue

		line = fp1.readline()
		while line:

			if line.startswith("k="):
				tokens = line.split()
				k = int(tokens[1])
				if (k == 1): index = 0	# The index tells us which position in the list corresponds to the k we read
				else: index += 1
				if (k < cutoff):

					if (k > max_k): 
						max_k = k
						k_list.append(k)
						times_aux.append([])

					times_aux[index].append(float(tokens[3]))

			line = fp1.readline()
		fp1.close()

		# If no data points were read, return an error
		if not times_aux:
			print("No data points to plot found for " + title + " , " + alg)
			times[alg] = [None for k in k_list]
		else:

			# If some instances contained more data points than others, cut them off
			instances_no = len(times_aux[0])
			while (len(times_aux[-1]) < instances_no):
				times_aux = times_aux[:-1]
				k_list = k_list[:-1]

			# Print the number of instances (only once)
			if (i == 0):
				print(str(instances_no) + " instances of " + title)

			# Now build one list by taking the median
			times[alg] = []
			index = 0
			for k in k_list:
				runtimes = times_aux[index]
				median_runtime = np.median(runtimes)
				times[alg].append(median_runtime)
				index += 1

	# Plot
	alg_label = algorithm_labels[alg]
	mark_frequency = int((len(k_list) - 1) / 5)
	lns += ax.plot(times[alg], k_list, label=alg_label, marker = markers[i], markersize = markersizes[i], markevery = mark_frequency,
					linestyle = linestyles[alg], linewidth=linewidths[i], fillstyle=fillstyles[i], alpha=alphas[i])

#ax.set_xscale('log')
ax.grid()

ax.set(xlabel="Time-to-$k$ (sec)", ylabel="#Answers $k$")
# plt.legend()
# plt.title(title, fontsize=16)

plt.ticklabel_format(style='sci', axis='y', scilimits=(0,0))

cmap = plt.get_cmap("tab10")

# Annotate TTF-TTL for some of the plots that show all results
# 4-Path
## Also, for presentation purposes, create many figures step-by-step
if (n == 10000 and l == 4 and title.startswith("4-Path")):

	## ------------ First empty plot ------------------
	for artist in plt.gca().lines + plt.gca().collections:
		artist.remove()


	last_k = k_list[-1]
	first_k = k_list[0]

	## ------------ Plot YannakakisSorting ------------------
	alg = "YannakakisSorting"
	i = 3
	batch_first = times[alg][0]
	batch_last = times[alg][-1]
	alg_label = algorithm_labels[alg]
	lns += ax.plot(times[alg], k_list, label=alg_label, marker = markers[i], markersize = markersizes[i], markevery = mark_frequency,
					linewidth=linewidths[i], fillstyle=fillstyles[i], alpha=alphas[i], color = cmap(i))
	## Annotate data points
	ax.annotate(('%.1f' % batch_last),xy = (batch_last - 1, last_k), size=15, color = cmap(i))
	ax.annotate(('%.1f' % batch_first),xy = (batch_first + 0.3, first_k), size=15, color = cmap(i))

	plt.savefig(outFileName + "_1.pdf", format="pdf", bbox_inches="tight")
	plt.savefig(outFileName + "_1.png", format="png", bbox_inches="tight")
	plt.savefig(outFileName + "_1.svg", format="svg", bbox_inches="tight")

	## ------------ Then PSQL ------------------
	alg = "psql"
	i = 4
	psql_last = times["psql"][-1]
	alg_label = algorithm_labels[alg]
	lns += ax.plot(times[alg], k_list, label=alg_label, marker = markers[i], markersize = markersizes[i], markevery = mark_frequency,
					linewidth=linewidths[i], fillstyle=fillstyles[i], alpha=alphas[i], color = cmap(i))
	## Annotate data points
	ax.annotate(('%.1f' % psql_last),xy = (psql_last, last_k), size=15, color = cmap(i), textcoords="offset points", xytext=(-25,0))
	
	plt.savefig(outFileName + "_2.pdf", format="pdf", bbox_inches="tight")
	plt.savefig(outFileName + "_2.png", format="png", bbox_inches="tight")
	plt.savefig(outFileName + "_2.svg", format="svg", bbox_inches="tight")

	## ------------ Then Any-k ------------------
	rea_last = times["Recursive"][-1]
	rea_first = times["Recursive"][0]
	quickm_last = times["QuickMemoized"][-1]
	quick_last = times["Quick"][-1]

	alg = "Recursive"
	i = 0
	alg_label = algorithm_labels[alg]
	lns += ax.plot(times[alg], k_list, label=alg_label, marker = markers[i], markersize = markersizes[i], markevery = mark_frequency,
					linewidth=linewidths[i], fillstyle=fillstyles[i], alpha=alphas[i], color = cmap(i))

	alg = "Quick"
	i = 1
	alg_label = algorithm_labels[alg]
	lns += ax.plot(times[alg], k_list, label=alg_label, marker = markers[i], markersize = markersizes[i], markevery = mark_frequency,
					linewidth=linewidths[i], fillstyle=fillstyles[i], alpha=alphas[i], color = cmap(i))

	alg = "QuickMemoized"
	i = 2
	alg_label = algorithm_labels[alg]
	lns += ax.plot(times[alg], k_list, label=alg_label, marker = markers[i], markersize = markersizes[i], markevery = mark_frequency,
					linewidth=linewidths[i], fillstyle=fillstyles[i], alpha=alphas[i], color = cmap(i))

	ax.annotate(('%.1f' % rea_last),xy = (rea_last, last_k), size=15, color = cmap(0), textcoords="offset points", xytext=(-25,0))
	ax.annotate(('%.2f' % rea_first),xy = (-0, 10**6 / 2), size=15, color = cmap(0), textcoords="offset points", xytext=(-25,0))
	ax.annotate(('%.1f' % quickm_last),xy = (quickm_last, last_k), size=15, color = cmap(2), textcoords="offset points", xytext=(-25,0))
	ax.annotate(('%.1f' % quick_last),xy = (quick_last - 0.7, last_k), size=15, color = cmap(1), textcoords="offset points", xytext=(-25,0))
	
	plt.savefig(outFileName + "_3.pdf", format="pdf", bbox_inches="tight")
	plt.savefig(outFileName + "_3.png", format="png", bbox_inches="tight")
	plt.savefig(outFileName + "_3.svg", format="svg", bbox_inches="tight")

## 6-Path
if (n == 100 and l == 6 and title.startswith("6-Path")):
	last_k = k_list[-1]
	first_k = k_list[0]
	batch_first = times["YannakakisSorting"][0]
	batch_last = times["YannakakisSorting"][-1]
	rea_last = times["Recursive"][-1]
	rea_first = times["Recursive"][0]
	quickm_last = times["QuickMemoized"][-1]
	psql_last = times["psql"][-1]
	quick_last = times["Quick"][-1]
	# batch_nosort_first = times["Batch"][0]
	# batch_nosort_last = times["Batch"][-1]
	ax.annotate(('%.1f' % batch_last),xy = (batch_last - 1.3, last_k), size=15, color = cmap(3))
	ax.annotate(('%.1f' % batch_first),xy = (batch_first + 0.3, first_k), size=15, color = cmap(3))
	ax.annotate(('%.1f' % rea_last),xy = (rea_last, last_k), size=15, color = cmap(0), textcoords="offset points", xytext=(-25,0))
	ax.annotate(('%.3f' % rea_first),xy = (1.5, 0), size=15, color = cmap(0), textcoords="offset points", xytext=(-25,0))
	ax.annotate(('%.1f' % quickm_last),xy = (quickm_last + 1, last_k), size=15, color = cmap(2), textcoords="offset points", xytext=(-25,0))
	ax.annotate(('%.1f' % quick_last),xy = (quick_last + 0.3, last_k), size=15, color = cmap(1), textcoords="offset points", xytext=(-25,0))
	ax.annotate(('%.1f' % psql_last),xy = (psql_last - 0.5, last_k), size=15, color = cmap(4), textcoords="offset points", xytext=(-25,0))
	# batch_nosort_first = times["Batch"][0]
	# batch_nosort_last = times["Batch"][-1]

	# ax.annotate(('%.1f' % batch_nosort_last),xy = (batch_nosort_last, last_k), size=15, color = cmap(6))
	# ax.annotate(('%.1f' % batch_nosort_first),xy = (batch_nosort_first, first_k), size=15, color = cmap(6))


## 3-Path
if (n == 100000 and l == 3 and title.startswith("3-Path")):
	last_k = k_list[-1]
	first_k = k_list[0]
	batch_first = times["YannakakisSorting"][0]
	batch_last = times["YannakakisSorting"][-1]
	rea_last = times["Recursive"][-1]
	quickm_last = times["QuickMemoized"][-1]
	# batch_nosort_first = times["Batch"][0]
	# batch_nosort_last = times["Batch"][-1]
	
	ax.annotate(('%.1f' % batch_last),xy = (batch_last, last_k), size=15, color = cmap(3))
	ax.annotate(('%.1f' % batch_first),xy = (batch_first, first_k), size=15, color = cmap(3))
	ax.annotate(('%.1f' % rea_last),xy = (rea_last, last_k), size=15, color = cmap(0))
	ax.annotate(('%.1f' % quickm_last),xy = (quickm_last, last_k), size=15, color = cmap(2))

	# ax.annotate(('%.1f' % batch_nosort_last),xy = (batch_nosort_last, last_k), size=15, color = cmap(6))
	# ax.annotate(('%.1f' % batch_nosort_first),xy = (batch_nosort_first, first_k), size=15, color = cmap(6))


#if (n == 5000 and l == 4):
#	last_k = k_list[-1]
#	first_k = k_list[0]
#	batch_first = times["NPRR_Sort"][0]
#	batch_last = times["NPRR_Sort"][-1]
#	rea_last = times["Recursive"][-1]
#	
#	ax.annotate(('%.1f' % batch_last),xy = (batch_last, last_k), size=15, color = cmap(5))
#	ax.annotate(('%.1f' % batch_first),xy = (batch_first, first_k), size=15, color = cmap(5))
#	ax.annotate(('%.1f' % rea_last),xy = (rea_last, last_k), size=15, color = cmap(0), textcoords="offset points", xytext=(-25,0))

# ax.set_yscale('log', basey=10)
# ax.set_xscale('log', basex=10)


plt.savefig(outFileName + ".pdf", format="pdf", bbox_inches="tight")
plt.savefig(outFileName + ".png", format="png", bbox_inches="tight")
# plt.savefig(outFileName + ".svg", format="svg", bbox_inches="tight")
# if "twitter_sample_217_path_fewk_l6" in outFileName:
# 	plt.savefig(outFileName + ".svg", format="svg", bbox_inches="tight")

## Legend
plt.rc('text', usetex=True)  
plt.rc('font', family='serif', size=20) 

h, l = ax.get_legend_handles_labels()
figlegend = plt.figure(figsize=(4 * len(algorithms), 0.5))
ax_leg = figlegend.add_subplot(111)
ax_leg.legend(h, l, loc='center', ncol=len(algorithms), fancybox=True, shadow=True, prop={'size':30}, markerscale=2)
ax_leg.axis('off')
figlegend.savefig("plots/legend.pdf", format="pdf", bbox_inches="tight")
figlegend.savefig("plots/legend.svg", format="svg", bbox_inches="tight")