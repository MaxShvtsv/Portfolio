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

-- Show all countries
SELECT DISTINCT countries_and_territories
FROM covid;

-- Show population of every country in 2020
SELECT DISTINCT countries_and_territories, pop_data_2020
FROM covid
WHERE year = 2020;

-- Show data only for Austria
SELECT *
FROM covid
WHERE countries_and_territories = 'Austria'
ORDER BY date_rep;

-- Show tuple with maximum deaths fixed in Austria
SELECT *
FROM covid
WHERE countries_and_territories = 'Austria' AND deaths = (
	SELECT MAX(deaths)
    FROM covid
    WHERE countries_and_territories = 'Austria'
);

-- Find country which have maximum deaths, show date and population also
SELECT date_rep, deaths, countries_and_territories, pop_data_2020
FROM covid
WHERE deaths = (
	SELECT MAX(deaths)
    FROM covid
);

-- Write a function which returns max deaths of the given country]
DELIMITER $$

DROP FUNCTION IF EXISTS max_country_deaths;
CREATE FUNCTION max_country_deaths(country VARCHAR(60))
RETURNS INT
DETERMINISTIC
BEGIN
	RETURN (
		SELECT MAX(deaths)
		FROM covid
		WHERE countries_and_territories = country
	);
END $$

DELIMITER ;

SELECT max_country_deaths('Austria');

-- Write a procedure

-- Write a trigger
