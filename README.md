# Any-k: Ranked enumeration for join queries


This repo provides an implementation of the any-k framework for ranked enumeration of the answers to a join query over a relational database.
More generally, the code can easily be extended to obtain ranked enumeration for any problem solvable via Dynamic Programming.


## Programming Language and Dependencies
The source code is written in Java. The current version is tested on version 11. To install it in a Debian/Ubuntu system, you can use:
```
sudo apt-get update
sudo apt-get install openjdk-11-jdk
export JAVA_HOME=path_to_java_home
```
The project compiles with the [Maven](https://maven.apache.org/index.html) package manager.
To run the bundled experiments, several scripts need a working version of Python 2. We recommend using [Anaconda](https://docs.anaconda.com/anaconda/install/) to create an environment with all the required packages in [`Experiments/environment.yml`](/Experiments/environment.yml):
```
conda env create -f Experiments/environment.yml
conda activate anyk_env
```


## Compilation
To compile, navigate to the root directory of the project and run:
```
mvn package
```
Successful comilation will produce a jar file in `/target/` from which classes that implement a `main` function can be executed, e.g.,
```
java -cp target/any-k-1.0.jar entities.paths.DP_Path_Equijoin_Instance
```



## Running on your own Queries and Data
Use the `MainEntryPoint` class to run on your own queries and data. See [examples/](/examples) for some helpful examples.
The query is specified as a join tree (in json format) where each joining relation can
refer to the same input file (a self-join) or a different file.
The execution can be parameterized by the following set of parameters,
provided in a different json file, or via the command line (has priority).

- `result_output_file`:  Path to file where the output tuples will be written. You can leave it empty if you only want to time the program.

- `timings_output_file`:  Path to file where timing information will be recorded. You can also leave it empty.

- `algorithm`: Has to be one of "Eager", "All", "Take2", "Lazy", "Quick", "QuickPlus", "Recursive", "BatchSorting", "Batch", "Yannakakis", "YannakakisSorting", "Count".

- `max_k`: Maximum number of output tuples to be produced.

- `weight_cutoff`: Instead of `max_k`, you can use this to stop the enumeration after a certain weight is exceeded in the output.

- `timing_frequency`: Useful if the query produces many answers and you want to restrict the number of timing measurements. If set to a number x, then time will only be recorded every x answers returned.

- `timing_measurements`: Similar to `timing_frequency`, but specifies the number of measurements instead. Has to be used in conjunction with `estimated_result_size`. Has lower priority than `timing_frequency`.

- `estimated_result_size`: An estimate for the number of query answers. Used to calculate `timing_frequency` if `timing_measurements` is used.

- `factorization_method`: This is only relevant for queries with inequality join conditions and controls the technique for handling those. Has to be one of "binary_part", "multi_part", "shared_ranges".

- `path_optimization`: If the query specified in the json file has a path structure, then turning this on may boost performance.

## Synthetic data generator

The produced jar contains a generator for synthetic data in the `data/` package. 
It creates ternary relations of size $n$, where the first two columns are intended for joins, while the third column encodes tuple weight.
The tuples of every relation are always distinct.
We parameterize our generator across three dimensions.
- We generate different join distributions by controlling the values that populate the first two columns. 
  - For a Uniform distribution, we draw integers in $[0 \ldots d]$ uniformly at random with replacement for some given value $d$, which defaults to $n / 10$.
  - For a Gaussian distribution, we round to integers the values drawn with a mean of $0$ and a given standard deviation, which defaults to $n / 10$.

- We generate different weight distributions.
  - For a Uniform distribution, we draw real numbers from $[0, w)$ where $w$ defaults to $10^4$.
  - For a Gaussian distribution, we take as input the mean and the standard deviation, which default to $0$ and $1$ respectively.
  - For a Lexicographic distribution, we ensure that the tuples of the first relation are always prioritized in the ranking and in the case of ties,
  the same happens with tuples of the second relation, and so on.

- We generate different query patterns by changing the names of the columns, assuming that two columns join if and only if they have the same name.
    Our generator supports path, star, and simple cycle patterns.

Example usage:

    java -cp target/any-k-1.0.jar data.BinaryRandomPattern -q "path" -n 200 -l 3 -dom 100 -w uniform -o Synthetic_data/inputs/example.in

The above will create a 3-path instance with 3 binary relations of size 200, drawn uniformly at random from a domain of size 100 and weights also drawn uniformly. The input file will be saved in `Synthetic_data/inputs/` (the directory needs to be created beforehand). 

To instead create a 4-star pattern with Gaussian domain values and a lexicographic ranking:

    java -cp target/any-k-1.0.jar data.BinaryGaussPattern -q "star" -n 200 -l 4 -w lex -o Synthetic_data/inputs/example.in

By default, the relations are all written in the same file, in a format used by some classes under `experiments`.
If instead you want to create a different file per relation use the `-mf` flag.
This will also remove headers and footers.

    java -cp target/any-k-1.0.jar data.BinaryRandomPattern -q "path" -n 200 -l 3 -dom 100 -w uniform -o example.csv -mf

The above will produce 3 different files: `example_1.in`, `example_2.csv`, `example_3.csv`


## Implementation Details

Directory `doc/` contains documentation of classes and methods generated by Javadoc in HTML format. 

The code is written in a way such that it is very easily extendable to other Dynamic Programming (DP) problems, making them any-k. This is done by extending the classes found in `paths/` packages. Specifically, the abstract class `DP_Problem_Instance` can be instantiated for "your own" DP problem by specifying how the bottom-up phase looks like. Then the rest of the code solves ranked enumeration for the problem. For DP problems that have a tree structure (Tree-DP), such as acyclic CQs, this is done with the `trees/` packages. For cyclic queries, `cycles/` contains methods for decomposing a simple cycle into a union of acyclic queries.

## License
Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at [http://www.apache.org/licenses/LICENSE-2.0](http://www.apache.org/licenses/LICENSE-2.0)

