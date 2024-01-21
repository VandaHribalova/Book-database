DROP TABLE IF EXISTS prekladatel;
DROP TABLE IF EXISTS nakladatelstvi;
DROP TABLE IF EXISTS kniha;
DROP TABLE IF EXISTS autor;
DROP TABLE IF EXISTS zanr;
DROP TABLE IF EXISTS kniha_autor;
DROP TABLE IF EXISTS kniha_prekladatel;
DROP TABLE IF EXISTS kniha_zanr;
DROP TABLE IF EXISTS kniha_nakladatelstvi;


CREATE TABLE prekladatel (
	prekladatel_id INTEGER PRIMARY KEY,
	jmeno TEXT NOT NULL,
	prijmeni TEXT NOT NULL,
	pocet_knih INTEGER );

CREATE TABLE nakladatelstvi (
	nakladatelstvi_id INTEGER PRIMARY KEY,
  	nazev TEXT NOT NULL,
  	rok_zalozeni INTEGER ,
  	majitel_jmeno TEXT ,
  	majitel_primeni TEXT );

CREATE TABLE kniha (
	kniha_id INTEGER PRIMARY KEY,
	nazev TEXT NOT NULL,
	rok_vydani INTEGER NOT NULL,
	serie TEXT );

CREATE TABLE autor (
	autor_id INTEGER PRIMARY KEY,
	jmeno TEXT NOT NULL,
    prijmeni TEXT NOT NULL,
    rodne_misto TEXT ,
	pocet_knih INTEGER ,
  	pocet_serii INTEGER);

CREATE TABLE zanr (
	zanr_id INTEGER PRIMARY KEY,
	zanr TEXT NOT NULL);

CREATE TABLE kniha_autor (
	kniha_autor_id INTEGER PRIMARY KEY,
	id_kniha INTEGER NOT NULL,
    id_autor INTEGER NOT NULL);

CREATE TABLE kniha_prekladatel (
	kniha_prekladatel_id INTEGER PRIMARY KEY,
  	id_kniha INTEGER NOT NULL,
  	id_prekladatel INTEGER NOT NULL);

CREATE TABLE kniha_zanr (
	kniha_zanr_id INTEGER PRIMARY KEY,
	id_kniha INTEGER NOT NULL,
    id_zanr INTEGER NOT NULL);

CREATE TABLE kniha_nakladatelstvi (
	kniha_nakladatelstvi_id INTEGER PRIMARY KEY, 
	id_kniha INTEGER NOT NULL,
    id_nakladatelstvi INTEGER NOT NULL);