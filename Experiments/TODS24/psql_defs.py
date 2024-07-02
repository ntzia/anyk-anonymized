def start_statements(fp, schema, tables):
	fp.write("SET client_min_messages TO WARNING;\n")
	fp.write("SET statement_timeout TO '4000s';\n\n")
	
	if type(tables) is list:
		for table in tables:
			fp.write("DROP TABLE IF EXISTS " + schema + "." + table + ";\n")
	else:
		fp.write("DROP TABLE IF EXISTS " + schema + "." + tables + ";\n")

	fp.write("CREATE SCHEMA IF NOT EXISTS " + schema + ";\n")

def apply_limit_k(query, k):
	return query + "\nLIMIT " + str(k)

def end_statements(fp, q, schema, tables, proc_name, k, l):
	fp.write("BEGIN TRANSACTION ISOLATION LEVEL READ UNCOMMITTED;\n\n")
	fp.write(q)
	fp.write("\n\n")
	fp.write("COMMIT;\n\n")

	fp.write("BEGIN TRANSACTION ISOLATION LEVEL READ UNCOMMITTED;\n\nEXPLAIN ANALYZE ")
	fp.write(q)
	fp.write("\n\n")
	fp.write("COMMIT;\n\n")

	if type(tables) is list:
		for table in tables:
			fp.write("DROP TABLE IF EXISTS " + schema + "." + table + ";\n")
	else:
		fp.write("DROP TABLE IF EXISTS " + schema + "." + tables + ";\n")




def create_birds_table(fp, schema, input_dir):
	schema = schema + "."

	fp.write("CREATE TABLE " + schema + "BirdObs(\n")
	fp.write("\tID BIGINT,\n")
	fp.write("\tLatitude float,\n")
	fp.write("\tLongitude float,\n")
	fp.write("\tNegIndividualCount float\n")
	fp.write(");\n")
	fp.write("\n")

	fp.write("COPY " + schema + "BirdObs\n")
	fp.write("FROM '" + input_dir + "BirdObs.csv'\n")
	fp.write("DELIMITER ',' CSV;\n\n")

	## Index the joining attributes
	fp.write("CREATE INDEX ON " + schema + "BirdObs USING btree (Latitude);\n")
	fp.write("CREATE INDEX ON " + schema + "BirdObs USING btree (Longitude);\n")
	fp.write("CREATE INDEX ON " + schema + "BirdObs USING btree (NegIndividualCount);\n\n")
	fp.write("\n")

def create_reddit_table(fp, schema, input_dir):
	schema = schema + "."

	fp.write("CREATE TABLE " + schema + "REDDIT (\n")
	fp.write("\tSource numeric,\n")
	fp.write("\tTarget numeric,\n")
	fp.write("\tTimest float,\n")
	fp.write("\tSentiment float,\n")
	fp.write("\tLen float,\n")
	fp.write("\tInverseReadability float\n")
	fp.write(");\n")
	fp.write("\n")

	fp.write("COPY " + schema + "REDDIT\n")
	fp.write("FROM '" + input_dir + "Reddit.csv'\n")
	fp.write("DELIMITER ',' CSV;\n\n")

	fp.write("CREATE INDEX ON " + schema + "REDDIT USING hash (Source);\n")
	fp.write("CREATE INDEX ON " + schema + "REDDIT USING hash (Target);\n")
	fp.write("CREATE INDEX ON " + schema + "REDDIT USING btree (Timest);\n\n")
	fp.write("CREATE INDEX ON " + schema + "REDDIT USING btree (Sentiment);\n\n")
	fp.write("\n")

def create_synthetic_hash_tables(fp, schema, input_dir, l):
	schema = schema + "."

	for j in range(1, l + 1):
		fp.write("CREATE TABLE " + schema + "R" + str(j) + " (\n")
		fp.write("\tA" + str(2 * j - 1) + " numeric,\n")
		fp.write("\tA" + str(2 * j) + " numeric,\n")
		fp.write("\tWeight" + str(j) + " float\n")
		fp.write(");\n")
		fp.write("\n")

		fp.write("COPY " + schema + "R" + str(j) + "\n")
		fp.write("FROM '" + input_dir + "R" + str(j) + ".csv'\n")
		fp.write("DELIMITER ',' CSV;\n")
		fp.write("\n")

		fp.write("CREATE INDEX ON " + schema + "R" + str(j) + " USING hash (A" + str(2 * j - 1) + ");\n")
		fp.write("CREATE INDEX ON " + schema + "R" + str(j) + " USING hash (A" + str(2 * j) + ");\n")
		fp.write("CREATE INDEX ON " + schema + "R" + str(j) + " USING btree (Weight" + str(j) + ");\n")
	fp.write("\n")

def create_synthetic_tables(fp, schema, input_dir, l):
	schema = schema + "."

	for j in range(1, l + 1):
		fp.write("CREATE TABLE " + schema + "R" + str(j) + " (\n")
		fp.write("\tA" + str(2 * j - 1) + " numeric,\n")
		fp.write("\tA" + str(2 * j) + " numeric,\n")
		fp.write("\tWeight" + str(j) + " float\n")
		fp.write(");\n")
		fp.write("\n")

		fp.write("COPY " + schema + "R" + str(j) + "\n")
		fp.write("FROM '" + input_dir + "R" + str(j) + ".csv'\n")
		fp.write("DELIMITER ',' CSV;\n")
		fp.write("\n")

		fp.write("CREATE INDEX ON " + schema + "R" + str(j) + " USING btree (A" + str(2 * j - 1) + ");\n")
		fp.write("CREATE INDEX ON " + schema + "R" + str(j) + " USING btree (A" + str(2 * j) + ");\n")
		fp.write("CREATE INDEX ON " + schema + "R" + str(j) + " USING btree (Weight" + str(j) + ");\n")
	fp.write("\n")

def create_lineitem_table(fp, schema, input_file):
	schema = schema + "."

	fp.write("CREATE TABLE " + schema + "LINEITEM (\n")
	fp.write("\tOrderKey numeric,\n")
	fp.write("\tPartKey numeric,\n")
	fp.write("\tSuppkey numeric,\n")
	fp.write("\tLineNumber numeric,\n")
	fp.write("\tQuantity numeric,\n")
	fp.write("\tNegExtendedPrice float,\n")
	fp.write("\tShipDate numeric,\n")
	fp.write("\tCommitDate numeric,\n")
	fp.write("\tReceiptDate numeric\n")
	fp.write(");")
	fp.write("\n\n") 

	fp.write("COPY " + schema + "LINEITEM\n")
	fp.write("FROM '" + input_file + "'\n")
	fp.write("DELIMITER ',' CSV;\n")
	fp.write("\n")

	fp.write("CREATE INDEX ON " + schema + "LINEITEM USING Hash (Suppkey);\n")
	fp.write("CREATE INDEX ON " + schema + "LINEITEM USING btree (Quantity, ShipDate);\n")
	fp.write("CREATE INDEX ON " + schema + "LINEITEM USING btree (ShipDate);\n")
	fp.write("CREATE INDEX ON " + schema + "LINEITEM USING btree (Quantity, CommitDate);\n")
	fp.write("CREATE INDEX ON " + schema + "LINEITEM USING btree (CommitDate);\n")
	fp.write("CREATE INDEX ON " + schema + "LINEITEM USING btree (Quantity, ReceiptDate);\n")
	fp.write("CREATE INDEX ON " + schema + "LINEITEM USING btree (ReceiptDate);\n")
	fp.write("CREATE INDEX ON " + schema + "LINEITEM USING btree (NegExtendedPrice);\n")
	fp.write("\n")

def create_weighted_graph_table(fp, schema, input_dir, table_name):
	schema = schema + "."

	fp.write("CREATE TABLE " + schema + table_name + "(\n")
	fp.write("\tSource numeric,\n")
	fp.write("\tTarget numeric,\n")
	fp.write("\tWeight numeric\n")
	fp.write(");\n")
	fp.write("\n")

	fp.write("COPY " + schema + table_name + "\n")
	fp.write("FROM '" + input_dir + "Edges.csv'\n")
	fp.write("DELIMITER ',' CSV;\n\n")
	fp.write("\n")

	fp.write("CREATE INDEX ON " + schema + table_name + " USING hash (Source);\n")
	fp.write("CREATE INDEX ON " + schema + table_name + " USING hash (Target);\n")
	fp.write("CREATE INDEX ON " + schema + table_name + " USING btree (Weight);\n\n")
	fp.write("\n")

def create_bitcoin_table(fp, schema, input_dir):
	schema = schema + "."

	fp.write("CREATE TABLE " + schema + "BITCOIN (\n")
	fp.write("\tSource numeric,\n")
	fp.write("\tTarget numeric,\n")
	fp.write("\tRating numeric\n")
	fp.write(");\n")
	fp.write("\n")

	fp.write("COPY " + schema + "BITCOIN\n")
	fp.write("FROM '" + input_dir + "Edges.csv'\n")
	fp.write("DELIMITER ',' CSV;\n\n")
	fp.write("\n")

	fp.write("CREATE INDEX ON " + schema + "BITCOIN USING hash (Source);\n")
	fp.write("CREATE INDEX ON " + schema + "BITCOIN USING hash (Target);\n")
	fp.write("CREATE INDEX ON " + schema + "BITCOIN USING btree (Rating);\n\n")
	fp.write("\n")

def create_twitter_table(fp, schema, input_dir):
	schema = schema + "."
	
	fp.write("CREATE TABLE " + schema + "TWITTER (\n")
	fp.write("\tSource numeric,\n")
	fp.write("\tTarget numeric,\n")
	fp.write("\tWeight numeric\n")
	fp.write(");\n")
	fp.write("\n")

	fp.write("COPY " + schema + "TWITTER\n")
	fp.write("FROM '" + input_dir + "Edges.csv'\n")
	fp.write("DELIMITER ',' CSV;\n\n")
	fp.write("\n")

	fp.write("CREATE INDEX ON " + schema + "TWITTER USING hash (Source);\n")
	fp.write("CREATE INDEX ON " + schema + "TWITTER USING hash (Target);\n")
	fp.write("CREATE INDEX ON " + schema + "TWITTER USING btree (Weight);\n\n")
	fp.write("\n")