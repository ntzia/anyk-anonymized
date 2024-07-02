   use tempdb
   go

   dbcc shrinkfile (tempdev, 1)
   go
   -- this command shrinks the primary data file

   dbcc shrinkfile (templog, 1)
   go
   -- this command shrinks the log file,

   dbcc shrinkdatabase (tempdb, 1) 
   go