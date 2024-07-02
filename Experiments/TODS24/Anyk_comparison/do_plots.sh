#!/bin/bash

# All results Synthetic
ALG_LIST=("Recursive" "Quick" "QuickPlus" "YannakakisSorting" "psql" "sysx" "duckdb")

# for params in "3 100000" "4 10000" "5 1000"  "6 100"
# do
# 	set -- $params # convert the "tuple" into the param args $1 $2...
#     l=$1
# 	n=$2
# 	d=$((n / 10))
#     for q in "path" "star" "one_branch"
#     do
#         ./plot.py -a "${ALG_LIST[@]}" -i "outputs/synthetic_${q}_n${n}_l${l}_d${d}" -o "plots/synthetic_allk_${q}_n${n}_l${l}_d${d}" -t "Synthetic allk $q n=$n l=$l" -l $l
#     done
# done

# All results Real
# ./plot.py -a "${ALG_LIST[@]}" -i "outputs/bitcoinotc_sample_210_path_allk_l4" -o "plots/bitcoin210_allk_path_l4" -t "Bitcoin allk path" -l 4
# ./plot.py -a "${ALG_LIST[@]}" -i "outputs/bitcoinotc_sample_26_path_allk_l6" -o "plots/bitcoin26_allk_path_l6" -t "Bitcoin allk path" -l 6

# ./plot.py -a "${ALG_LIST[@]}" -i "outputs/twitter_sample_210_path_allk_l3" -o "plots/twitter210_allk_path_l3" -t "Twitter allk path" -l 3
# ./plot.py -a "${ALG_LIST[@]}" -i "outputs/twitter_sample_211_path_allk_l3" -o "plots/twitter211_allk_path_l3" -t "Twitter allk path" -l 3
# ./plot.py -a "${ALG_LIST[@]}" -i "outputs/twitter_sample_28_path_allk_l4" -o "plots/twitter28_allk_path_l4" -t "Twitter allk path" -l 4
# ./plot.py -a "${ALG_LIST[@]}" -i "outputs/twitter_sample_29_path_allk_l4" -o "plots/twitter29_allk_path_l4" -t "Twitter allk path" -l 4
# ./plot.py -a "${ALG_LIST[@]}" -i "outputs/twitter_sample_27_path_allk_l6" -o "plots/twitter27_allk_path_l6" -t "Twitter allk path" -l 6

# for q in "path" "star"
# do
#     for l in 4 #3 5 6
#     do
#         ./plot.py -a "${ALG_LIST[@]}" -i "outputs/friendship_${q}_allk_l${l}" -o "plots/friendship_${q}_allk_l${l}" -t "Friendship allk ${l}-${q}" -l ${l}
#     done
#     for l in 4 #3 4 5
#     do
#         ./plot.py -a "${ALG_LIST[@]}" -i "outputs/foodweb_${q}_allk_l${l}" -o "plots/foodweb_${q}_allk_l${l}" -t "Foodweb allk ${l}-${q}" -l ${l}
#     done
# done

## Paths (few results)
ALG_LIST=("Recursive" "Quick" "QuickPlus")
for q in "path" "star"
do
    for l in 4 6
    do 
        ./plot.py -a "${ALG_LIST[@]}" -i "outputs/bitcoinotc_${q}_fewk_l${l}" -o "plots/bitcoinotc_${q}_fewk_l${l}" -t "${l}-${q} Bitcoin few answers" -l $l
        ./plot.py -a "${ALG_LIST[@]}" -i "outputs/twitter_sample_217_${q}_fewk_l${l}" -o "plots/twitter_sample_217_${q}_fewk_l${l}" -t "${l}-${q} Twitter few answers" -l $l
    done
done

