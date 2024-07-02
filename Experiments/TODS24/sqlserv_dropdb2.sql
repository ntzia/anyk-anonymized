------------------------------------------------------------
/* Use database */ 
-------------------------------------------------------------

use AnykDB;

GO

------------------------------------------------------------------
/* Script to delete an repopulate the base [init database] */
------------------------------------------------------------------

-------------------------------------------------------------
/* Procedure delete all constraints */ 
-------------------------------------------------------------

IF EXISTS (SELECT name  
           FROM  sysobjects 
           WHERE name = 'sp_DeleteAllConstraints' AND type = 'P')
    DROP PROCEDURE dbo.sp_DeleteAllConstraints
GO

CREATE PROCEDURE sp_DeleteAllConstraints
AS
    EXEC sp_MSForEachTable 'ALTER TABLE ? NOCHECK CONSTRAINT ALL'
    EXEC sp_MSForEachTable 'ALTER TABLE ? DISABLE TRIGGER ALL'
GO

-----------------------------------------------------
/* Procedure delete all data from the database */ 
-----------------------------------------------------

IF EXISTS (SELECT name  
           FROM  sysobjects 
           WHERE name = 'sp_DeleteAllData' AND type = 'P')
    DROP PROCEDURE dbo.sp_DeleteAllData
GO

CREATE PROCEDURE sp_DeleteAllData
AS
    EXEC sp_MSForEachTable 'DELETE FROM ?'
GO

-----------------------------------------------
/* Procedure enable all constraints */ 
-----------------------------------------------

IF EXISTS (SELECT name  
           FROM  sysobjects 
           WHERE name = 'sp_EnableAllConstraints' AND type = 'P')
    DROP PROCEDURE dbo.sp_EnableAllConstraints
GO