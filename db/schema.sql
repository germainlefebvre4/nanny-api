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

/***********************************************************
* configuration
************************************************************/

CREATE TABLE configuration (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    value TEXT NOT NULL
);

/***********************************************************
* absence
************************************************************/

CREATE TABLE absence_type (
    id TEXT NOT NULL,
    kind TEXT NOT NULL
);

/***********************************************************
* users
************************************************************/

CREATE TABLE users (
    id INTEGER NOT NULL,
    email TEXT NUL NULL UNIQUE,
    firstname TEXT NOT NULL
);

/***********************************************************
* days_off
************************************************************/

CREATE TABLE days_off (
    id TEXT NOT NULL,
    day DATE NOT NULL,
    usersid INTEGER NOT NULL,
    absenceid TEXT NOT NULL,
    FOREIGN KEY (usersid)
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
