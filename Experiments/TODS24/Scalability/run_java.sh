#!/bin/bash

source ../execution_parameters.sh
JAR_PATH="../../../target/any-k-1.0.jar"
DATA_PATH="../Data/"
OUT_PATH="outputs/"
OPTS="$OTHER_OPTS $MEM"

ALG_LIST=("QuickPlus" "YannakakisSorting")


######### Vary data size
graph=bitcoinotc
k=1000
for alg in "${ALG_LIST[@]}"
do
    ## Acyclic
    l=4
    if [ $alg == "BatchSorting" ] || [ $alg == "YannakakisSorting" ]; then
        MAXIDLIST=("28" "29" "210")
        ITERS=$ITERS_FEW
    else
        MAXIDLIST=("28" "29" "210" "211" "212" "all")
        ITERS=$ITERS_MEDIUM
    fi
    for maxid in "${MAXIDLIST[@]}"
    do
        for i in $(seq 1 $ITERS);
        do
            infile=${graph}_sample_${maxid}
            java $OPTS -cp ${JAR_PATH} experiments.Equijoin -q "path" -a $alg -i "${DATA_PATH}${infile}.in" -sj -l $l -k $k -wi $JAVA_WARMUP_ITERS -ri $JAVA_RUN_ITERS >> "${OUT_PATH}${infile}_QBC1_l${l}_${alg}.out"
            echo "Done with $graph, QBC1 (path), $alg, l=$l, maxid=${maxid}, run $i"
            java $OPTS -cp ${JAR_PATH} experiments.Equijoin -q "star" -a $alg -i "${DATA_PATH}${infile}.in" -sj -l $l -k $k -wi $JAVA_WARMUP_ITERS -ri $JAVA_RUN_ITERS >> "${OUT_PATH}${infile}_QBC2_l${l}_${alg}.out"
            echo "Done with $graph, QBC2 (star), $alg, l=$l, maxid=${maxid}, run $i"
        done
    done
    
    ## Cyclic
    l=6
    ITERS=$ITERS_MEDIUM
    if [ $alg == "BatchSorting" ] || [ $alg == "YannakakisSorting" ]; then
        MAXIDLIST=("28" "29" "210" "211" "212" "all")
    else
        MAXIDLIST=("28" "29" "210" "211" "212" "all")
    fi
    for maxid in "${MAXIDLIST[@]}"
    do
        for i in $(seq 1 $ITERS);
        do
            infile=${graph}_sample_${maxid}
            java $OPTS -cp ${JAR_PATH} experiments.Equijoin -q "cycle" -a $alg -i "${DATA_PATH}${infile}.in" -sj -l $l -k $k -wi $JAVA_WARMUP_ITERS -ri $JAVA_RUN_ITERS >> "${OUT_PATH}${infile}_QBC3_l${l}_${alg}.out"
            echo "Done with $graph, QBC3 (cycle), $alg, l=$l, maxid=${maxid}, run $i"
        done
    done
done


k=1000
graph=twitter
for alg in "${ALG_LIST[@]}"
do
    ## Acyclic
    l=4
    if [ $alg == "BatchSorting" ] || [ $alg == "YannakakisSorting" ]; then
        MAXIDLIST=("28" "29" "210")
        ITERS=$ITERS_FEW
    else
        MAXIDLIST=("28" "29" "210" "211" "212" "213" "214" "215" "216" "217")
        ITERS=$ITERS_MEDIUM
    fi
    for maxid in "${MAXIDLIST[@]}"
    do
        for i in $(seq 1 $ITERS);
        do
            infile=${graph}_sample_${maxid}

            java $OPTS -cp ${JAR_PATH} experiments.Equijoin -q "path" -a $alg -i "${DATA_PATH}${infile}.in" -sj -l $l -k $k -wi $JAVA_WARMUP_ITERS -ri $JAVA_RUN_ITERS >> "${OUT_PATH}${infile}_QTW1_l${l}_${alg}.out"
            echo "Done with $graph, QTW1 (path), $alg, l=$l, maxid=${maxid}, run $i"
            java $OPTS -cp ${JAR_PATH} experiments.Equijoin -q "star" -a $alg -i "${DATA_PATH}${infile}.in" -sj -l $l -k $k -wi $JAVA_WARMUP_ITERS -ri $JAVA_RUN_ITERS >> "${OUT_PATH}${infile}_QTW2_l${l}_${alg}.out"
            echo "Done with $graph, QTW2 (star), $alg, l=$l, maxid=${maxid}, run $i"
        done
    done

    ## Cyclic
    l=6
    ITERS=$ITERS_MEDIUM
    if [ $alg == "BatchSorting" ] || [ $alg == "YannakakisSorting" ]; then
        MAXIDLIST=("28" "29" "210" "211" "212" "213")
    else
        #MAXIDLIST=("28" "29" "210" "211" "212" "213" "214" "215" "216")
        MAXIDLIST=("28" "29" "210" "211" "212" "213")
    fi
    for maxid in "${MAXIDLIST[@]}"
    do
        for i in $(seq 1 $ITERS);
        do
            infile=${graph}_sample_${maxid}
            java $OPTS -cp ${JAR_PATH} experiments.Equijoin -q "cycle" -a $alg -i "${DATA_PATH}${infile}.in" -sj -l $l -k $k -wi $JAVA_WARMUP_ITERS -ri $JAVA_RUN_ITERS >> "${OUT_PATH}${infile}_QTW3_l${l}_${alg}.out"
            echo "Done with $graph, QTW3 (cycle), $alg, l=$l, maxid=${maxid}, run $i"
        done
    done
done


######### Vary query size

graph=bitcoinotc
k=1000
infile=${graph}_sample_all
for alg in "${ALG_LIST[@]}"
do
    ## Acyclic
    if [ $alg == "BatchSorting" ] || [ $alg == "YannakakisSorting" ]; then
        L_LIST=(2 3 4)
        ITERS=$ITERS_FEW
    else
        L_LIST=(2 3 4 5 6 7 8 9 10)
        ITERS=$ITERS_MEDIUM
    fi
    for l in "${L_LIST[@]}"
    do
        for i in $(seq 1 $ITERS);
        do
            java $OPTS -cp ${JAR_PATH} experiments.Equijoin -q "path" -a $alg -i "${DATA_PATH}${infile}.in" -sj -l $l -k $k -wi $JAVA_WARMUP_ITERS -ri $JAVA_RUN_ITERS >> "${OUT_PATH}${infile}_QBC1_l${l}_${alg}.out"
            echo "Done with $graph, QBC1 (path), $alg, l=$l, run $i"
            java $OPTS -cp ${JAR_PATH} experiments.Equijoin -q "star" -a $alg -i "${DATA_PATH}${infile}.in" -sj -l $l -k $k -wi $JAVA_WARMUP_ITERS -ri $JAVA_RUN_ITERS >> "${OUT_PATH}${infile}_QBC2_l${l}_${alg}.out"
            echo "Done with $graph, QBC2 (star), $alg, l=$l, run $i"
        done
    done

    ## Cyclic
    ITERS=$ITERS_MEDIUM
    L_LIST=(4 6 8 10)
    for l in "${L_LIST[@]}"
    do
        for i in $(seq 1 $ITERS);
        do
            java $OPTS -cp ${JAR_PATH} experiments.Equijoin -q "cycle" -a $alg -i "${DATA_PATH}${infile}.in" -sj -l $l -k $k -wi $JAVA_WARMUP_ITERS -ri $JAVA_RUN_ITERS >> "${OUT_PATH}${infile}_QBC3_l${l}_${alg}.out"
            echo "Done with $graph, QBC3 (cycle), $alg, l=$l, run $i"
        done
    done
done



graph=twitter
infile=${graph}_large
for alg in "${ALG_LIST[@]}"
do
    ## Acyclic
    if [ $alg == "BatchSorting" ] || [ $alg == "YannakakisSorting" ]; then
        L_LIST=(2)
        ITERS=$ITERS_FEW
    else
        L_LIST=(2 3 4 5 6 7 8 9 10)
        ITERS=$ITERS_MEDIUM
    fi
    for l in "${L_LIST[@]}"
    do
        for i in $(seq 1 $ITERS);
        do
            java $OPTS -cp ${JAR_PATH} experiments.Equijoin -q "path" -a $alg -i "${DATA_PATH}${infile}.in" -sj -l $l -k $k -wi $JAVA_WARMUP_ITERS -ri $JAVA_RUN_ITERS >> "${OUT_PATH}${infile}_QTW1_l${l}_${alg}.out"
            echo "Done with $graph, QTW1 (path), $alg, l=$l, run $i"
            java $OPTS -cp ${JAR_PATH} experiments.Equijoin -q "star" -a $alg -i "${DATA_PATH}${infile}.in" -sj -l $l -k $k -wi $JAVA_WARMUP_ITERS -ri $JAVA_RUN_ITERS >> "${OUT_PATH}${infile}_QTW2_l${l}_${alg}.out"
            echo "Done with $graph, QTW2 (star), $alg, l=$l, run $i"
        done
    done

    ## Cyclic
    ITERS=$ITERS_MEDIUM
    L_LIST=(4 6 8 10)
    for l in "${L_LIST[@]}"
    do
        for i in $(seq 1 $ITERS);
        do
            java $OPTS -cp ${JAR_PATH} experiments.Equijoin -q "cycle" -a $alg -i "${DATA_PATH}${infile}.in" -sj -l $l -k $k -wi $JAVA_WARMUP_ITERS -ri $JAVA_RUN_ITERS >> "${OUT_PATH}${infile}_QTW3_l${l}_${alg}.out"
            echo "Done with $graph, QTW3 (cycle), $alg, l=$l, run $i"
        done
    done
done


######## Vary domain size

k=1000
for alg in "${ALG_LIST[@]}"
do
    # l=4
    # n=1000000
    # if [ $alg == "BatchSorting" ] || [ $alg == "YannakakisSorting" ]; then
    #     DOMDIV_LIST=(1 10)
    #     ITERS=$ITERS_FEW
    # else
    #     DOMDIV_LIST=(1 10 100 1000)
    #     ITERS=$ITERS_MEDIUM
    # fi

    # for q in "path" "star"
    # do
    #     for dom_div in "${DOMDIV_LIST[@]}"
    #     do
    #         d=$((${n}/${dom_div}))
    #         # Create the input if it doesn't exist
    #         INPUT="${DATA_PATH}${q}_n${n}_l${l}_d${d}.in"
    #         if [ ! -f $INPUT ]; then
    #             java -cp ${JAR_PATH} data.BinaryRandomPattern -q $q -n $n -l $l -dom $d -o $INPUT
    #         fi 

    #         for i in $(seq 1 $ITERS);
    #         do
    #             java $OPTS -cp ${JAR_PATH} experiments.Equijoin -q $q -a $alg -i $INPUT -k $k -l $l -wi $JAVA_WARMUP_ITERS -ri $JAVA_RUN_ITERS >> "${OUT_PATH}synthetic_${q}_n${n}_l${l}_d${d}_${alg}.out"
    #             echo "Done with synthetic uniform $q, n=$n, d=$d, $alg, run $i"
    #         done
    #     done
    # done

    ## Cyclic
    n=100000
    if [ $alg == "BatchSorting" ] || [ $alg == "YannakakisSorting" ]; then
        DOMDIV_LIST=(1 2 4 8 16 32)
        ITERS=$ITERS_FEW
    else
        DOMDIV_LIST=(1 2 4 8 16 32)
        ITERS=$ITERS_MEDIUM
    fi
    q="cycle"
    l=6
    for dom_div in "${DOMDIV_LIST[@]}"
    do
        d=$((${n}/${dom_div}))
        # Create the input if it doesn't exist
        INPUT="${DATA_PATH}${q}_n${n}_l${l}_d${d}.in"
        if [ ! -f $INPUT ]; then
            java -cp ${JAR_PATH} data.BinaryRandomPattern -q $q -n $n -l $l -dom $d -o $INPUT
        fi 

        for i in $(seq 1 $ITERS);
        do
            java $OPTS -cp ${JAR_PATH} experiments.Equijoin -q $q -a $alg -i $INPUT -l $l -k $k -wi $JAVA_WARMUP_ITERS -ri $JAVA_RUN_ITERS >> "${OUT_PATH}synthetic_${q}_n${n}_l${l}_d${d}_${alg}.out"
            echo "Done with synthetic uniform $q, n=$n, d=$d, $alg, run $i"
        done
    done
done


######### Vary join pattern

k=1000
for alg in "${ALG_LIST[@]}"
do
    l=4
    n=1000000
    if [ $alg == "BatchSorting" ] || [ $alg == "YannakakisSorting" ]; then
        STDDEV_LIST=(1000 10000 100000 1000000)
        ITERS=$ITERS_FEW
    else
        STDDEV_LIST=(1000 10000 100000 1000000)
        ITERS=$ITERS_MEDIUM
    fi

    # for q in "path" "star"
    # do
    #     for std_dev in "${STDDEV_LIST[@]}"
    #     do
    #         # Create the input if it doesn't exist
    #         INPUT="${DATA_PATH}${q}_gauss_n${n}_l${l}_std${std_dev}.in"
    #         if [ ! -f $INPUT ]; then
    #             java -cp ${JAR_PATH} data.BinaryGaussPattern -q $q -n $n -l $l -std $std_dev -o $INPUT
    #         fi 

    #         for i in $(seq 1 $ITERS);
    #         do
    #             java $OPTS -cp ${JAR_PATH} experiments.Equijoin -q $q -a $alg -i $INPUT -k $k -l $l -wi $JAVA_WARMUP_ITERS -ri $JAVA_RUN_ITERS >> "${OUT_PATH}synthetic_gauss_${q}_n${n}_l${l}_std${std_dev}_${alg}.out"
    #             echo "Done with synthetic gauss $q, n=$n, std=$std_dev, $alg, run $i"
    #         done
    #     done
    # done

    ## Cyclic
    q="cycle"
    l=6
    n=100000
    if [ $alg == "BatchSorting" ] || [ $alg == "YannakakisSorting" ]; then
        STDDEV_LIST=(3125 6250 12500 25000 50000 100000)
        ITERS=$ITERS_FEW
    else
        STDDEV_LIST=(3125 6250 12500 25000 50000 100000)
        ITERS=$ITERS_MEDIUM
    fi
    for std_dev in "${STDDEV_LIST[@]}"
    do
        # Create the input if it doesn't exist
        INPUT="${DATA_PATH}${q}_gauss_n${n}_l${l}_std${std_dev}.in"
        if [ ! -f $INPUT ]; then
            java -cp ${JAR_PATH} data.BinaryGaussPattern -q $q -n $n -l $l -std $std_dev -o $INPUT
        fi 

        for i in $(seq 1 $ITERS);
        do
            java $OPTS -cp ${JAR_PATH} experiments.Equijoin -q $q -a $alg -i $INPUT -l $l -k $k -wi $JAVA_WARMUP_ITERS -ri $JAVA_RUN_ITERS >> "${OUT_PATH}synthetic_gauss_${q}_n${n}_l${l}_std${std_dev}_${alg}.out"
            echo "Done with synthetic gauss $q, n=$n, std=$std_dev, $alg, run $i"
        done
    done
done


######### Single instance runs for cyclic
for l in 8 10
do
    k=1000
    for graph in friendship foodweb
    do
        for alg in "${ALG_LIST[@]}"
        do
            ITERS=$ITERS_MEDIUM
            for i in $(seq 1 $ITERS);
            do
                infile=${graph}
                java $OPTS -cp ${JAR_PATH} experiments.Equijoin -q "cycle" -a $alg -i "${DATA_PATH}${infile}.in" -sj -l $l -k $k -wi $JAVA_WARMUP_ITERS -ri $JAVA_RUN_ITERS >> "${OUT_PATH}${infile}_QWG3_l${l}_${alg}.out"
                echo "Done with $graph, QWG3 (cycle), $alg, l=$l, run $i"
            done
        done
    done
done