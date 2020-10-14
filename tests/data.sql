/*
* Drop tables content
*/
DELETE FROM configuration;
DELETE FROM working_days;
DELETE FROM users;
DELETE FROM absence_type;
DELETE FROM nannies;
DELETE FROM contracts;


/***********************************************************
* users
************************************************************/

INSERT INTO users (id, email, firstname) VALUES (1, 'germain@lefebvre.fr', 'Germain');
INSERT INTO users (id, email, firstname) VALUES (2, 'toto@biclo.fr', 'Toto');

/***********************************************************
* nannies
************************************************************/

INSERT INTO nannies (id, email, firstname) VALUES (1, 'claudie@nanny.fr', 'Claudie');
INSERT INTO nannies (id, email, firstname) VALUES (2, 'tata@nanny.fr', 'Tata');

/***********************************************************
* absence
************************************************************/

INSERT INTO absence_type (id, kind) VALUES (1, 'Présence enfant');
INSERT INTO absence_type (id, kind) VALUES (2, 'Maladie Enfant');
INSERT INTO absence_type (id, kind) VALUES (3, 'Absence Enfant');
INSERT INTO absence_type (id, kind) VALUES (4, 'CP Enfant');
INSERT INTO absence_type (id, kind) VALUES (5, 'CP Enfant exceptionnel');
INSERT INTO absence_type (id, kind) VALUES (6, 'Maladie Nounou');
INSERT INTO absence_type (id, kind) VALUES (7, 'CP Nounou');
INSERT INTO absence_type (id, kind) VALUES (8, 'CP Nounou exceptionnel');

/***********************************************************
* contracts
************************************************************/

INSERT INTO contracts (id, weekdays, start_date, end_date, creation_date, userid, nannyid) VALUES (1, "1,2,3,4,5", datetime('now'), datetime('now'), datetime('now'), 1, 1);
INSERT INTO contracts (id, weekdays, start_date, end_date, creation_date, userid, nannyid) VALUES (2, "1,2,3,4,5", datetime('now'), datetime('now'), datetime('now'), 2, 2);

/***********************************************************
* working_days
************************************************************/

INSERT INTO working_days (id, day, creation_date, contractid, absenceid) 
    VALUES (1, "2020-01-05", datetime('now'), 1, 3);
INSERT INTO working_days (id, day, creation_date, contractid, absenceid) 
    VALUES (2, "2020-01-05", datetime('now'), 2, 4);
