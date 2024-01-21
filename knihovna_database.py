import sqlite3

connection = sqlite3.connect('knihovna.db')
with open('knihovna_scheme.sql') as f:
   connection.executescript(f.read())

cursor = connection.cursor()

#autor
cursor.execute("INSERT INTO autor (jmeno, prijmeni, rodne_misto, pocet_knih, pocet_serii) VALUES ('Leigh','Bardugo', 'Jeruzalém', 15, 4 )")
cursor.execute("INSERT INTO autor (jmeno, prijmeni, rodne_misto, pocet_knih, pocet_serii) VALUES ('Lexi','Ryan', 'USA', 2, 1 )")
cursor.execute("INSERT INTO autor (jmeno, prijmeni, rodne_misto, pocet_knih, pocet_serii) VALUES ('Mary E.','Pearson', 'USA', 10, 3 )")

#spojovaci tabulka autor_kniha
cursor.execute("INSERT INTO kniha_autor (id_kniha, id_autor) VALUES (1, 1)")
cursor.execute("INSERT INTO kniha_autor (id_kniha, id_autor) VALUES (2, 2)")
cursor.execute("INSERT INTO kniha_autor (id_kniha, id_autor) VALUES (3, 3)")

#spojovaci tabulka kniha_prekladatel
cursor.execute("INSERT INTO kniha_prekladatel (id_kniha, id_prekladatel) VALUES (1, 1)")
cursor.execute("INSERT INTO kniha_prekladatel (id_kniha, id_prekladatel) VALUES (2, 3)")
cursor.execute("INSERT INTO kniha_prekladatel (id_kniha, id_prekladatel) VALUES (3, 2)")

#kniha
cursor.execute("INSERT INTO kniha (nazev, rok_vydani, serie) VALUES ('Šest Vran', 2015,'Šest Vran')")
cursor.execute("INSERT INTO kniha (nazev, rok_vydani, serie) VALUES ('Prázdné sliby', 2021,'Prázdné sliby')")
cursor.execute("INSERT INTO kniha (nazev, rok_vydani, serie) VALUES ('Falešný polibek', 2017,'Kroniky pozůstalých')")

#spojovaci tabulka kniha_zanr
cursor.execute("INSERT INTO kniha_zanr (id_kniha, id_zanr) VALUES (1, 1)")
cursor.execute("INSERT INTO kniha_zanr (id_kniha, id_zanr) VALUES (1, 2)")
cursor.execute("INSERT INTO kniha_zanr (id_kniha, id_zanr) VALUES (2, 1)")
cursor.execute("INSERT INTO kniha_zanr (id_kniha, id_zanr) VALUES (2, 2)")
cursor.execute("INSERT INTO kniha_zanr (id_kniha, id_zanr) VALUES (3, 1)")
cursor.execute("INSERT INTO kniha_zanr (id_kniha, id_zanr) VALUES (3, 2)")
cursor.execute("INSERT INTO kniha_zanr (id_kniha, id_zanr) VALUES (3, 4)")


#nakladatelstvi
cursor.execute("INSERT INTO nakladatelstvi (nazev, rok_zalozeni, majitel_jmeno, majitel_primeni) VALUES ('Fragment', 1991, 'Jan', 'Eisler')")
cursor.execute("INSERT INTO nakladatelstvi (nazev, rok_zalozeni, majitel_jmeno, majitel_primeni) VALUES ('CooBoo', 2009 , 'Tereza', 'Eliášová')")

#prekladatel
cursor.execute("INSERT INTO prekladatel (jmeno, prijmeni, pocet_knih) VALUES ('Julie', 'Žemlová', 16)")
cursor.execute("INSERT INTO prekladatel (jmeno, prijmeni, pocet_knih) VALUES ('Jana', 'Jašová', 389)")
cursor.execute("INSERT INTO prekladatel (jmeno, prijmeni, pocet_knih) VALUES ('Kristýna', 'Suchomelová', 9)")

#zanr
cursor.execute("INSERT INTO zanr (zanr) VALUES ('Fantasy')")
cursor.execute("INSERT INTO zanr (zanr) VALUES ('YA')")
cursor.execute("INSERT INTO zanr (zanr) VALUES ('Sci-Fy')")
cursor.execute("INSERT INTO zanr (zanr) VALUES ('Romance')")
cursor.execute("INSERT INTO zanr (zanr) VALUES ('Mystery')")
cursor.execute("INSERT INTO zanr (zanr) VALUES ('Horror')")

#spojovaci tabulka kniha nakladatelstvi
cursor.execute("INSERT INTO kniha_nakladatelstvi (id_kniha, id_nakladatelstvi) VALUES (1, 1)")
cursor.execute("INSERT INTO kniha_nakladatelstvi (id_kniha, id_nakladatelstvi) VALUES (2, 2)")
cursor.execute("INSERT INTO kniha_nakladatelstvi (id_kniha, id_nakladatelstvi) VALUES (3, 2)")




print("done")



connection.commit()
connection.close()