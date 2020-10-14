/*
* Drop tables content
*/
DELETE FROM users;
DELETE FROM absence_type;

/***********************************************************
* users
************************************************************/

INSERT INTO users (id, email, firstname) VALUES (1, 'germain@lefebvre.fr', 'Germain');
INSERT INTO users (id, email, firstname) VALUES (2, 'toto@biclo.fr', 'Toto');

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
* working_days
************************************************************/

-- INSERT INTO working_days (usersabsenceid) VALUES (1', 1, '1');
