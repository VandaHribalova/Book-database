from flask import Flask, render_template, request, redirect, flash, url_for, make_response, jsonify, session
import sqlite3

app = Flask(__name__)
app.secret_key = '27ceea1d6b635a05fd713ce9a0c02468'


#web
@app.route("/")
@app.route("/home")
def home():
    db = sqlite3.connect("knihovna.db")
    cursor = db.cursor()
    cursor.execute("SELECT MAX(kniha_id) FROM kniha")
    book_id_result = cursor.fetchone()
    cursor.execute(f"""
        SELECT
            kniha.nazev,
            rok_vydani,
            serie,
            nakladatelstvi.nazev,
            zanr.zanr,
            prekladatel.jmeno AS prekladatel_jmeno,
            prekladatel.prijmeni AS prekladatel_prijmeni,
            autor.jmeno AS autor_jmeno,
            autor.prijmeni AS autor_prijmeni,
            autor.autor_id,
            nakladatelstvi.nakladatelstvi_id,
            prekladatel.prekladatel_id
        FROM
            kniha
            LEFT JOIN kniha_nakladatelstvi ON kniha.kniha_id = kniha_nakladatelstvi.id_kniha
            LEFT JOIN nakladatelstvi ON kniha_nakladatelstvi.id_nakladatelstvi = nakladatelstvi.nakladatelstvi_id
            LEFT JOIN kniha_zanr ON kniha.kniha_id = kniha_zanr.id_kniha
            LEFT JOIN zanr ON kniha_zanr.id_zanr = zanr.zanr_id
            LEFT JOIN kniha_prekladatel ON kniha.kniha_id = kniha_prekladatel.id_kniha
            LEFT JOIN prekladatel ON kniha_prekladatel.id_prekladatel = prekladatel.prekladatel_id
            LEFT JOIN kniha_autor ON kniha.kniha_id = kniha_autor.id_kniha
            LEFT JOIN autor ON kniha_autor.id_autor = autor.autor_id
        WHERE
            kniha_id LIKE '%{book_id_result[0]}%'
    """)
    
    book_result = cursor.fetchall()
    return render_template("home.html", info=book_result)

@app.route("/search", methods=["GET", "POST"])
def search():
    if request.method == "GET":
        return render_template("search_form.html")
    else:
        query = request.form.get("search")
        db = sqlite3.connect("knihovna.db")
        cursor = db.cursor()
        cursor.execute(f'SELECT autor_id,jmeno,prijmeni FROM autor WHERE jmeno LIKE ? OR prijmeni LIKE ?', ('%' + query + '%', '%' + query + '%'))
        result_set_author = cursor.fetchall()
        cursor.execute(f'SELECT prekladatel_id, jmeno,prijmeni FROM prekladatel WHERE jmeno LIKE ? OR prijmeni LIKE ?', ('%' + query + '%', '%' + query + '%'))
        result_set_translator = cursor.fetchall()
        cursor.execute(f'SELECT kniha_id,nazev FROM kniha WHERE nazev LIKE "%{query}%"')
        result_set_book = cursor.fetchall()
        cursor.execute(f'SELECT nakladatelstvi_id,nazev FROM nakladatelstvi WHERE nazev LIKE "%{query}%"')
        result_set_publisher = cursor.fetchall()
        return render_template("result.html", author=result_set_author, translators=result_set_translator, books=result_set_book, publishers=result_set_publisher)
    

@app.route("/book")
def book():
    db = sqlite3.connect("knihovna.db")
    cursor = db.cursor()
    cursor.execute("SELECT * FROM kniha")
    result_set_books = cursor.fetchall()
    cursor.execute("SELECT kniha_id FROM kniha")
    result_set_id = cursor.fetchall()
    return render_template("book.html", books=result_set_books, id = result_set_id)


@app.route("/author")
def author():
    db = sqlite3.connect("knihovna.db")
    cursor = db.cursor()
    cursor.execute("SELECT * FROM autor")
    result_set = cursor.fetchall()
    return render_template("author.html", authors=result_set)


@app.route("/author/<author_id>")
def author_detail(author_id):
    author_id = author_id.strip(',()[]')
    db = sqlite3.connect("knihovna.db")
    cursor = db.cursor()
    cursor.execute(f"SELECT * FROM autor WHERE autor_id LIKE '%{author_id}%' ")
    result_set = cursor.fetchall()
    return render_template("author_detail.html", author_details=result_set)



@app.route("/book/<book_id>")
def book_detail(book_id):
    book_id = book_id.strip(',()[]')
    db = sqlite3.connect("knihovna.db")
    cursor = db.cursor()
    cursor.execute(f"""
        SELECT
            kniha.nazev,
            rok_vydani,
            serie,
            nakladatelstvi.nazev,
            zanr.zanr,
            prekladatel.jmeno AS prekladatel_jmeno,
            prekladatel.prijmeni AS prekladatel_prijmeni,
            autor.jmeno AS autor_jmeno,
            autor.prijmeni AS autor_prijmeni,
            autor.autor_id,
            nakladatelstvi.nakladatelstvi_id,
            prekladatel.prekladatel_id
        FROM
            kniha
            LEFT JOIN kniha_nakladatelstvi ON kniha.kniha_id = kniha_nakladatelstvi.id_kniha
            LEFT JOIN nakladatelstvi ON kniha_nakladatelstvi.id_nakladatelstvi = nakladatelstvi.nakladatelstvi_id
            LEFT JOIN kniha_zanr ON kniha.kniha_id = kniha_zanr.id_kniha
            LEFT JOIN zanr ON kniha_zanr.id_zanr = zanr.zanr_id
            LEFT JOIN kniha_prekladatel ON kniha.kniha_id = kniha_prekladatel.id_kniha
            LEFT JOIN prekladatel ON kniha_prekladatel.id_prekladatel = prekladatel.prekladatel_id
            LEFT JOIN kniha_autor ON kniha.kniha_id = kniha_autor.id_kniha
            LEFT JOIN autor ON kniha_autor.id_autor = autor.autor_id
        WHERE
            kniha_id LIKE '%{book_id}%'
    """)

    result_set = cursor.fetchall()
    return render_template("book_detail.html", book_details=result_set)


@app.route("/add_author", methods=["GET", "POST"])
def add_author():
    book_id_info = session.get('book_id_info', {})
    bookid = book_id_info.get('bookid')
    need_of_publisher = book_id_info.get('need_of_publisher')
    need_of_translator = book_id_info.get('need_of_translator')
    
    if request.method == "POST":
        
        author = request.form.get("autor")
        breaks = author.split()
        author_name = breaks[0]
        author_surname = breaks[1]
        bornplace = request.form.get("rodne_misto")
        booknumber = request.form.get("pocet_knih")
        seriesnumber = request.form.get("pocet_serii")

        db = sqlite3.connect("knihovna.db")
        cursor = db.cursor()
        cursor.execute("INSERT INTO autor (jmeno, prijmeni,rodne_misto,pocet_knih,pocet_serii) VALUES (?, ?, ?, ?, ?)", (author_name, author_surname,bornplace, booknumber, seriesnumber ))
        cursor.execute(f"SELECT autor_id FROM autor WHERE prijmeni LIKE '%{author_surname}%'")
        author_result = cursor.fetchone()
        cursor.execute("INSERT INTO kniha_autor (id_kniha, id_autor) VALUES (?, ?)", (bookid[0], author_result[0]))
        db.commit()
        db.close()
        flash("author added successfully!",  "success")
        
        if need_of_publisher is True:
            need_of_publisher = False
            return redirect(url_for("add_publisher"))
        elif need_of_publisher is False and need_of_translator is True:
            need_of_translator = False
            return redirect(url_for("add_translator"))
        else:
            return redirect(url_for("book"))

    return render_template("add_author.html")

@app.route("/add_publisher", methods=["GET", "POST"])
def add_publisher():
    book_id_info = session.get('book_id_info', {})
    bookid = book_id_info.get('bookid')
    need_of_translator = book_id_info.get('need_of_translator')

    if request.method == "POST":
        
        publisher = request.form.get("nakladatelstvi")
        year = request.form.get("rok_zalozeni")
        owner = request.form.get("majitel")
        breaks = owner.split()
        owner_name = breaks[0]
        owner_surname = breaks[1]

        db = sqlite3.connect("knihovna.db")
        cursor = db.cursor()
        cursor.execute("INSERT INTO nakladatelstvi (nazev, rok_zalozeni, majitel_jmeno, majitel_primeni) VALUES (?, ?, ?, ?)", (publisher, year,owner_name, owner_surname))
        
        cursor.execute(f"SELECT nakladatelstvi_id FROM nakladatelstvi WHERE nazev LIKE '%{publisher}%'")
        db.commit()
        publisher_result = cursor.fetchone()
        cursor.execute("INSERT INTO kniha_nakladatelstvi (id_kniha, id_nakladatelstvi) VALUES (?, ?)", (bookid[0], publisher_result[0]))
        flash("publisher added successfully!",  "success")
        db.commit()
        db.close()
        if need_of_translator is True:
            need_of_translator = False
            return redirect(url_for("add_translator"))
        else:
            return redirect(url_for("book"))

    return render_template("add_publisher.html")


@app.route("/add_book", methods=["GET", "POST"])
def add_book():
    if request.method == "POST":
        need_of_translator = False
        need_of_publisher = False
        title = request.form.get("nazev")
        year = request.form.get("rok_vydani")
        series = request.form.get("serie")
        genre = request.form.get("zanr")
        publisher = request.form.get("nakladatelstvi")
        translator = request.form.get("prekladatel")
        breaks = translator.split()
        translator_surname = breaks[1]
        author = request.form.get("autor")
        breaks = author.split()
        author_surname = breaks[1]
        db = sqlite3.connect("knihovna.db")
        cursor = db.cursor()


        cursor.execute(f"SELECT kniha_id FROM kniha WHERE nazev LIKE '%{title}%'")
        book_result = cursor.fetchone()


        
        if book_result is None:
            cursor.execute("INSERT INTO kniha (nazev, rok_vydani, serie) VALUES (?, ?, ?)", (title, year, series))
            cursor.execute(f"SELECT kniha_id FROM kniha WHERE nazev LIKE '%{title}%'")
            result_book_id = cursor.fetchone()
            db.commit()
        
            cursor.execute(f"SELECT zanr_id FROM zanr WHERE zanr LIKE '%{genre}%'")
            zanr = cursor.fetchone()
            cursor.execute("INSERT INTO kniha_zanr (id_kniha, id_zanr) VALUES (?, ?)", (result_book_id[0], zanr[0]))


            cursor.execute(f"SELECT nakladatelstvi_id FROM nakladatelstvi WHERE nazev LIKE '%{publisher}%'")
            publisher_result = cursor.fetchone()
            if publisher_result is None:
                need_of_publisher = True
            else:
                cursor.execute("INSERT INTO kniha_nakladatelstvi (id_kniha, id_nakladatelstvi) VALUES (?, ?)", (result_book_id[0], publisher_result[0]))

            cursor.execute(f"SELECT prekladatel_id FROM prekladatel WHERE prijmeni LIKE '%{translator_surname}%'")
            translator_result = cursor.fetchone()
            if translator_result is None:
                need_of_translator = True
            else:
                cursor.execute("INSERT INTO kniha_prekladatel (id_kniha, id_prekladatel) VALUES (?, ?)", (result_book_id[0], translator_result[0]))

            session['book_id_info'] = {'bookid': result_book_id, 'need_of_publisher': need_of_publisher, 'need_of_translator': need_of_translator}

            cursor.execute(f"SELECT autor_id FROM autor WHERE prijmeni LIKE '%{author_surname}%'")
            author_result = cursor.fetchone()
            if author_result is None:                  
                flash("Author not found. Please provide author details.", "warning")
                db.close()
                return redirect(url_for("add_author"))
            else:
                cursor.execute("INSERT INTO kniha_autor (id_kniha, id_autor) VALUES (?, ?)", (result_book_id[0], author_result[0]))



            if need_of_publisher is True:
                flash("Publisher not found. Please provide publisher details.", "warning")
                db.commit()
                db.close()
                return redirect(url_for("add_publisher"))

            
            if need_of_translator is True:  
                flash("translator not found. Please provide translator details.", "warning")
                db.commit()
                db.close()
                return redirect(url_for("add_translator"))

            db.commit()
            db.close()
            flash("Book added successfully!",  "success")
            return redirect(url_for("book"))     


        else:
            flash("Book already exists!",  "warning")

        
        
    genres = ["Fantasy", "YA", "Sci-Fy", "Romance", "Mystery", "Horror"]
    return render_template("add_book.html", genres=genres)

@app.route("/add_translator", methods=["GET", "POST"])
def add_translator():
    book_id_info = session.get('book_id_info', {})
    bookid = book_id_info.get('bookid')
    

    if request.method == "POST":
        
        translator = request.form.get("prekladatel")
        number = request.form.get("pocet_knih")
        breaks = translator.split()
        translator_name = breaks[0]
        translator_surname = breaks[1]

        db = sqlite3.connect("knihovna.db")
        cursor = db.cursor()
        cursor.execute("INSERT INTO prekladatel (jmeno, prijmeni, pocet_knih) VALUES (?, ?, ?)", (translator_name, translator_surname, number))
        cursor.execute(f"SELECT prekladatel_id FROM prekladatel WHERE prijmeni LIKE '%{translator_surname}%'")
        translator_result = cursor.fetchone()
        cursor.execute("INSERT INTO kniha_prekladatel (id_kniha, id_prekladatel) VALUES (?, ?)", (bookid[0], translator_result[0]))
        db.commit()
        db.close()
        flash("translator added successfully!",  "success")
        return redirect(url_for("book"))

    return render_template("add_translator.html")


@app.route("/publisher/<publisher_id>")
def publisher_detail(publisher_id):
    publisher_id = publisher_id.strip(',()[]')
    db = sqlite3.connect("knihovna.db")
    cursor = db.cursor()
    cursor.execute(f"SELECT * FROM nakladatelstvi WHERE nakladatelstvi_id LIKE '%{publisher_id}%' ")
    result_set = cursor.fetchall()
    return render_template("publisher_detail.html", publisher_details=result_set)


@app.route("/translator/<translator_id>")
def translator_detail(translator_id):
    translator_id = translator_id.strip(',()[]')
    db = sqlite3.connect("knihovna.db")
    cursor = db.cursor()
    cursor.execute(f"SELECT * FROM prekladatel WHERE prekladatel_id LIKE '%{translator_id}%' ")
    result_set = cursor.fetchall()
    return render_template("translator_detail.html", translator_details=result_set)

    




#API
@app.route('/api/books')
def api_get_books():
    db = sqlite3.connect("knihovna.db")
    cursor = db.cursor()
    cursor.execute("SELECT nazev FROM kniha")
    book_list = cursor.fetchall()
    return make_response(jsonify(book_list), 200)


@app.route('/api/authors')
def api_get_authors():
    db = sqlite3.connect("knihovna.db")
    cursor = db.cursor()
    cursor.execute("SELECT jmeno, prijmeni FROM autor")
    author_list = cursor.fetchall()
    return make_response(jsonify(author_list), 200)


@app.route('/api/book')
def api_book():
    name = request.args.get('name')
    db = sqlite3.connect("knihovna.db")
    cursor = db.cursor()
    cursor.execute(f"SELECT * FROM kniha WHERE nazev LIKE '%{name}%' ")
    book_details = cursor.fetchall()
    return make_response(jsonify({'books': book_details}), 200)


@app.route('/api/author')
def api_author():
    name = request.args.get('name')
    last_name = request.args.get('last_name')
    db = sqlite3.connect("knihovna.db")
    cursor = db.cursor()
    cursor.execute(f"SELECT * FROM autor WHERE jmeno LIKE '%{name}%' OR prijmeni LIKE '%{last_name}%'") 
    author_details = cursor.fetchall() 
    return make_response(jsonify(author_details), 200)


@app.route('/api/search', methods=['GET'])
def api_search():
    query = request.args.get('query')
    db = sqlite3.connect("knihovna.db")
    cursor = db.cursor()
    cursor.execute(f"SELECT * FROM kniha WHERE nazev LIKE '%{query}%' OR serie LIKE '%{query}%'")
    kniha_results = cursor.fetchone()
    cursor.execute(f"SELECT * FROM autor WHERE jmeno LIKE '%{query}%' OR prijmeni LIKE '%{query}%'")
    autor_results = cursor.fetchone()
    cursor.execute(f"SELECT * FROM prekladatel WHERE jmeno LIKE '%{query}%' OR prijmeni LIKE '%{query}%'")
    prekladatel_results = cursor.fetchone()
    cursor.execute(f"SELECT * FROM nakladatelstvi WHERE majitel_jmeno LIKE '%{query}%' OR majitel_primeni LIKE '%{query}%' OR nazev LIKE '%{query}%'")
    nakladatelstvi_results = cursor.fetchone()
    if kniha_results is None and autor_results is None and prekladatel_results is None and nakladatelstvi_results is None:
        return make_response(jsonify({'message': 'No results found'}), 404)
    return make_response(jsonify(kniha_results, autor_results, prekladatel_results, nakladatelstvi_results), 200)


@app.route('/api/publisher')
def api_publisher():
    name = request.args.get('name')
    db = sqlite3.connect("knihovna.db")
    cursor = db.cursor()
    cursor.execute(f"SELECT * FROM nakladatelstvi WHERE nazev LIKE '%{name}%'")
    publisher_details = cursor.fetchall()
    return make_response(jsonify(publisher_details), 200)




@app.route('/api/add_book', methods=['POST'])
def api_add_book():
    name = request.args.get('name')
    series = request.args.get('serie')
    author_name = request.args.get('author_name')
    author_surname = request.args.get('author_surname')
    publisher = request.args.get('publisher')
    translator_name = request.args.get('translator_name')
    translator_surname = request.args.get('translator_surname')
    year = request.args.get('year')
    db = sqlite3.connect("knihovna.db")
    cursor = db.cursor()

    cursor.execute(f"SELECT kniha_id FROM kniha WHERE nazev LIKE '%{name}%'")
    existing_book = cursor.fetchone()

    if existing_book is None:

        cursor.execute(f"SELECT nakladatelstvi_id FROM nakladatelstvi WHERE nazev LIKE '%{publisher}%'")
        publisher_result = cursor.fetchone()
        if publisher_result is None:
            cursor.execute("INSERT INTO nakladatelstvi (nazev) VALUES (?)", (publisher))
            cursor.execute(f"SELECT nakladatelstvi_id FROM nakladatelstvi WHERE nazev LIKE '%{publisher}%'")
            publisher_result = cursor.fetchone()

        cursor.execute(f"SELECT autor_id FROM autor WHERE prijmeni LIKE '%{author_surname}%'")
        author_result = cursor.fetchone()
        if author_result is None:
            cursor.execute("INSERT INTO autor (jmeno, prijmeni) VALUES (?, ?)", (author_name, author_surname))
            cursor.execute(f"SELECT autor_id FROM autor WHERE prijmeni LIKE '%{author_surname}%'")
            author_result = cursor.fetchone()
        
        cursor.execute(f"SELECT prekladatel_id FROM prekladatel WHERE prijmeni LIKE '%{translator_surname}%'")
        translator_result = cursor.fetchone()
        if translator_result is None:
            cursor.execute("INSERT INTO prekladatel (jmeno, prijmeni) VALUES (?, ?)", (translator_name, translator_surname))
            cursor.execute(f"SELECT prekladatel_id FROM prekladatel WHERE prijmeni LIKE '%{translator_surname}%'")
            translator_result = cursor.fetchone()

        cursor.execute("INSERT INTO kniha (nazev, rok_vydani, serie) VALUES (?, ?, ?)",(name, year, series))
        cursor.execute(f"SELECT kniha_id FROM kniha WHERE nazev LIKE '%{name}%'")
        book_result = cursor.fetchone()

        cursor.execute("INSERT INTO kniha_autor (id_kniha, id_autor) VALUES (?, ?)", (book_result[0], author_result[0]))
        cursor.execute("INSERT INTO kniha_prekladatel (id_kniha, id_prekladatel) VALUES (?, ?)", (book_result[0], translator_result[0]))
        cursor.execute("INSERT INTO kniha_nakladatelstvi (id_kniha, id_nakladatelstvi ) VALUES (?, ?)", (book_result[0], publisher_result[0]))
        db.commit()
        db.close()

        return make_response(jsonify({'success': 'Book added'}), 200)
    else:
        db.close()
        return make_response(jsonify({'error': 'Book already exists'}), 400)


        
@app.route('/api/translator')
def api_translator():
    name = request.args.get('name')
    last_name = request.args.get('last_name')
    db = sqlite3.connect("knihovna.db")
    cursor = db.cursor()
    cursor.execute(f"SELECT * FROM prekladatel WHERE jmeno LIKE '%{name}%' OR prijmeni LIKE '%{last_name}%' ")
    translator_details = cursor.fetchall()
    return make_response(jsonify(translator_details), 200)




if __name__ == "__main__":
    app.run(debug=True)



