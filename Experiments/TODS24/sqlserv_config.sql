--------------------------------------  
-- create database with a memory-optimized
-- filegroup and a container.

ALTER DATABASE AnykDB ADD FILEGROUP imoltp_mod
    CONTAINS MEMORY_OPTIMIZED_DATA;

ALTER DATABASE AnykDB ADD FILE (
    name='anykdb_mod1', filename='/var/opt/mssql/anykdb_mod1')
    TO FILEGROUP imoltp_mod;

ALTER DATABASE AnykDB
    SET MEMORY_OPTIMIZED_ELEVATE_TO_SNAPSHOT = ON;
GO  

EXEC sp_configure 'show advanced options', 1;  
GO  
RECONFIGURE WITH OVERRIDE;  
GO  
EXEC sp_configure 'max degree of parallelism', 1;  
GO  
RECONFIGURE WITH OVERRIDE;  
GO

USE AnykDB ;  
GO  
EXEC sp_configure 'show advanced options', 1;  
GO  
RECONFIGURE;  
GO  
EXEC sp_configure 'min memory per query', 100000000 ;  
GO  
RECONFIGURE;  
GO 