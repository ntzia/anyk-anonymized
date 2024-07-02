#!/bin/bash

# Start and configure PostgreSQL
service postgresql start
runuser -l postgres -c 'createuser root -s'
runuser -l postgres -c 'createdb root'
cp /app/Experiments/TODS24/postgresql.conf /etc/postgresql/9.5/main/
psql $USER -c 'SELECT pg_reload_conf();'

# Start and configure SQLServer
export MSSQL_SA_PASSWORD='Anyk_pwd'
#/opt/mssql/bin/mssql-conf -n setup accept-eula
cp /app/Experiments/TODS24/start_sqlserv.sh /etc/init.d/mssql-server
chmod 755 /etc/init.d/mssql-server
screen -d -m sudo -u mssql MSSQL_SA_PASSWORD=$MSSQL_SA_PASSWORD MSSQL_PID='developer' ACCEPT_EULA='Y' /opt/mssql/bin/sqlservr -c -d/var/opt/mssql/data/master.mdf -l/var/opt/mssql/data/mastlog.ldf -e/var/opt/mssql/log/errorlog -x
sleep 30
# Create a database
sqlcmd -S 127.0.0.1 -U SA -P $MSSQL_SA_PASSWORD -Q "CREATE DATABASE AnykDB"
# Create a user with a password that will be hardcoded in the scripts
sqlcmd -S 127.0.0.1 -U SA -P $MSSQL_SA_PASSWORD -Q "CREATE LOGIN Anyk WITH PASSWORD = '$MSSQL_SA_PASSWORD'"
# Unfortunately, SQL server on linux doesn't currently support the bulkadmin role. The only way to use BULK INSERT statements is to have sysadmin privileges. 
sqlcmd -S 127.0.0.1 -U SA -P $MSSQL_SA_PASSWORD -Q "EXEC AnykDB..sp_addsrvrolemember @loginame = N'Anyk', @rolename = N'sysadmin'"
# For security reasons, disable remote connections to the database, at least for the time that the experiments are run.
echo "[network]" >> /var/opt/mssql/mssql.conf
echo "ipaddress = 127.0.0.1" >> /var/opt/mssql/mssql.conf
# Set other parameters
sqlcmd -S 127.0.0.1 -U Anyk -P Anyk_pwd -i /app/Experiments/TODS24/sqlserv_config.sql

# Start the python virtual environment
source activate anyk_env

cd /app/Experiments/TODS24/Synthetic_data
./run_paths_psql.sh

# Below command can be used to avoid container termination
sleep infinity