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
ALTER TABLE days_off
    DROP FOREIGN KEY FK_DAYSOFF_USERS,
    DROP FOREIGN KEY FK_DAYSOFF_ABSENCE;


*/
DROP TABLE IF EXISTS configuration;
DROP TABLE IF EXISTS days_off;
DROP TABLE IF EXISTS users;
DROP TABLE IF EXISTS absence_type;


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
* days_off
************************************************************/

CREATE TABLE days_off (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    day DATE NOT NULL,
    userid INTEGER NOT NULL,
    absenceid TEXT NOT NULL,
    FOREIGN KEY (userid)
        REFERENCES users (id)
            ON DELETE CASCADE,
    FOREIGN KEY (absenceid)
       REFERENCES absence_type (id)
            ON DELETE CASCADE
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
INSERT INTO users (email, firstname) VALUES ('germain@lefebvre.fr', 'Germain');
INSERT INTO absence_type (kind) VALUES ('Congé');
INSERT INTO absence_type (kind) VALUES ('Maladie');

