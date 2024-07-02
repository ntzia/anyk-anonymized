def drop_all_procedures_sysx():
	s = ""
	s += "-- drop all user defined stored procedures\n"
	s += "Declare @procName varchar(500)\nDeclare cur Cursor For Select [name] From sys.objects where type = 'p'\n"
	s += "Open cur\nFetch Next From cur Into @procName\nWhile @@fetch_status = 0\nBegin\n"
	s += " Exec('drop procedure ' + @procName)\n Fetch Next From cur Into @procName\nEnd\n"
	s += "Close cur\nDeallocate cur\n"
	return s


def start_statements(fp, schema, tables):
    fp.write("USE AnykDB;\n\n")

    fp.write(drop_all_procedures_sysx())
    fp.write("GO\n")

    if type(tables) is list:
        for table in tables:
            fp.write("DROP TABLE IF EXISTS " + schema + "." + table + ";\n")
    else:
        fp.write("DROP TABLE IF EXISTS " + schema + "." + tables + ";\n")
    fp.write("GO\n")
    fp.write("CREATE SCHEMA " + schema + ";\n")
    fp.write("GO\n")

def apply_limit_k(query, k):
	return "SELECT TOP " + str(k) + query[6:]

def end_statements(fp, q, schema, tables, proc_name, k, l):
	## Create a natively compiled stored procedure for System X
	if k < 8192 / 2:
		fp.write("GO\n")
		fp.write("CREATE PROCEDURE " + proc_name + "\n")
		fp.write("WITH NATIVE_COMPILATION, SCHEMABINDING, EXECUTE AS OWNER\nAS BEGIN ATOMIC WITH\n(\n\tTRANSACTION ISOLATION LEVEL = SNAPSHOT, LANGUAGE = N'us_english'\n)\n")
		fp.write(q)
		fp.write("END\nGO\n\n")

	fp.write("BEGIN TRANSACTION;\n\n")
	if k < 8192 / l:
		fp.write("EXEC " + proc_name + ";")
	fp.write("\n\n")
	fp.write("COMMIT TRANSACTION;\n\n\n")

	fp.write("BEGIN TRANSACTION;\n\n")
	fp.write("SET TRANSACTION ISOLATION LEVEL READ UNCOMMITTED;\n\n")
	fp.write("SET STATISTICS TIME ON;\n\n")
	if k < 8192 / l:
		fp.write("EXEC " + proc_name + ";")
	fp.write("\n\n")
	fp.write("SET STATISTICS TIME OFF;\nGO\n")
	fp.write("COMMIT TRANSACTION;\n\n")

	# For System X, provide the query once more to get the query plan
	fp.write("GO\nSET SHOWPLAN_XML ON;\nGO\n")
	if k < 8192 / l:
		fp.write("EXEC " + proc_name + ";")
	else:
		fp.write(q)
	fp.write("\n")
	fp.write("GO\nSET SHOWPLAN_XML OFF;\nGO\n\n")

	fp.write(drop_all_procedures_sysx())
	if type(tables) is list:
		for table in tables:
			fp.write("DROP TABLE IF EXISTS " + schema + "." + table + ";\n")
	else:
		fp.write("DROP TABLE IF EXISTS " + schema + "." + tables + ";\n")


def create_birds_table(fp, schema, input_dir):
	schema = schema + "."

	fp.write("CREATE TABLE " + schema + "BirdObs(\n")
	fp.write("\tID BIGINT,\n")
	fp.write("\tLatitude float INDEX ILA NONCLUSTERED,\n")
	fp.write("\tLongitude float INDEX ILO NONCLUSTERED,\n")
	fp.write("\tNegIndividualCount float INDEX INIC NONCLUSTERED\n")
	fp.write(")\nWITH (MEMORY_OPTIMIZED = ON, DURABILITY = SCHEMA_ONLY")  
	fp.write(");\n")
	fp.write("\n")

	fp.write("BULK INSERT " + schema + "BirdObs\n")
	fp.write("FROM '" + input_dir + "BirdObs.csv'\n")
	fp.write("WITH\n(\n\tFIELDTERMINATOR=',',\n\tROWTERMINATOR='\\n'\n)\n")
	fp.write("\n")

def create_reddit_table(fp, schema, input_dir):
	schema = schema + "."

	fp.write("CREATE TABLE " + schema + "REDDIT (\n")
	fp.write("\tSource numeric INDEX ISH HASH WITH (BUCKET_COUNT = 100000),\n")
	fp.write("\tTarget numeric INDEX ITH NONCLUSTERED HASH WITH (BUCKET_COUNT = 100000),\n")
	fp.write("\tTimest float INDEX IT NONCLUSTERED,\n")
	fp.write("\tSentiment float INDEX ISB NONCLUSTERED,\n")
	fp.write("\tLen float,\n")
	fp.write("\tInverseReadability float\n")
	fp.write(")\nWITH (MEMORY_OPTIMIZED = ON, DURABILITY = SCHEMA_ONLY")  
	fp.write(");\n")
	fp.write("\n")

	fp.write("BULK INSERT " + schema + "REDDIT\n")
	fp.write("FROM '" + input_dir + "Reddit.csv'\n")
	fp.write("WITH\n(\n\tFIELDTERMINATOR=',',\n\tROWTERMINATOR='\\n'\n)\n")
	fp.write("\n")

def create_synthetic_hash_tables(fp, schema, input_dir, l):
	schema = schema + "."

	for j in range(1, l + 1):
		fp.write("CREATE TABLE " + schema + "R" + str(j) + " (\n")
		fp.write("\tA" + str(2 * j - 1) + " numeric INDEX I" + str(j) + "1 HASH WITH (BUCKET_COUNT = 100000),\n")
		fp.write("\tA" + str(2 * j) + " numeric INDEX I" + str(j) + "2 HASH WITH (BUCKET_COUNT = 100000),\n")
		fp.write("\tWeight" + str(j) + " float INDEX I" + str(j) + "W NONCLUSTERED\n")
		fp.write(")\nWITH (MEMORY_OPTIMIZED = ON, DURABILITY = SCHEMA_ONLY")  
		fp.write(");\n")
		fp.write("\n")

		fp.write("BULK INSERT " + schema + "R" + str(j) + "\n")
		fp.write("FROM '" + input_dir + "R" + str(j) + ".csv'\n")
		fp.write("WITH\n(\n\tFIELDTERMINATOR=',',\n\tROWTERMINATOR='\\n'\n)\n")
	fp.write("\n")

def create_synthetic_tables(fp, schema, input_dir, l):
	schema = schema + "."

	for j in range(1, l + 1):
		fp.write("CREATE TABLE " + schema + "R" + str(j) + " (\n")
		fp.write("\tA" + str(2 * j - 1) + " numeric INDEX I" + str(j) + "1 NONCLUSTERED,\n")
		fp.write("\tA" + str(2 * j) + " numeric INDEX I" + str(j) + "2 NONCLUSTERED,\n")
		fp.write("\tWeight" + str(j) + " float INDEX I" + str(j) + "W NONCLUSTERED\n")
		fp.write(")\nWITH (MEMORY_OPTIMIZED = ON, DURABILITY = SCHEMA_ONLY")  
		fp.write(");\n")
		fp.write("\n")

		fp.write("BULK INSERT " + schema + "R" + str(j) + "\n")
		fp.write("FROM '" + input_dir + "R" + str(j) + ".csv'\n")
		fp.write("WITH\n(\n\tFIELDTERMINATOR=',',\n\tROWTERMINATOR='\\n'\n)\n")
	fp.write("\n")

def create_lineitem_table(fp, schema, input_file):
	schema = schema + "."

	fp.write("CREATE TABLE " + schema + "LINEITEM (\n")
	fp.write("\tOrderKey numeric,\n")
	fp.write("\tPartKey numeric,\n")
	fp.write("\tSuppkey numeric INDEX IH HASH WITH (BUCKET_COUNT = 500000),\n")
	fp.write("\tLineNumber numeric,\n")
	fp.write("\tQuantity numeric INDEX IQ NONCLUSTERED,\n")
	fp.write("\tNegExtendedPrice float INDEX IP NONCLUSTERED,\n")
	fp.write("\tShipDate numeric INDEX ISD NONCLUSTERED,\n")
	fp.write("\tCommitDate numeric,\n")
	fp.write("\tReceiptDate numeric\n")
	fp.write(")\nWITH (MEMORY_OPTIMIZED = ON, DURABILITY = SCHEMA_ONLY")  
	fp.write(");")
	fp.write("\n\n") 

	fp.write("BULK INSERT " + schema + "LINEITEM\n")
	fp.write("FROM '" + input_file + "'\n")
	fp.write("WITH\n(\n\tFIELDTERMINATOR=',',\n\tROWTERMINATOR='\\n'\n)\n")
	fp.write("\n")

def create_weighted_graph_table(fp, schema, input_dir, table_name):
	schema = schema + "."

	fp.write("CREATE TABLE " + schema + table_name + " (\n")
	fp.write("\tSource numeric INDEX ISH HASH WITH (BUCKET_COUNT = 100000),\n")
	fp.write("\tTarget numeric INDEX ITH NONCLUSTERED HASH WITH (BUCKET_COUNT = 100000),\n")
	fp.write("\tWeight float INDEX IT NONCLUSTERED\n")
	fp.write(")\nWITH (MEMORY_OPTIMIZED = ON, DURABILITY = SCHEMA_ONLY")  
	fp.write(");")
	fp.write("\n\n") 

	fp.write("BULK INSERT " + schema + table_name + "\n")
	fp.write("FROM '" + input_dir + "Edges.csv'\n")
	fp.write("WITH\n(\n\tFIELDTERMINATOR=',',\n\tROWTERMINATOR='\\n'\n)\n")
	fp.write("\n")

def create_bitcoin_table(fp, schema, input_dir):
	schema = schema + "."

	fp.write("CREATE TABLE " + schema + "BITCOIN (\n")
	fp.write("\tSource numeric INDEX ISH HASH WITH (BUCKET_COUNT = 100000),\n")
	fp.write("\tTarget numeric INDEX ITH NONCLUSTERED HASH WITH (BUCKET_COUNT = 100000),\n")
	fp.write("\tRating float INDEX IT NONCLUSTERED\n")
	fp.write(")\nWITH (MEMORY_OPTIMIZED = ON, DURABILITY = SCHEMA_ONLY")  
	fp.write(");")
	fp.write("\n\n") 

	fp.write("BULK INSERT " + schema + "BITCOIN\n")
	fp.write("FROM '" + input_dir + "Edges.csv'\n")
	fp.write("WITH\n(\n\tFIELDTERMINATOR=',',\n\tROWTERMINATOR='\\n'\n)\n")
	fp.write("\n")

def create_twitter_table(fp, schema, input_dir):
	schema = schema + "."

	fp.write("CREATE TABLE " + schema + "TWITTER (\n")
	fp.write("\tSource numeric INDEX ISH HASH WITH (BUCKET_COUNT = 100000),\n")
	fp.write("\tTarget numeric INDEX ITH NONCLUSTERED HASH WITH (BUCKET_COUNT = 100000),\n")
	fp.write("\tWeight float INDEX IT NONCLUSTERED\n")
	fp.write(")\nWITH (MEMORY_OPTIMIZED = ON, DURABILITY = SCHEMA_ONLY")  
	fp.write(");")
	fp.write("\n\n") 

	fp.write("BULK INSERT " + schema + "TWITTER\n")
	fp.write("FROM '" + input_dir + "Edges.csv'\n")
	fp.write("WITH\n(\n\tFIELDTERMINATOR=',',\n\tROWTERMINATOR='\\n'\n)\n")
	fp.write("\n")