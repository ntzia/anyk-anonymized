import textwrap

def start_statements(fp, schema, tables):
	fp.write(textwrap.dedent('''\
		import duckdb
		from timeit import default_timer as timer

		# Start connection and set parameters
		con = duckdb.connect(
								database = ":memory:", 
								config = { 
											'threads': 1,
											'memory_limit' : '110GB',
											'checkpoint_threshold' : '1000GB',
											'preserve_insertion_order' : 'false'
										}
							)
		
		# Create schema
		con.execute("CREATE SCHEMA ''') + schema + ";\")\n\n"
	)


def apply_limit_k(query, k):
	return query + "\nLIMIT " + str(k)

def end_statements(fp, q, schema, tables, proc_name, k, l):
	fp.write("# Run query once\n")
	fp.write('''con.execute("""\n''')
	fp.write('\t\t\t')
	fp.write('\t\t\t'.join(q.splitlines(True)))
	fp.write('''\t\t""")''')
	fp.write("\nans = con.fetchall()")
	fp.write("\n\n")


	fp.write("# Run query again\n")
	fp.write("start = timer()\n")
	fp.write('''con.execute("""\n''')
	fp.write('\t\t\t')
	fp.write('\t\t\t'.join(q.splitlines(True)))
	fp.write('''\t\t""")''')
	fp.write("\n\n")

			# # Enumerate all answers and measure time for first and last
			# k = 0
			# ans = con.fetchone()
			# end = timer()
			# print("k= 1 Time= " + str(end - start) + " sec")
			# while ans is not None:
			# 	k += 1
			# 	ans = con.fetchone()
			# end = timer()
			# print("k= " + str(k) + " Time= " + str(end - start) + " sec")
	
	if k == 0:
		fp.write(textwrap.dedent('''\
			# fetchall is way too slow, only measure the time for the query
			end = timer()
			print("Time= " + str(end - start) + " sec")
		'''))
	else:
		fp.write(textwrap.dedent('''\
			# Retrieve all answers at once
			ans = con.fetchall()
			end = timer()
			print("k= " + str(len(ans)) + " Time= " + str(end - start) + " sec")
		'''))
		
def create_bitcoin_table(fp, schema, input_dir):
	schema = schema + "."

	fp.write("# Create table\n")
	fp.write(textwrap.dedent('''\
		con.execute("""
			CREATE TABLE ''') + schema + "BITCOIN AS SELECT * FROM \\\n")
	fp.write("\t\t" + textwrap.dedent('''\
				read_csv(\'''') + input_dir + "Edges.csv',\n")
	fp.write(textwrap.dedent('''\
				delim = ',',
				header = false,
				columns = {
					'Source': 'numeric',
					'Target': 'numeric',
					'Rating': 'numeric'
				});
		""")
	  
		''')
	)

	fp.write(textwrap.dedent('''\
		# Create indexes
		con.execute("CREATE INDEX INDS ON ''' + schema + '''BITCOIN (Source);")
		con.execute("CREATE INDEX INDT ON ''' + schema + '''BITCOIN (Target);")
		con.execute("CREATE INDEX INDR ON ''' + schema + '''BITCOIN (Rating);")

		''')
	)

def create_twitter_table(fp, schema, input_dir):
	schema = schema + "."
	
	fp.write("# Create table\n")
	fp.write(textwrap.dedent('''\
		con.execute("""
			CREATE TABLE ''') + schema + "TWITTER AS SELECT * FROM \\\n")
	fp.write("\t\t" + textwrap.dedent('''\
				read_csv(\'''') + input_dir + "Edges.csv',\n")
	fp.write(textwrap.dedent('''\
				delim = ',',
				header = false,
				columns = {
					'Source': 'numeric',
					'Target': 'numeric',
					'Weight': 'numeric'
				});
		""")
	  
		''')
	)

	fp.write(textwrap.dedent('''\
		# Create indexes
		con.execute("CREATE INDEX INDS ON ''' + schema + '''TWITTER (Source);")
		con.execute("CREATE INDEX INDT ON ''' + schema + '''TWITTER (Target);")
		con.execute("CREATE INDEX INDR ON ''' + schema + '''TWITTER (Weight);")

		''')
	)

def create_synthetic_hash_tables(fp, schema, input_dir, l):
	schema = schema + "."

	for j in range(1, l + 1):
		fp.write("# Create table\n")
		fp.write(textwrap.dedent('''\
			con.execute("""
				CREATE TABLE ''') + schema + "R" + str(j) + " AS SELECT * FROM \\\n")
		fp.write("\t\t" + textwrap.dedent('''\
					read_csv(\'''') + input_dir + "R" + str(j) + ".csv',\n")
		fp.write(textwrap.dedent('''\
					delim = ',',
					header = false,
					columns = {
						'A''' + str(2 * j - 1) + '''': 'numeric',
						'A''' + str(2 * j) + '''': 'numeric',
						'Weight''' + str(j) + '''': 'float'
					});
			""")
	  
			''')
		)

		fp.write(textwrap.dedent('''\
			# Create indexes
			con.execute("CREATE INDEX INDS''' + str(j) + ''' ON ''' + schema + "R" + str(j) + "(A" + str(2 * j - 1) + ''');")
			con.execute("CREATE INDEX INDT''' + str(j) + ''' ON ''' + schema + "R" + str(j) + "(A" + str(2 * j) + ''');")
			con.execute("CREATE INDEX INDR''' + str(j) + ''' ON ''' + schema + "R" + str(j) + "(Weight" + str(j) + ''');")

			''')
		)

def create_weighted_graph_table(fp, schema, input_dir, table_name):
	schema = schema + "."

	fp.write("# Create table\n")
	fp.write(textwrap.dedent('''\
		con.execute("""
			CREATE TABLE ''') + schema + table_name + " AS SELECT * FROM \\\n")
	fp.write("\t\t" + textwrap.dedent('''\
				read_csv(\'''') + input_dir + "Edges.csv',\n")
	fp.write(textwrap.dedent('''\
				delim = ',',
				header = false,
				columns = {
					'Source': 'numeric',
					'Target': 'numeric',
					'Weight': 'numeric'
				});
		""")
	  
		''')
	)

	fp.write(textwrap.dedent('''\
		# Create indexes
		con.execute("CREATE INDEX INDS ON ''' + schema + table_name + ''' (Source);")
		con.execute("CREATE INDEX INDT ON ''' + schema + table_name + ''' (Target);")
		con.execute("CREATE INDEX INDR ON ''' + schema + table_name + ''' (Weight);")

		''')
	)
