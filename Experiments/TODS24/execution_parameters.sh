#!/bin/bash

# This controls the memory allocated to the Java VM. 
# Modify according to the RAM of the machine. 
MEM="-Xms100g -Xmx100g"

#-XX:-TieredCompilation -XX:CompileThreshold=100
OTHER_OPTS="-server -XX:+AlwaysPreTouch"
#-Xbatch -XX:+UseSerialGC

# The following turns off garbage collection when set to true
TURNOFFGC=false
if [ "$TURNOFFGC" = true ] ; then
    OTHER_OPTS="$OTHER_OPTS -XX:+UnlockExperimentalVMOptions -XX:+UseEpsilonGC"
fi

# To run the experiments more quickly to see some preliminary results, simply uncomment the line below.
# This will run them for only few iterations and will finish in a couple of hours.
# Note that due to variance, the results will not necessarily be similar to those reported in the paper.

# QUICK=true

# These parameters change the number of iterations that each experiments is repeated.
# The settings below are expected to produce the same results that are reported in the paper.
ITERS_FEW=5
ITERS_MEDIUM=20
ITERS_MANY=600

JAVA_WARMUP_ITERS=0
JAVA_RUN_ITERS=1