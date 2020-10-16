/***********************************************************
*
* MPD Designer 3.1.4150.32424
*
* Code for PostgreSQL 7.4
* Generated on 03/01/2020 13:31:32
*
* Louis SAUNDERS
* http://louis.saunders.free.fr/
*
************************************************************/
/*
ALTER TABLE working_days
    DROP FOREIGN KEY FK_WORKINGDAYS_USERS,
    DROP FOREIGN KEY FK_WORKINGDAYS_ABSENCE;
*/
DROP TABLE IF EXISTS configuration;
DROP TABLE IF EXISTS working_days;
DROP TABLE IF EXISTS users;
DROP TABLE IF EXISTS day_types;
DROP TABLE IF EXISTS nannies;
DROP TABLE IF EXISTS contracts;


PRAGMA encoding="UTF-8";


/***********************************************************
* configuration
************************************************************/

CREATE TABLE configuration (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    value TEXT NOT NULL
);

/***********************************************************
* day_types
************************************************************/

CREATE TABLE day_types (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    kind TEXT NOT NULL
);

/***********************************************************
* users
************************************************************/

CREATE TABLE users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    email TEXT NUL NULL UNIQUE,
    firstname TEXT NOT NULL
);

/***********************************************************
* nanny
************************************************************/

CREATE TABLE nannies (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    email TEXT NOT NULL UNIQUE,
    firstname TEXT NOT NULL
);

/***********************************************************
* contract
************************************************************/

CREATE TABLE contracts (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nannyid INTEGER NOT NULL,
    userid INTEGER NOT NULL,
    weekdays INTEGER NOT NULL,
    weeks INTEGER NOT NULL,
    hours REAL NOT NULL,
    price_hour_standard REAL NOT NULL,
    price_hour_additional REAL,
    price_hour_extra REAL NOT NULL,
    price_fees REAL NOT NULL,
    price_meals REAL,
    start_date DATETIME,
    end_date DATETIME,
    creation_date DATETIME NOT NULL,
    updated_date DATETIME,
    UNIQUE (nannyid, userid)
    FOREIGN KEY (nannyid)
       REFERENCES nannies (id),
    FOREIGN KEY (userid)
        REFERENCES users (id)
);

/***********************************************************
* working_days
************************************************************/

CREATE TABLE working_days (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    day TEXT NOT NULL,
    contractid INTEGER NOT NULL,
    daytypeid INTEGER NOT NULL,
    creation_date DATETIME NOT NULL,
    UNIQUE (contractid, day)
    FOREIGN KEY (contractid)
        REFERENCES contracts (id),
    FOREIGN KEY (daytypeid)
       REFERENCES day_types (id)
);


/***********************************************************
* INDEXED KEYS
************************************************************/


/***********************************************************
* FOREIGN KEYS
************************************************************/

/***********************************************************
* DATA
************************************************************/
INSERT INTO users (id, email, firstname) VALUES (1, 'germain@lefebvre.fr', 'Germain');
INSERT INTO users (id, email, firstname) VALUES (2, 'toto@biclo.fr', 'Toto');

INSERT INTO nannies (id, email, firstname) VALUES (1, 'claudie@nanny.fr', 'Claudie');
INSERT INTO nannies (id, email, firstname) VALUES (2, 'tata@nanny.fr', 'Tata');

INSERT INTO day_types (id, kind) VALUES (1, 'Présence enfant');
INSERT INTO day_types (id, kind) VALUES (2, 'Maladie enfant');
INSERT INTO day_types (id, kind) VALUES (3, 'Absence enfant');
INSERT INTO day_types (id, kind) VALUES (4, 'CP enfant');
INSERT INTO day_types (id, kind) VALUES (5, 'CP enfant exceptionnel');
INSERT INTO day_types (id, kind) VALUES (6, 'Maladie nounou');
INSERT INTO day_types (id, kind) VALUES (7, 'CP nounou');
INSERT INTO day_types (id, kind) VALUES (8, 'CP nounou exceptionnel');
INSERT INTO day_types (id, kind) VALUES (49, 'Exclu du contrat');
INSERT INTO day_types (id, kind) VALUES (50, 'Hérité du contrat');
INSERT INTO day_types (id, kind) VALUES (51, 'Jour férié');

INSERT INTO contracts (id, weeks, weekdays, hours, price_hour_standard, price_hour_additional, price_hour_extra, price_fees, price_meals, start_date, end_date, creation_date, userid, nannyid) 
    VALUES (1, 52, "True,True,True,True,True,,", 8.5, 3.5, NULL, 3.8, 3.08, 4, datetime('now'), datetime('now'), datetime('now'), 1, 1);
INSERT INTO contracts (id, weeks, weekdays, hours, price_hour_standard, price_hour_additional, price_hour_extra, price_fees, start_date, end_date, creation_date, userid, nannyid) 
    VALUES (2, 44, "True,True,True,True,True,,", 10, 3.5, 3.5, 4.0, 3.08, datetime('now'), datetime('now'), datetime('now'), 2, 2);

INSERT INTO working_days (id, day, creation_date, contractid, daytypeid) 
    VALUES (1, "2020-01-05", datetime('now'), 1, 3);
INSERT INTO working_days (id, day, creation_date, contractid, daytypeid) 
    VALUES (2, "2020-01-05", datetime('now'), 2, 4);
