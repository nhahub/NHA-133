-- create cars1 table
CREATE TABLE IF NOT EXISTS cars1 (
    Source_Name VARCHAR(500),
    URL VARCHAR(1000),
    Price VARCHAR(100),
    DATE VARCHAR(50),
    Make VARCHAR(200),
    Model VARCHAR(200),
    `Used since` VARCHAR(50),
    Km VARCHAR(50),
    Transmission VARCHAR(50),
    City VARCHAR(200),
    Color VARCHAR(50),
    versionCleand VARCHAR(200),
    Fuel VARCHAR(50),
    Class VARCHAR(100),
    `Body Style` VARCHAR(100)
);

-- create cars2 table
CREATE TABLE IF NOT EXISTS cars2 (
    URL VARCHAR(1000),
    Price VARCHAR(50),
    City VARCHAR(200),
    Country VARCHAR(200),
    DATE VARCHAR(50),
    Title VARCHAR(200),
    Make VARCHAR(200),
    Model VARCHAR(200),
    YEAR INT,
    `Body Shape` VARCHAR(100),
    Transmission VARCHAR(50),
    Mileage_in_KM VARCHAR(50),
    `Fuel Type` VARCHAR(50),
    `Engine Capacity` VARCHAR(50),
    Color VARCHAR(50),
    `Cylinder Count` VARCHAR(50)
);

-- Load data into cars1 table
LOAD DATA INFILE 'C:/ProgramData/MySQL/MySQL Server 8.0/Uploads/cars1.csv' INTO
TABLE cars1 FIELDS TERMINATED BY ',' ENCLOSED BY '"' LINES TERMINATED BY '\n' IGNORE 1 ROWS;

-- Load data into cars2 table
LOAD DATA INFILE 'C:/ProgramData/MySQL/MySQL Server 8.0/Uploads/cars2.csv' INTO
TABLE cars2 FIELDS TERMINATED BY ',' ENCLOSED BY '"' LINES TERMINATED BY '\n' IGNORE 1 ROWS;

SELECT * FROM cars1 LIMIT 10;

-- drop the 'Source.Name' column from the 'cars1' table
ALTER TABLE cars1 DROP COLUMN `Source_Name`;

-- formatting price column to remove EGP and , and convert to float
UPDATE cars1
SET
    Price = CAST(
        REPLACE (
                REPLACE (Price, ' EGP', ''),
                    ',',
                    ''
            ) AS FLOAT
    );

-- updating Date column to DATE type
UPDATE cars1 SET DATE = NULL WHERE TRIM(DATE) = '';

ALTER TABLE cars1 MODIFY COLUMN DATE DATE;

--updating Used since column to INT type
UPDATE cars1 SET `Used since` = NULL WHERE TRIM(`Used since`) = '';

ALTER TABLE cars1 MODIFY COLUMN `Used since` INT;

-- updating Km to INT type and removing commas and Km
UPDATE cars1 SET `Km` = NULL WHERE TRIM(`Km`) = '';

UPDATE cars1
SET
    Km = CAST(
        REPLACE (
                REPLACE (Km, ' Km', ''),
                    ',',
                    ''
            ) AS UNSIGNED
    );

-- updating versionCleand name to be Version
ALTER TABLE cars1 CHANGE COLUMN versionCleand VERSION VARCHAR(255);

SELECT * FROM cars2 LIMIT 10;

SELECT DISTINCT (country) FROM cars2;

SELECT DISTINCT (city) FROM cars1;

-- drop City column from cars2
ALTER TABLE cars2 DROP COLUMN city;

-- rename country column to City in cars2
ALTER TABLE cars2 CHANGE COLUMN country City VARCHAR(255);

SELECT * FROM cars1 LIMIT 1;

SELECT * FROM cars2 LIMIT 1;

-- change Used since column to Year in cars1
ALTER TABLE cars1 CHANGE COLUMN `Used since` YEAR INT;

-- change Km in cars1 to Mileage_in_KM
ALTER TABLE cars1 CHANGE COLUMN Km Mileage_in_KM INT;

-- printing the column names for car1 and car2 to unify them
SHOW COLUMNS FROM cars1;

SHOW COLUMNS FROM cars2;

CREATE TABLE cars_merged (
    URL VARCHAR(255),
    Price DECIMAL(15, 2),
    DATE DATE,
    Make VARCHAR(50),
    Model VARCHAR(70),
    YEAR INT,
    Mileage_in_KM INT,
    Transmission VARCHAR(50),
    City VARCHAR(50),
    Color VARCHAR(50),
    Fuel VARCHAR(50),
    Class VARCHAR(50),
    Body_Style VARCHAR(50),
    Fuel_Type VARCHAR(50),
    Engine_Capacity VARCHAR(50),
    Cylinder_Count VARCHAR(50)
);

INSERT INTO
    cars_merged (
        URL,
        Price,
        DATE,
        Make,
        Model,
        YEAR,
        Mileage_in_KM,
        Transmission,
        City,
        Color,
        Fuel,
        Class,
        Body_Style,
        Fuel_Type,
        Engine_Capacity,
        Cylinder_Count
    )
SELECT
    URL,
    Price,
    STR_TO_DATE(DATE, '%d/%m/%Y') AS DATE, -- convert DD/MM/YYYY to MySQL DATE
    Make,
    Model,
    YEAR,
    Mileage_in_KM,
    Transmission,
    City,
    Color,
    NULL AS Fuel,
    NULL AS Class,
    `Body Shape` AS Body_Style,
    `Fuel Type`,
    `Engine Capacity`,
    `Cylinder Count`
FROM cars2
WHERE
    CHAR_LENGTH(Model) <= 70;

INSERT INTO
    cars_merged (
        URL,
        Price,
        DATE,
        Make,
        Model,
        YEAR,
        Mileage_in_KM,
        Transmission,
        City,
        Color,
        Fuel,
        Class,
        Body_Style,
        Fuel_Type,
        Engine_Capacity,
        Cylinder_Count
    )
SELECT
    URL,
    Price,
    CASE
        WHEN DATE LIKE '%/%/%' THEN STR_TO_DATE(DATE, '%m/%d/%Y') -- MM/DD/YYYY
        ELSE DATE -- YYYY-MM-DD أو NULL
    END AS DATE,
    Make,
    Model,
    `Used since` AS YEAR,
    Km AS Mileage_in_KM,
    Transmission,
    City,
    Color,
    Fuel,
    Class,
    `Body Style` AS Body_Style,
    NULL AS Fuel_Type,
    NULL AS Engine_Capacity,
    NULL AS Cylinder_Count
FROM cars1
WHERE
    CHAR_LENGTH(Model) <= 70
    AND CHAR_LENGTH(Make) <= 50;

SELECT DISTINCT (make) FROM final_cars;

UPDATE final_cars
SET
    make = 'BYD'
WHERE
    make IN (
        'BYD',
        'BYD ',
        'BYD.',
        'BYD',
        'BYD',
        'BYD',
        'BYD',
        'BYD',
        'BYD',
        'BYD',
        'BYD',
        'BYD',
        'Byd'
    );

UPDATE final_cars
SET
    make = 'BAIC'
WHERE
    make IN (
        'BAIC',
        'Baic',
        'BAIC ',
        'BAIC.',
        'BAIC MOTOR'
    );

UPDATE final_cars SET make = 'GMC' WHERE make IN ('GMC', 'Gmc');

UPDATE final_cars SET make = 'JAC' WHERE make IN ('JAC', 'Jac');

UPDATE final_cars SET make = 'DS' WHERE make IN ('DS', 'Ds');

UPDATE final_cars
SET
    make = 'Citroën'
WHERE
    make IN (
        'Citroen',
        'CITROEN',
        'Citroën'
    );

UPDATE final_cars
SET
    make = 'SsangYong'
WHERE
    make IN (
        'SsangYong',
        'Ssang Yong',
        'SSANGYONG'
    );

UPDATE final_cars
SET
    make = 'Changan'
WHERE
    make IN ('Chana', 'Changan');