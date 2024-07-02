#!/bin/bash

source ../execution_parameters.sh
JAR_PATH="../../../target/any-k-1.0.jar"
DATA_PATH="../Data/"
OUT_PATH="outputs/"
OPTS="$OTHER_OPTS $MEM"

ALG_LIST=("Recursive" "Quick" "QuickPlus" "YannakakisSorting")
# ALG_LIST=("Count")

# Synthetic, All results
for params in "4 10000" "3 100000" "6 100" #"5 1000"
do
	set -- $params # convert the "tuple" into the param args $1 $2...
    l=$1
	n=$2
	d=$((n / 10))

	for i in $(seq 1 $ITERS_MEDIUM);
	do
		for q in "star" "one_branch" #"path" 
		do
			# Create the input if it doesn't exist
			INPUT="${DATA_PATH}${q}_n${n}_l${l}_d${d}.in"
			if [ ! -f $INPUT ]; then
				java -cp ${JAR_PATH} data.BinaryRandomPattern -q $q -n $n -l $l -dom $d -o $INPUT
			fi  
			for alg in "${ALG_LIST[@]}"
			do
				java $OPTS -cp ${JAR_PATH} experiments.Equijoin -q $q -a $alg -i $INPUT -n $n -l $l -dom $d -ds -wi $JAVA_WARMUP_ITERS -ri $JAVA_RUN_ITERS >> "${OUT_PATH}synthetic_${q}_n${n}_l${l}_d${d}_${alg}.out"
			done	
			echo "Done with $q, n=${n}, l=${l}, d=${d}, run ${i}"
		done
	done
done

# Bitcoin path, All results
# Twitter path, All results
q="path"
for i in $(seq 1 $ITERS_MEDIUM);
do
	for params in "6 bitcoinotc_sample_26" #"4 bitcoinotc_sample_210"
	do
		set -- $params # convert the "tuple" into the param args $1 $2...
		l=$1
		graph=$2
		infile=${graph}
		for alg in "${ALG_LIST[@]}"
		do
			java $OPTS -cp ${JAR_PATH} experiments.Equijoin -q $q -a $alg -i "${DATA_PATH}${infile}.in" -sj -l $l -ds -wi $JAVA_WARMUP_ITERS -ri $JAVA_RUN_ITERS >> "${OUT_PATH}${infile}_${q}_allk_l${l}_${alg}.out"

			echo "Done with $graph, $q, $alg, l=$l, run $i"
		done
	done

	for params in "6 twitter_sample_27" "4 twitter_sample_28" "4 twitter_sample_29" "3 twitter_sample_210" "3 twitter_sample_211" 
	do
		set -- $params # convert the "tuple" into the param args $1 $2...
		l=$1
		graph=$2
		infile=${graph}

		for alg in "${ALG_LIST[@]}"
		do
			java $OPTS -cp ${JAR_PATH} experiments.Equijoin -q $q -a $alg -i "${DATA_PATH}${infile}.in" -sj -l $l -ds -wi $JAVA_WARMUP_ITERS -ri $JAVA_RUN_ITERS >> "${OUT_PATH}${infile}_${q}_allk_l${l}_${alg}.out"

			echo "Done with $graph, $q, $alg, l=$l, run $i"
		done
	done
done

## Other path, all results
for i in $(seq 1 $ITERS_MEDIUM);
do
	for q in "star" #"path" 
	do
		for params in "4 foodweb" "4 friendship" #"3 foodweb"  "5 foodweb" "3 friendship"  "5 friendship"
		do
			set -- $params # convert the "tuple" into the param args $1 $2...
			l=$1
			graph=$2
			infile=${graph}
			for alg in "${ALG_LIST[@]}"
			do
				java $OPTS -cp ${JAR_PATH} experiments.Equijoin -q $q -a $alg -i "${DATA_PATH}${infile}.in" -sj -l $l -ds -wi $JAVA_WARMUP_ITERS -ri $JAVA_RUN_ITERS >> "${OUT_PATH}${infile}_${q}_allk_l${l}_${alg}.out"

				echo "Done with $graph, $q, $alg, l=$l, run $i"
			done
		done
	done
done

## Real data, few results
ALG_LIST=("Recursive" "Quick" "QuickPlus")
# ALG_LIST=("Count")
for q in "star" # "path" "binary_star"
do
	# k = n
	for params in "bitcoinotc 35592" # "twitter_sample_217 3615171"
	do
		set -- $params # convert the "tuple" into the param args $1 $2...
		graph=$1
		k=$2
		for l in 6 4
		do
			for i in $(seq 1 4000); #$ITERS_MANY);
			do
				for alg in "${ALG_LIST[@]}"
				do
					java $OPTS -cp ${JAR_PATH} experiments.Equijoin -q $q -a $alg -i "${DATA_PATH}${graph}.in" -sj -ds -k $k -l $l -wi $JAVA_WARMUP_ITERS -ri $JAVA_RUN_ITERS >> "${OUT_PATH}${graph}_${q}_fewk_l${l}_${alg}.out"

					echo "Done with $graph, $q, $alg, l=$l, few results, run $i"
				done
			done
		done
	done
done