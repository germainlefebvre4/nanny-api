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
DROP TABLE IF EXISTS absence_type;
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
* absence
************************************************************/

CREATE TABLE absence_type (
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
    absenceid INTEGER NOT NULL,
    creation_date DATETIME NOT NULL,
    UNIQUE (contractid, day)
    FOREIGN KEY (contractid)
        REFERENCES contracts (id),
    FOREIGN KEY (absenceid)
       REFERENCES absence_type (id)
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

INSERT INTO absence_type (id, kind) VALUES (1, 'Présence enfant');
INSERT INTO absence_type (id, kind) VALUES (2, 'Maladie enfant');
INSERT INTO absence_type (id, kind) VALUES (3, 'Absence enfant');
INSERT INTO absence_type (id, kind) VALUES (4, 'CP enfant');
INSERT INTO absence_type (id, kind) VALUES (5, 'CP enfant exceptionnel');
INSERT INTO absence_type (id, kind) VALUES (6, 'Maladie nounou');
INSERT INTO absence_type (id, kind) VALUES (7, 'CP nounou');
INSERT INTO absence_type (id, kind) VALUES (8, 'CP nounou exceptionnel');

INSERT INTO contracts (id, creation_date, userid, nannyid) VALUES (1, datetime('now'), 1, 1);
INSERT INTO contracts (id, creation_date, userid, nannyid) VALUES (2, datetime('now'), 2, 2);

INSERT INTO working_days (id, day, creation_date, contractid, absenceid) 
    VALUES (1, "2020-01-05", datetime('now'), 1, 3);
INSERT INTO working_days (id, day, creation_date, contractid, absenceid) 
    VALUES (2, "2020-01-05", datetime('now'), 2, 4);
