from flask import Flask, render_template, request
import sqlite3

app = Flask(__name__)

conn = sqlite3.connect('contactos.db')
# conn.execute('CREATE TABLE contactos (id INT auto_increment, nombre TEXT, telefono TEXT, email TEXT)')


@app.route('/')
def index():
    conn = sqlite3.connect('contactos.db')
    print('Opened db succesfully')
    cur = conn.cursor()
    cur.execute('select * from contactos')
    data = cur.fetchall()
    return render_template('index.html', contactos=data)


@app.route('/add_contact', methods=['POST', 'GET'])
def add_contact():
    if request.method == 'POST':
        try:
            nomb = request.form['nombres']
            telf = request.form['telefono']
            email = request.form['email']

            with sqlite3.connect("contactos.db") as con:
                cur = con.cursor()
                cur.execute("INSERT INTO contactos (nombre, telefono, email) VALUES (?,?,?)", (nomb,telf,email))
                con.commit()
                msg = "Record succesfully added"
        except:
            con.rollback()
            msg = "error in insert operation"

        finally:
            return render_template("index.html", msg = msg)
            con.close()


    return 'Contacto'


if __name__ == '__main__':
    app.run()
