-- Optional staging table for the assignment/demo.
-- This is intentionally NOT the Moodle core mdl_user table.
CREATE TABLE mdl_user_import (
  id INT NOT NULL,
  username VARCHAR(100) NOT NULL,
  email VARCHAR(255) NOT NULL,
  firstname VARCHAR(100) NOT NULL,
  lastname VARCHAR(100) NOT NULL,
  idnumber VARCHAR(5) NOT NULL,
  password VARCHAR(255) NOT NULL,
  city VARCHAR(100) NOT NULL,
  country CHAR(2) NOT NULL,
  PRIMARY KEY (id),
  UNIQUE (username),
  UNIQUE (email)
);
