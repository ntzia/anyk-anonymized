#!/bin/bash

source ../execution_parameters.sh
DATA_PATH="../Data/"
OUT_PATH="outputs/"

######### Vary data size
graph=bitcoinotc
l=4
k=1000
for i in $(seq 1 $ITERS_FEW);
do
	for q in "QBC1" "QBC2"
	do
		if [[ $q == "QBC1" ]]; then
			MAXIDLIST=("28" "29" "210" "211" "212" "all")
		elif [[ $q == "QBC2" ]]; then
			# 212 is ~6300 sec
			MAXIDLIST=("28" "29" "210" "211")
		fi
		
		for maxid in "${MAXIDLIST[@]}"
		do
			infile=${graph}_sample_${maxid}
			# Generate csv files
			./in_to_csv.py "$DATA_PATH${infile}.in"
			# Generate sql query
			./"generate_sql_${q}.py" `pwd`/$DATA_PATH ${l} ${k} sysx
			# Run the query
			sqlcmd -y0 -S 127.0.0.1 -U Anyk -P Anyk_pwd -t 4000 -i "sql_queries/${q}_l${l}_k${k}_sysx.sql" 2>> "${OUT_PATH}${infile}_${q}_l${l}_k${k}_sysx.out" | grep -A 9999 "SQL Server Execution Times:" >> "${OUT_PATH}${infile}_${q}_l${l}_k${k}_sysx.out"        
			# Delete the csv files
			rm ${DATA_PATH}/Edges.csv
		done
		echo "Done with $graph, $q, sysx, run ${i}"
	done
done


graph=twitter
for i in $(seq 1 $ITERS_FEW);
do
	for q in "QTW1" "QTW2"
	do
		if [[ $q == "QTW1" ]]; then
			# 213 needs 23k seconds
			MAXIDLIST=("28" "29" "210" "211" "212")
		elif [[ $q == "QTW2" ]]; then
			MAXIDLIST=("28" "29" "210")
		fi

		for maxid in "${MAXIDLIST[@]}"
		do
			infile=${graph}_sample_${maxid}

			# Generate csv files
			./in_to_csv.py "$DATA_PATH${infile}.in"
			# Generate sql query
			./"generate_sql_${q}.py" `pwd`/$DATA_PATH ${l} ${k} sysx
			# Run the query
			sqlcmd -y0 -S 127.0.0.1 -U Anyk -P Anyk_pwd -t 4000 -i "sql_queries/${q}_l${l}_k${k}_sysx.sql" 2>> "${OUT_PATH}${infile}_${q}_l${l}_k${k}_sysx.out" | grep -A 9999 "SQL Server Execution Times:" >> "${OUT_PATH}${infile}_${q}_l${l}_k${k}_sysx.out"        
			# Delete the csv files
			rm ${DATA_PATH}/Edges.csv
		done
		echo "Done with $graph, $q, sysx, run ${i}"
	done
done

# Clean sql server temp files
sqlcmd -y0 -S 127.0.0.1 -U Anyk -P Anyk_pwd -i ../sqlserv_clean.sql  > /dev/null


######### Vary query size
graph=bitcoinotc
k=1000
infile=${graph}_sample_all
for i in $(seq 1 $ITERS_FEW);
do
	for q in "QBC1" "QBC2"
	do
        if [[ $q == "QBC1" ]]; then
            L_LIST=(2 3)
        elif [[ $q == "QBC2" ]]; then
            L_LIST=(2 3)
        fi
		
		for l in "${L_LIST[@]}"
		do
			# Generate csv files
			./in_to_csv.py "$DATA_PATH${infile}.in"
			# Generate sql query
			./"generate_sql_${q}.py" `pwd`/$DATA_PATH ${l} ${k} sysx
			# Run the query
			sqlcmd -y0 -S 127.0.0.1 -U Anyk -P Anyk_pwd -t 4000 -i "sql_queries/${q}_l${l}_k${k}_sysx.sql" 2>> "${OUT_PATH}${infile}_${q}_l${l}_k${k}_sysx.out" | grep -A 9999 "SQL Server Execution Times:" >> "${OUT_PATH}${infile}_${q}_l${l}_k${k}_sysx.out"        
			# Delete the csv files
			rm ${DATA_PATH}/Edges.csv
		done
		echo "Done with $graph, $q, sysx, run ${i}"
	done
done


graph=twitter
l=4
k=1000
infile=${graph}_large
for i in $(seq 1 $ITERS_FEW);
do
	for q in "QTW1" "QTW2"
	do
        if [[ $q == "QTW1" ]]; then
            L_LIST=(2 3)
			# l=3 takes more than a day
        elif [[ $q == "QTW2" ]]; then
            L_LIST=(2 3)
        fi
		
		for l in "${L_LIST[@]}"
		do
			# Generate csv files
			./in_to_csv.py "$DATA_PATH${infile}.in"
			# Generate sql query
			./"generate_sql_${q}.py" `pwd`/$DATA_PATH ${l} ${k} sysx
			# Run the query
			sqlcmd -y0 -S 127.0.0.1 -U Anyk -P Anyk_pwd -t 4000 -i "sql_queries/${q}_l${l}_k${k}_sysx.sql" 2>> "${OUT_PATH}${infile}_${q}_l${l}_k${k}_sysx.out" | grep -A 9999 "SQL Server Execution Times:" >> "${OUT_PATH}${infile}_${q}_l${l}_k${k}_sysx.out"
			# Delete the csv files
			rm ${DATA_PATH}/Edges.csv
		done
		echo "Done with $graph, $q, sysx, run ${i}"
	done
done

# Clean sql server temp files
sqlcmd -y0 -S 127.0.0.1 -U Anyk -P Anyk_pwd -i ../sqlserv_clean.sql  > /dev/null


######### Vary domain size
k=1000
n=1000000
l=4
# DOMDIV_LIST=(1 10)
DOMDIV_LIST=(100)
for i in $(seq 1 $ITERS_FEW);
do
    for q in "path" "star"
    do
        for dom_div in "${DOMDIV_LIST[@]}"
        do
            d=$((${n}/${dom_div}))
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
			sqlcmd -y0 -S 127.0.0.1 -U Anyk -P Anyk_pwd -t 4000 -i "sql_queries/${q}_l${l}_k${k}_sysx.sql" 2>> "${OUT_PATH}synthetic_${q}_n${n}_l${l}_d${d}_sysx.out" | grep -A 9999 "SQL Server Execution Times:" >> "${OUT_PATH}synthetic_${q}_n${n}_l${l}_d${d}_sysx.out"
            # Delete the csv files
            for j in $(seq 1 ${l});
            do
                rm "${DATA_PATH}R${j}.csv"
            done

            echo "Done with synthetic $q, n=$n, d=$d, sysx, run $i"
        done
    done
done

# Clean sql server temp files
sqlcmd -y0 -S 127.0.0.1 -U Anyk -P Anyk_pwd -i ../sqlserv_clean.sql  > /dev/null


######### Vary join pattern
k=1000
n=1000000
l=4
#STDDEV_LIST=(1000 10000 100000 1000000)
STDDEV_LIST=(1000000 100000 10000)
for i in $(seq 1 $ITERS_FEW);
do
    for q in "path" "star"
    do
        for std_dev in "${STDDEV_LIST[@]}"
        do
            # Create the input if it doesn't exist
            INPUT="${DATA_PATH}${q}_gauss_n${n}_l${l}_std${std_dev}.in"
            if [ ! -f $INPUT ]; then
                java -cp ${JAR_PATH} data.BinaryGaussPattern -q $q -n $n -l $l -std $std_dev -o $INPUT
            fi 

            # Generate csv files
            ./in_to_csv.py $INPUT
            # Generate sql query
            ./"generate_sql_${q}.py" `pwd`/$DATA_PATH ${l} ${k} sysx
            # Run the query
			sqlcmd -y0 -S 127.0.0.1 -U Anyk -P Anyk_pwd -t 4000 -i "sql_queries/${q}_l${l}_k${k}_sysx.sql" 2>> "${OUT_PATH}synthetic_gauss_${q}_n${n}_l${l}_std${std_dev}_sysx.out" | grep -A 9999 "SQL Server Execution Times:" >> "${OUT_PATH}synthetic_gauss_${q}_n${n}_l${l}_std${std_dev}_sysx.out"
            # Delete the csv files
            for j in $(seq 1 ${l});
            do
                rm "${DATA_PATH}R${j}.csv"
            done

            echo "Done with synthetic $q, n=$n, std=$std_dev, sysx, run $i"
        done
    done
done

# Clean sql server temp files
sqlcmd -y0 -S 127.0.0.1 -U Anyk -P Anyk_pwd -i ../sqlserv_clean.sql  > /dev/null


######### Cyclic queries, Vary data size
l=6
k=1000
for i in $(seq 1 $ITERS_FEW);
do
    for graph in "bitcoinotc" "twitter"
    do
        if [[ $graph == "bitcoinotc" ]]; then
            MAXIDLIST=("28" "29" "210") #211 exceeds time limit
            q=QBC3
        elif [[ $graph == "twitter" ]]; then
            MAXIDLIST=("28" "29" "210") #211 exceeds time limit (210 close to 1h)
            q=QTW3
        fi

		for maxid in "${MAXIDLIST[@]}"
		do
			infile=${graph}_sample_${maxid}
			# Generate csv files
			./in_to_csv.py "$DATA_PATH${infile}.in"
			# Generate sql query
			./"generate_sql_${q}.py" `pwd`/$DATA_PATH ${l} ${k} sysx
			# Run the query
			sqlcmd -y0 -S 127.0.0.1 -U Anyk -P Anyk_pwd -t 4000 -i "sql_queries/${q}_l${l}_k${k}_sysx.sql" 2>> "${OUT_PATH}${infile}_${q}_l${l}_k${k}_sysx.out" | grep -A 9999 "SQL Server Execution Times:" >> "${OUT_PATH}${infile}_${q}_l${l}_k${k}_sysx.out"        
			# Delete the csv files
			rm ${DATA_PATH}/Edges.csv
		done
		echo "Done with $graph, $q, sysx, run ${i}"
    done
done

# Clean sql server temp files
sqlcmd -y0 -S 127.0.0.1 -U Anyk -P Anyk_pwd -i ../sqlserv_clean.sql  > /dev/null

######### Cyclic queries, Vary query size
l=6
k=1000
q=QWG3
for i in $(seq 1 $ITERS_FEW);
do
    for graph in "foodweb" "friendship"
    do
        infile=${graph}
        L_LIST=(4 6 8 10)

		for l in "${L_LIST[@]}"
		do
			# Generate csv files
			./in_to_csv.py "$DATA_PATH${infile}.in"
			# Generate sql query
			./"generate_sql_${q}.py" `pwd`/$DATA_PATH ${l} ${k} sysx ${graph^^}
			# Run the query
			sqlcmd -y0 -S 127.0.0.1 -U Anyk -P Anyk_pwd -t 4000 -i "sql_queries/${q}_l${l}_k${k}_sysx.sql" 2>> "${OUT_PATH}${infile}_${q}_l${l}_k${k}_sysx.out" | grep -A 9999 "SQL Server Execution Times:" >> "${OUT_PATH}${infile}_${q}_l${l}_k${k}_sysx.out"        
			# Delete the csv files
			rm ${DATA_PATH}/Edges.csv
		done
		echo "Done with $graph, $q, sysx, run ${i}"
    done
done