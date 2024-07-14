CREATE DATABASE covid19
USE covid19

/*
Create table with Covid-19 cases date in different countries.
*/
CREATE TABLE Covid(
	date_rep 					DATE 		NOT NULL,
    day 						INTEGER 	NOT NULL,
    month 						INTEGER 	NOT NULL,
    year 						INTEGER 	NOT NULL,
    cases 						INTEGER 	NOT NULL,
    deaths 					  	INTEGER  	NOT NULL,
    countries_and_territories 	VARCHAR(60) NOT NULL,
    geo_id 						VARCHAR(3)  NOT NULL,
    country_territory_code 		VARCHAR(4)  NOT NULL,
    pop_data_2020 				INTEGER 	NOT NULL,
    continent_exp 				VARCHAR(10) NOT NULL
);

/*
Enable access to load data from .csv file.
Reading Covid data from .csv file.
*/
SHOW GLOBAL VARIABLES LIKE 'local_infile'

SET GLOBAL local_infile=true

LOAD DATA LOCAL INFILE 'C:/Users/maksn/Desktop/Development/GitHub/Portfolio/Covid SQL/covid-data-mod.csv'
INTO TABLE covid
FIELDS TERMINATED BY ','
ENCLOSED BY '"' LINES TERMINATED BY '\n'
IGNORE 1 ROWS;

ALTER TABLE covid ADD COLUMN id_rep INT PRIMARY KEY UNIQUE AUTO_INCREMENT FIRST;

/*
Simple selections.
*/
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

/*
Function which returns max deaths of the given country.
*/
DELIMITER $$

DROP FUNCTION IF EXISTS max_country_deaths$$
CREATE FUNCTION max_country_deaths(country VARCHAR(60))
RETURNS INT
DETERMINISTIC
BEGIN
	RETURN (
		SELECT MAX(deaths)
		FROM covid
		WHERE countries_and_territories = country
	);
END$$

DELIMITER ;

SELECT max_country_deaths('Austria');


/*
Procedure which selects countries with
cases more than given minimum cases value.
*/
DELIMITER $$

DROP PROCEDURE IF EXISTS get_countries_by_cases$$
CREATE PROCEDURE get_countries_by_cases(min_cases INT)
BEGIN
	SELECT DISTINCT countries_and_territories
    FROM covid
    WHERE cases > min_cases;
END $$

DELIMITER ;

CALL get_countries_by_cases(200000);

/*
Procedure with loop which returns maximum cases
of countries which name like 'S...a', 'L...a'
*/
CREATE TABLE temp_table_countries(
	id_country INT PRIMARY KEY AUTO_INCREMENT,
	country VARCHAR(30)
);

INSERT INTO temp_table_countries(country)
SELECT DISTINCT countries_and_territories
FROM covid
WHERE LOWER(countries_and_territories) LIKE 's%a' OR
	  LOWER(countries_and_territories) LIKE 'l%a';

SELECT *
FROM temp_table_countries;
/*
Output:
1 Latvia
2 Lithuania
3 Slovakia
4 Slovenia
*/

DELIMITER $$

DROP PROCEDURE IF EXISTS loop_max_deaths$$
CREATE PROCEDURE loop_max_deaths()
BEGIN
	Declare iterator and
    temporary var for country in temp_table_countries
    DECLARE i INT DEFAULT 1;
	DECLARE country_var VARCHAR(30) DEFAULT '';

	Create table which store countries and
    max deaths in this country.
    DROP TABLE IF EXISTS temp_table_deaths;
	CREATE TABLE temp_table_deaths(
		country VARCHAR(30),
		deaths INT
	);

	Loop through countries.
	WHILE i <= (SELECT COUNT(*) FROM temp_table_countries) DO
        SET country_var = (
			SELECT country
			FROM temp_table_countries
            WHERE id_country = i
		);

		INSERT INTO temp_table_deaths(country, deaths)
		SELECT country_var, max_country_deaths(country_var);

		SET i = i + 1;
	END WHILE;
    
    Output
    SELECT *
    FROM temp_table_deaths;

    DROP TABLE temp_table_deaths;
END $$

DELIMITER ;

CALL loop_max_deaths();
