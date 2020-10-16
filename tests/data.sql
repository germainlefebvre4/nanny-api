/*
* Drop tables content
*/
DELETE FROM configuration;
DELETE FROM working_days;
DELETE FROM users;
-- DELETE FROM day_types;
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
* day_types
************************************************************/

-- INSERT INTO day_types (id, kind) VALUES (1, 'Présence enfant');
-- INSERT INTO day_types (id, kind) VALUES (2, 'Maladie enfant');
-- INSERT INTO day_types (id, kind) VALUES (3, 'Absence enfant');
-- INSERT INTO day_types (id, kind) VALUES (4, 'CP enfant');
-- INSERT INTO day_types (id, kind) VALUES (5, 'CP enfant exceptionnel');
-- INSERT INTO day_types (id, kind) VALUES (6, 'Maladie nounou');
-- INSERT INTO day_types (id, kind) VALUES (7, 'CP nounou');
-- INSERT INTO day_types (id, kind) VALUES (8, 'CP nounou exceptionnel');
-- INSERT INTO day_types (id, kind) VALUES (49, 'Exclu du contrat');
-- INSERT INTO day_types (id, kind) VALUES (50, 'Hérité du contrat');
-- INSERT INTO day_types (id, kind) VALUES (51, 'Jour férié');

/***********************************************************
* contracts
************************************************************/

INSERT INTO contracts (id, weeks, weekdays, hours, price_hour_standard, price_hour_additional, price_hour_extra, price_fees, price_meals, start_date, end_date, creation_date, userid, nannyid) 
    VALUES (1, 52, "True,True,True,True,True,,", 8.5, 3.5, NULL, 3.8, 3.08, 4, datetime('now'), datetime('now'), datetime('now'), 1, 1);
INSERT INTO contracts (id, weeks, weekdays, hours, price_hour_standard, price_hour_additional, price_hour_extra, price_fees, start_date, end_date, creation_date, userid, nannyid) 
    VALUES (2, 44, "True,True,True,True,True,,", 10, 3.5, 3.5, 4.0, 3.08, datetime('now'), datetime('now'), datetime('now'), 2, 2);

/***********************************************************
* working_days
************************************************************/

INSERT INTO working_days (id, day, creation_date, contractid, daytypeid) 
    VALUES (1, "2020-01-05", datetime('now'), 1, 3);
INSERT INTO working_days (id, day, creation_date, contractid, daytypeid) 
    VALUES (2, "2020-01-05", datetime('now'), 2, 4);
