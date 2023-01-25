-- CREATE DATABASE tv

-- USE tv

CREATE TABLE Channel (
  id_channel   INT PRIMARY KEY,
  name_channel VARCHAR(100) NOT NULL
);

CREATE TABLE Quiz (
  date_quiz    DATETIME,
  nom_operator  INT,
  channels VARCHAR(20),
  CONSTRAINT PK_QUIZ PRIMARY KEY(date_quiz, nom_operator)
);