#!/usr/bin/env python

import sys 
sys.path.append('../')

input_dir = sys.argv[1]
l = int(sys.argv[2])
k = int(sys.argv[3])
dbms = sys.argv[4]

table = "TWITTER"
schema = "ANYK"
schemadot = schema + "."

if dbms == "psql":
    from psql_defs import *
elif dbms == "sysx":
    from sysx_defs import *
elif dbms == "duckdb":
    from duckdb_defs import *
else:
    print("Unknown DBMS")
    sys.exit(1)

if dbms == "psql" or dbms == "sysx":
    ext = ".sql"
else:
    ext = ".py"
fp = open("sql_queries/QTW2_l" + str(l) + "_k" + str(k) + "_" + dbms + ext, "w")
proc_name = "QTW2l" + str(l) + "k" + str(k)


start_statements(fp, schema, table)

create_twitter_table(fp, schema, input_dir)


q = "SELECT"
for j in range(1, l + 1):
    q += " R" + str(j) + ".Source, R" + str(j) + ".Target,"
for j in range(1, l):
    q += " R" + str(j) + ".Weight +"
q += " R" + str(l) + ".Weight as SWeight\n"
q += "FROM "
for j in range(1, l):
    q += schemadot + "TWITTER R" + str(j) + ", "
q += schemadot + "TWITTER R" + str(l) + "\n"
q += "WHERE "
for j in range(1, l - 1):
    q += "R1.Target = R" + str(j + 1) + ".Source AND "
q += "R1.Target = R" + str(l) + ".Source\n"
q += "ORDER BY SWeight ASC"

q = apply_limit_k(q, k)
q += ";\n\n"

end_statements(fp, q, schema, table, proc_name, k, l)

fp.close()