#!/bin/bash

OUT_PATH="outputs/"
# ALG_LIST=("QuickPlus" "BatchSorting" "psql" "sysx") 
ALG_LIST=("QuickPlus" "YannakakisSorting" "psql" "sysx" "duckdb") 

## Add -p for creating step-by-step presentation figures

## Cyclic Queries
l=6
k=1000
q="QBC3"
maxid_exp_list=(28 29 210 211 212 all)
./plot_increasing_data.py -a "${ALG_LIST[@]}" -mid "${maxid_exp_list[@]}" -q $q -l $l -i "${OUT_PATH}bitcoinotc_sample" -k $k -o "plots/${q}_l${l}" -t "${q}, l=${l}"
q="QTW3"
maxid_exp_list=("28" "29" "210" "211" "212" "213")
./plot_increasing_data.py -a "${ALG_LIST[@]}" -mid "${maxid_exp_list[@]}" -q $q -l $l -i "${OUT_PATH}twitter_sample" -k $k -o "plots/${q}_l${l}" -t "${q}, l=${l}"

l_list=(4 6 8 10)
q="QWG3"
./plot_increasing_query.py -a "${ALG_LIST[@]}" -l "${l_list[@]}" -q $q -i "${OUT_PATH}friendship" -k $k -o "plots/friendship_${q}" -t "friendship_${q}"
./plot_increasing_query.py -a "${ALG_LIST[@]}" -l "${l_list[@]}" -q $q -i "${OUT_PATH}foodweb" -k $k -o "plots/foodweb_${q}" -t "foodweb_${q}"




# ## Increasing Data
# l=4
# k=1000
# maxid_exp_list=(28 29 210 211 212 all)
# q="QBC1"
# ./plot_increasing_data.py -a "${ALG_LIST[@]}" -mid "${maxid_exp_list[@]}" -q $q -l $l -i "${OUT_PATH}bitcoinotc_sample" -k $k -o "plots/${q}_l${l}" -t "${q}, l=${l}"
# q="QBC2"
# ./plot_increasing_data.py -a "${ALG_LIST[@]}" -mid "${maxid_exp_list[@]}" -q $q -l $l -i "${OUT_PATH}bitcoinotc_sample" -k $k -o "plots/${q}_l${l}" -t "${q}, l=${l}"
# maxid_exp_list=("28" "29" "210" "211" "212" "213" "214" "215" "216" "217")
# q="QTW1"
# ./plot_increasing_data.py -a "${ALG_LIST[@]}" -mid "${maxid_exp_list[@]}" -q $q -l $l -i "${OUT_PATH}twitter_sample" -k $k -o "plots/${q}_l${l}" -t "${q}, l=${l}"
# q="QTW2"
# ./plot_increasing_data.py -a "${ALG_LIST[@]}" -mid "${maxid_exp_list[@]}" -q $q -l $l -i "${OUT_PATH}twitter_sample" -k $k -o "plots/${q}_l${l}" -t "${q}, l=${l}"



# ## Increasing Query Size
# k=1000
# l_list=(2 3 4 5 6 7 8 9 10)
# q="QBC1"
# ./plot_increasing_query.py -a "${ALG_LIST[@]}" -l "${l_list[@]}" -q $q -i "${OUT_PATH}bitcoinotc_sample_all" -k $k -o "plots/${q}" -t "${q}"
# q="QBC2"
# ./plot_increasing_query.py -a "${ALG_LIST[@]}" -l "${l_list[@]}" -q $q -i "${OUT_PATH}bitcoinotc_sample_all" -k $k -o "plots/${q}" -t "${q}"
# q="QTW1"
# ./plot_increasing_query.py -a "${ALG_LIST[@]}" -l "${l_list[@]}" -q $q -i "${OUT_PATH}twitter_large" -k $k -o "plots/${q}" -t "${q}"
# q="QTW2"
# ./plot_increasing_query.py -a "${ALG_LIST[@]}" -l "${l_list[@]}" -q $q -i "${OUT_PATH}twitter_large" -k $k -o "plots/${q}" -t "${q}"


# ## Varying Domain Size
# k=1000
# n=1000000
# l=4
# dom_list=(1000000 100000 10000 1000)
# x_axis_labels=(n n/10 n/100 n/1000)
# q="path"
# ./plot_increasing_domain.py -a "${ALG_LIST[@]}" -d "${dom_list[@]}" -x "${x_axis_labels[@]}" -n $n -l $l -q $q -i "${OUT_PATH}synthetic_${q}_n${n}_l${l}" -k $k -o "plots/${q}_n${n}_l${l}" -t "${q}"
# q="star"
# ./plot_increasing_domain.py -a "${ALG_LIST[@]}" -d "${dom_list[@]}" -x "${x_axis_labels[@]}" -n $n -l $l -q $q -i "${OUT_PATH}synthetic_${q}_n${n}_l${l}" -k $k -o "plots/${q}_n${n}_l${l}" -t "${q}"



# ## Varying Standard Deviation (Gauss)
# k=1000
# n=1000000
# l=4
# std_list=(1000000 100000 10000 1000)
# x_axis_labels=(n n/10 n/100 n/1000)
# q="path"
# ./plot_increasing_std.py -a "${ALG_LIST[@]}" -std "${std_list[@]}" -x "${x_axis_labels[@]}" -n $n -l $l -q $q -i "${OUT_PATH}synthetic_gauss_${q}_n${n}_l${l}" -k $k -o "plots/gauss_${q}_n${n}_l${l}" -t "${q}"
# q="star"
# ./plot_increasing_std.py -a "${ALG_LIST[@]}" -std "${std_list[@]}" -x "${x_axis_labels[@]}" -n $n -l $l -q $q -i "${OUT_PATH}synthetic_gauss_${q}_n${n}_l${l}" -k $k -o "plots/gauss_${q}_n${n}_l${l}" -t "${q}"