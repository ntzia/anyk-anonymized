#!/usr/bin/env python

import sys 
import os
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

## -- Read input
algorithms = ["Recursive", "YannakakisSorting", "psql", "sysx"]
inFileName = "outputs/synthetic_path_n1000_l5_d100"
outFileName = "plots/anyk_presentation"
title = "5-Path Synthetic"
n = 1000
l = 5
d = 100
cutoff = sys.maxint

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

markers=['x', '^', '*', 'd', 'o', 's', '']
markersizes=[11, 12, 14, 9, 13, 13, 0]
fillstyles=['full', 'full', 'full', 'full', 'none', 'none', 'full']
linewidths=[1.5, 1.5, 1.5, 1.5, 1.5, 2, 2]
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

	if alg == "psql":
		# Read file
		try:
			fp1 = open(inFileName_dbms + "_" + alg + ".out")
		except IOError:
			print "Could not open file " + inFileName_dbms + "_" + alg + ".out"
			continue

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
			print "No data points to plot found for " + title + " , " + alg
			times[alg] = [None for k in k_list]
		else:

			# Print the number of instances (only once)
			if (i == 0):
				print str(instances_no) + " instances of " + title

			# Now build one list by taking the median
			times[alg] = []
			index = 0
			for k in k_list:
				times[alg].append(np.median(times_aux[0]))     

	elif alg == "sysx":
		# Read file
		try:
			fp1 = open(inFileName_dbms + "_" + alg + ".out")
		except IOError:
			print "Could not open file " + inFileName_dbms + "_" + alg + ".out"
			continue

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
			print "No data points to plot found for " + title + " , " + alg
			times[alg] = [None for k in k_list]
		else:

			# Print the number of instances (only once)
			if (i == 0):
				print str(instances_no) + " instances of " + title + " , " + alg

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
			print "Could not open file " + inFileName_dbms + "_" + alg + ".out"
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
			print "No data points to plot found for " + title + " , " + alg
			times[alg] = [None for k in k_list]
		else:

			# If some instances contained more data points than others, cut them off
			instances_no = len(times_aux[0])
			while (len(times_aux[-1]) < instances_no):
				times_aux = times_aux[:-1]
				k_list = k_list[:-1]

			# Print the number of instances (only once)
			if (i == 0):
				print str(instances_no) + " instances of " + title

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
	mark_frequency = (len(k_list) - 1) / 5
	lns += ax.plot(times[alg], k_list, label=alg_label, marker = markers[i], markersize = markersizes[i], markevery = mark_frequency,
					linestyle = linestyles[alg], linewidth=linewidths[i], fillstyle=fillstyles[i], alpha=alphas[i])
	# marker=marker_list[i], markersize=8

#ax.set_xscale('log')
ax.grid()

ax.set(xlabel="Time-to-$k$ (sec)", ylabel="#Answers $k$")
# plt.legend()
# plt.title(title, fontsize=16)

plt.ticklabel_format(style='sci', axis='y', scilimits=(0,0))

cmap = plt.get_cmap("tab10")

# Clean the canvas
while lns != []:
	ln = lns.pop()
	#line = ln.pop(0)
	ln.remove()

last_k = k_list[-1]
first_k = k_list[0]

# Plot again
i = 1
alg = "YannakakisSorting"
alg_label = algorithm_labels[alg]
lns += ax.plot(times[alg], k_list, label=alg_label, marker = markers[i], markersize = markersizes[i], markevery = mark_frequency,
				linestyle = linestyles[alg], linewidth=linewidths[i], fillstyle=fillstyles[i], alpha=alphas[i], color = cmap(i))
plt.text(6, 0.5 * 10**7, "JoinFirst", color=cmap(1), size=17)
batch_first = times["YannakakisSorting"][0]
batch_last = times["YannakakisSorting"][-1]
ax.annotate(('%.1f' % batch_last),xy = (batch_last - 2.4, last_k * 0.97), size=17, color = cmap(1))
ax.annotate(('%.1f' % batch_first),xy = (batch_first - 2.5, first_k), size=17, color = cmap(1))

plt.savefig(outFileName + "_1.pdf", format="pdf", bbox_inches="tight")
plt.savefig(outFileName + "_1.png", format="png", bbox_inches="tight")
plt.savefig(outFileName + "_1.svg", format="svg", bbox_inches="tight")

#---
i = 2
alg = "psql"
alg_label = algorithm_labels[alg]
lns += ax.plot(times[alg], k_list, label=alg_label, marker = markers[i], markersize = markersizes[i], markevery = mark_frequency,
				linestyle = linestyles[alg], linewidth=linewidths[i], fillstyle=fillstyles[i], alpha=alphas[i], color = cmap(i))
plt.text(12, 0.3 * 10**7, "PSQL", color=cmap(2), size=17)

i = 3
alg = "sysx"
alg_label = algorithm_labels[alg]
lns += ax.plot(times[alg], k_list, label=alg_label, marker = markers[i], markersize = markersizes[i], markevery = mark_frequency,
				linestyle = linestyles[alg], linewidth=linewidths[i], fillstyle=fillstyles[i], alpha=alphas[i], color = cmap(i))
plt.text(15.1, 0.7 * 10**7, "System X", color=cmap(3), size=17)


plt.savefig(outFileName + "_2.pdf", format="pdf", bbox_inches="tight")
plt.savefig(outFileName + "_2.png", format="png", bbox_inches="tight")
plt.savefig(outFileName + "_2.svg", format="svg", bbox_inches="tight")


#----
i = 0
alg = "Recursive"
alg_label = algorithm_labels[alg]
lns += ax.plot(times[alg], k_list, label=alg_label, marker = markers[i], markersize = markersizes[i], markevery = mark_frequency,
				linestyle = linestyles[alg], linewidth=linewidths[i], fillstyle=fillstyles[i], alpha=alphas[i], color = cmap(i))
plt.text(3, 0.3 * 10**7, "Any-k", color=cmap(0), size=17)
rea_last = times["Recursive"][-1]
rea_first = times["Recursive"][0]
ax.annotate(('%.1f' % rea_last),xy = (rea_last - 1, last_k * 0.97), size=17, color = cmap(0), textcoords="offset points", xytext=(-25,0))
ax.annotate(('%.2f' % rea_first),xy = (2.2, first_k), size=17, color = cmap(0), textcoords="offset points", xytext=(-25,0))


## Draw arrows
plt.arrow(7.2, 300000, -4, 0, color="black", length_includes_head=True, head_width=300000, head_length=0.5, width = 30000)
ax.annotate(("500" + r'$\times$'), xy = (4, 400000), size=21, color = "black", weight='bold')
plt.arrow(8.5, last_k * 0.99, -1.5, 0, color="black", length_includes_head=True, head_width=300000, head_length=0.5, width = 30000)
ax.annotate(("1.6" + r'$\times$'), xy = (6.5, last_k * 0.89), size=21, color = "black", weight='bold')

plt.savefig(outFileName + ".pdf", format="pdf", bbox_inches="tight")
plt.savefig(outFileName + ".png", format="png", bbox_inches="tight")
plt.savefig(outFileName + ".svg", format="svg", bbox_inches="tight")
