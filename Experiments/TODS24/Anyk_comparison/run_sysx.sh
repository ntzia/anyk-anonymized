#!/bin/bash

source ../execution_parameters.sh
JAR_PATH="../../../target/any-k-1.0.jar"
DATA_PATH="../Data/"
OUT_PATH="outputs/"

alg="sysx"
k=0

## Synthetic, All results
for params in "4 10000" "3 100000" "6 100" "5 1000"
do
	set -- $params # convert the "tuple" into the param args $1 $2...
    l=$1
	n=$2
	d=$((n / 10))

	for i in $(seq 1 $ITERS_MEDIUM);
	do
		for q in "path" "star" "one_branch"
		do
			# Create the input if it doesn't exist
			INPUT="${DATA_PATH}${q}_n${n}_l${l}_d${d}.in"
			if [ ! -f $INPUT ]; then
				java -cp ${JAR_PATH} data.BinaryRandomPattern -q $q -n $n -l $l -dom $d -o $INPUT
			fi  

            # Generate csv files
            ./in_to_csv.py $INPUT
            # Generate sql query
            ./"generate_sql_${q}.py" `pwd`/$DATA_PATH ${l} ${k} sysx
            # Run the query
			sqlcmd -y0 -S 127.0.0.1 -U Anyk -P Anyk_pwd -t 4000 -i "sql_queries/${q}_l${l}_k${k}_sysx.sql" 2>> "${OUT_PATH}synthetic_${q}_n${n}_l${l}_d${d}_${alg}.out" | grep -A 9999 "SQL Server Execution Times:" >> "${OUT_PATH}synthetic_${q}_n${n}_l${l}_d${d}_${alg}.out"
            # Delete the csv files
            for j in $(seq 1 ${l});
            do
                rm "${DATA_PATH}R${j}.csv"
            done

            echo "Done with $q, n=${n}, l=${l}, d=${d}, sysx, run ${i}"
		done
	done
done

# Clean sql server temp files
sqlcmd -y0 -S 127.0.0.1 -U Anyk -P Anyk_pwd -i ../sqlserv_clean.sql  > /dev/null


## Bitcoin path, All results
q="QBC1"
for params in "4 bitcoinotc_sample_210" #"4 bitcoinotc_sample_211" "3 bitcoinotc" 
do
	set -- $params # convert the "tuple" into the param args $1 $2...
	l=$1
	graph=$2
	infile=${graph}
	for i in $(seq 1 $ITERS_MEDIUM);
	do
			# Generate csv files
			./in_to_csv.py "$DATA_PATH${infile}.in"
			# Generate sql query
			./"generate_sql_${q}.py" `pwd`/$DATA_PATH ${l} ${k} sysx
			# Run the query
			sqlcmd -y0 -S 127.0.0.1 -U Anyk -P Anyk_pwd -t 4000 -i "sql_queries/${q}_l${l}_k${k}_sysx.sql" 2>> "${OUT_PATH}${infile}_${q}_allk_l${l}_${alg}.out" | grep -A 9999 "SQL Server Execution Times:" >> "${OUT_PATH}${infile}_${q}_allk_l${l}_${alg}.out"       
			# Delete the csv files
			rm ${DATA_PATH}/Edges.csv

			echo "Done with $graph, $q, $alg, l=$l, run $i"
	done
done

# Clean sql server temp files
sqlcmd -y0 -S 127.0.0.1 -U Anyk -P Anyk_pwd -i ../sqlserv_clean.sql  > /dev/null


## Other, All results
l=4
for i in $(seq 1 $ITERS_MEDIUM);
do
	for graph in "friendship" "foodweb"
	do
		for qtype in "path" "star"
		do
			q="QWG_${qtype}"

			# Generate csv files
			./in_to_csv.py "$DATA_PATH${graph}.in"
			# Generate sql query
			./"generate_sql_${q}.py" `pwd`/$DATA_PATH ${l} ${k} sysx ${graph^^}
			# Run the query
			sqlcmd -y0 -S 127.0.0.1 -U Anyk -P Anyk_pwd -t 4000 -i "sql_queries/${q}_l${l}_k${k}_sysx.sql" 2>> "${OUT_PATH}${graph}_${q}_allk_l${l}_${alg}.out" | grep -A 9999 "SQL Server Execution Times:" >> "${OUT_PATH}${graph}_${q}_allk_l${l}_${alg}.out"       
			# Delete the csv files
			rm ${DATA_PATH}/Edges.csv

			echo "Done with $graph, $q, $alg, l=$l, run $i"
		done
	done
done


# Clean sql server temp files
sqlcmd -y0 -S 127.0.0.1 -U Anyk -P Anyk_pwd -i ../sqlserv_clean.sql  > /dev/null