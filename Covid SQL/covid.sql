-- CREATE DATABASE covid19
-- USE covid19

-- CREATE TABLE Covid(
-- 	date_rep 					DATE 		NOT NULL,
--     day 						INTEGER 	NOT NULL,
--     month 						INTEGER 	NOT NULL,
--     year 						INTEGER 	NOT NULL,
--     cases 						INTEGER 	NOT NULL,
--     deaths 					  	INTEGER  	NOT NULL,
--     countries_and_territories 	VARCHAR(60) NOT NULL,
--     geo_id 						VARCHAR(3)  NOT NULL,
--     country_territory_code 		VARCHAR(4)  NOT NULL,
--     pop_data_2020 				INTEGER 	NOT NULL,
--     continent_exp 				VARCHAR(10) NOT NULL
-- );

-- DROP TABLE covid;

-- SHOW GLOBAL VARIABLES LIKE 'local_infile'

-- SET GLOBAL local_infile=true

-- TRUNCATE TABLE covid;

-- LOAD DATA LOCAL INFILE 'C:/Users/maksn/Desktop/Development/GitHub/Portfolio/Covid SQL/covid-data-mod.csv'
-- INTO TABLE covid
-- FIELDS TERMINATED BY ','
-- ENCLOSED BY '"' LINES TERMINATED BY '\n'
-- IGNORE 1 ROWS;

-- ALTER TABLE covid ADD COLUMN id_rep INT PRIMARY KEY UNIQUE AUTO_INCREMENT FIRST;

SELECT AVG(cases)
FROM covid;