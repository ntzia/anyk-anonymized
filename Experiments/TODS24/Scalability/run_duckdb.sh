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
            MAXIDLIST=("28" "29" "210" "211" "212")
        fi

        for maxid in "${MAXIDLIST[@]}"
        do
            infile=${graph}_sample_${maxid}
            # Generate csv files
            ./in_to_csv.py "$DATA_PATH${infile}.in"
            # Generate sql query
            ./"generate_sql_${q}.py" `pwd`/$DATA_PATH ${l} ${k} duckdb
            # Run the query
            timeout 4000s python sql_queries/${q}_l${l}_k${k}_duckdb.py 2>> "${OUT_PATH}${infile}_${q}_l${l}_k${k}_duckdb.out" >> "${OUT_PATH}${infile}_${q}_l${l}_k${k}_duckdb.out"
            exit_status=$?
            if [[ $exit_status -eq 124 ]]; then
                echo "Query timed out" >> "${OUT_PATH}${infile}_${q}_l${l}_k${k}_duckdb.out"
            fi
            # Delete the csv files
            rm ${DATA_PATH}Edges.csv
        done
        echo "Done with $graph, $q, duckdb, run ${i}"
    done
done


graph=twitter
for i in $(seq 1 $ITERS_FEW);
do
    for q in "QTW1" "QTW2" 
    do
        # QTW1 212 times out
        # QTW2 29 times out
        if [[ $q == "QTW1" ]]; then
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
            ./"generate_sql_${q}.py" `pwd`/$DATA_PATH ${l} ${k} duckdb
            # Run the query
            timeout 4000s python sql_queries/${q}_l${l}_k${k}_duckdb.py 2>> "${OUT_PATH}${infile}_${q}_l${l}_k${k}_duckdb.out" >> "${OUT_PATH}${infile}_${q}_l${l}_k${k}_duckdb.out"
            exit_status=$?
            if [[ $exit_status -eq 124 ]]; then
                echo "Query timed out" >> "${OUT_PATH}${infile}_${q}_l${l}_k${k}_duckdb.out"
            fi
            # Delete the csv files
            rm ${DATA_PATH}Edges.csv
        done
        echo "Done with $graph, $q, duckdb, run ${i}"
    done
done


######## Vary query size
graph=bitcoinotc
k=1000
infile=${graph}_sample_all
for i in $(seq 1 $ITERS_FEW);
do
    for q in "QBC1" "QBC2" 
    do
        if [[ $q == "QBC1" ]]; then
            L_LIST=(2 3 4 5)
        elif [[ $q == "QBC2" ]]; then
            L_LIST=(2 3 4)
        fi

        for l in "${L_LIST[@]}"
        do
            # Generate csv files
            ./in_to_csv.py "$DATA_PATH${infile}.in"
            # Generate sql query
            ./"generate_sql_${q}.py" `pwd`/$DATA_PATH ${l} ${k} duckdb
            # Run the query
            timeout 4000s python sql_queries/${q}_l${l}_k${k}_duckdb.py 2>> "${OUT_PATH}${infile}_${q}_l${l}_k${k}_duckdb.out" >> "${OUT_PATH}${infile}_${q}_l${l}_k${k}_duckdb.out"
            exit_status=$?
            if [[ $exit_status -eq 124 ]]; then
                echo "Query timed out" >> "${OUT_PATH}${infile}_${q}_l${l}_k${k}_duckdb.out"
            fi
            # Delete the csv files
            rm ${DATA_PATH}Edges.csv
        done
        echo "Done with $graph, $q, duckdb, run ${i}"
    done
done


graph=twitter
k=1000
infile=${graph}_large
for i in $(seq 1 $ITERS_FEW);
do
    for q in "QTW1" "QTW2" 
    do
        if [[ $q == "QTW1" ]]; then
            L_LIST=(2 3)
        elif [[ $q == "QTW2" ]]; then
            L_LIST=(2 3)
        fi

        for l in "${L_LIST[@]}"
        do
            # Generate csv files
            ./in_to_csv.py "$DATA_PATH${infile}.in"
            # Generate sql query
            ./"generate_sql_${q}.py" `pwd`/$DATA_PATH ${l} ${k} duckdb
            # Run the query
            timeout 4000s python sql_queries/${q}_l${l}_k${k}_duckdb.py 2>> "${OUT_PATH}${infile}_${q}_l${l}_k${k}_duckdb.out" >> "${OUT_PATH}${infile}_${q}_l${l}_k${k}_duckdb.out"
            exit_status=$?
            if [[ $exit_status -eq 124 ]]; then
                echo "Query timed out" >> "${OUT_PATH}${infile}_${q}_l${l}_k${k}_duckdb.out"
            fi
            # Delete the csv files
            rm ${DATA_PATH}Edges.csv
        done
        echo "Done with $graph, $q, duckdb, run ${i}"
    done
done


######### Vary domain size
k=1000
n=1000000
l=4
DOMDIV_LIST=(1 10 100)
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
            ./"generate_sql_${q}.py" `pwd`/$DATA_PATH ${l} ${k} duckdb
            # Run the query
            timeout 4000s python sql_queries/${q}_l${l}_k${k}_duckdb.py 2>> "${OUT_PATH}synthetic_${q}_n${n}_l${l}_d${d}_duckdb.out" >> "${OUT_PATH}synthetic_${q}_n${n}_l${l}_d${d}_duckdb.out"
            exit_status=$?
            if [[ $exit_status -eq 124 ]]; then
                echo "Query timed out" >> "${OUT_PATH}synthetic_${q}_n${n}_l${l}_d${d}_duckdb.out"
            fi
            # Delete the csv files
            for j in $(seq 1 ${l});
            do
                rm "${DATA_PATH}R${j}.csv"
            done

            echo "Done with synthetic $q, n=$n, d=$d, duckdb, run $i"
        done
    done
done


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
            ./"generate_sql_${q}.py" `pwd`/$DATA_PATH ${l} ${k} duckdb
            # Run the query
            timeout 4000s python sql_queries/${q}_l${l}_k${k}_duckdb.py 2>> "${OUT_PATH}synthetic_gauss_${q}_n${n}_l${l}_std${std_dev}_duckdb.out" >> "${OUT_PATH}synthetic_gauss_${q}_n${n}_l${l}_std${std_dev}_duckdb.out"
            exit_status=$?
            if [[ $exit_status -eq 124 ]]; then
                echo "Query timed out" >> "${OUT_PATH}synthetic_gauss_${q}_n${n}_l${l}_std${std_dev}_duckdb.out"
            fi
            # Delete the csv files
            for j in $(seq 1 ${l});
            do
                rm "${DATA_PATH}R${j}.csv"
            done

            echo "Done with synthetic $q, n=$n, std=$std_dev, duckdb, run $i"
        done
    done
done



######### Cyclic queries, Vary data size
l=6
k=1000
for i in $(seq 1 $ITERS_FEW);
do
    for graph in "bitcoinotc" "twitter"
    do
        if [[ $graph == "bitcoinotc" ]]; then
            MAXIDLIST=("28" "29" "210" "211" "212")
            q=QBC3
        elif [[ $graph == "twitter" ]]; then
            MAXIDLIST=("28" "29" "210" "211")
            q=QTW3
        fi

        for maxid in "${MAXIDLIST[@]}"
        do
            infile=${graph}_sample_${maxid}
            # Generate csv files
            ./in_to_csv.py "$DATA_PATH${infile}.in"
            # Generate sql query
            ./"generate_sql_${q}.py" `pwd`/$DATA_PATH ${l} ${k} duckdb
            # Run the query
            timeout 4000s python sql_queries/${q}_l${l}_k${k}_duckdb.py 2>> "${OUT_PATH}${infile}_${q}_l${l}_k${k}_duckdb.out" >> "${OUT_PATH}${infile}_${q}_l${l}_k${k}_duckdb.out"
            exit_status=$?
            if [[ $exit_status -eq 124 ]]; then
                echo "Query timed out" >> "${OUT_PATH}${infile}_${q}_l${l}_k${k}_duckdb.out"
            fi
            # Delete the csv files
            rm ${DATA_PATH}Edges.csv
        done
        echo "Done with $graph, $q, duckdb, run ${i}"
    done
done


######### Cyclic queries, Vary query size
l=6
k=1000
q=QWG3
for i in $(seq 1 $ITERS_FEW);
do
    for graph in "foodweb" "friendship"
    do
        infile=${graph}
        L_LIST=(4 6 8)

        for l in "${L_LIST[@]}"
        do
            # Generate csv files
            ./in_to_csv.py "$DATA_PATH${infile}.in"
            # Generate sql query
            ./"generate_sql_${q}.py" `pwd`/$DATA_PATH ${l} ${k} duckdb ${graph^^}
            # Run the query
            timeout 4000s python sql_queries/${q}_l${l}_k${k}_duckdb.py 2>> "${OUT_PATH}${infile}_${q}_l${l}_k${k}_duckdb.out" >> "${OUT_PATH}${infile}_${q}_l${l}_k${k}_duckdb.out"
            exit_status=$?
            if [[ $exit_status -eq 124 ]]; then
                echo "Query timed out" >> "${OUT_PATH}${infile}_${q}_l${l}_k${k}_duckdb.out"
            fi
            # Delete the csv files
            rm ${DATA_PATH}Edges.csv
        done
        echo "Done with $graph, $q, duckdb, run ${i}"
    done
done