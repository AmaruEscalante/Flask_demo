from flask import Flask, render_template, request, redirect, flash, url_for, sessions
import sqlite3

app = Flask(__name__)
app.secret_key = 'super secret key'


conn = sqlite3.connect('contactos.db')
conn.execute('CREATE TABLE IF NOT EXISTS contactos (id INTEGER PRIMARY KEY AUTOINCREMENT, nombre TEXT, telefono TEXT, email TEXT)')

secretkey = "secretkey"

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
                cur.execute("INSERT INTO contactos (nombre, telefono, email) VALUES (?,?,?)", (nomb, telf, email))
                con.commit()
                msg = "Record succesfully added"
        except:
            con.rollback()
            msg = "error in insert operation"

        finally:
            flash(msg)
            return redirect(url_for('index'))
            con.close()

    return redirect(url_for('index'))


@app.route('/edit/<id>')
def edit_contact(id):
    conn = sqlite3.connect('contactos.db')
    print('Opened db succesfully')
    cur = conn.cursor()
    cur.execute('SELECT * FROM contactos WHERE id = ?',(id))
    data = cur.fetchall()
    print(data[0])
    return render_template('edit.html', contacto=data[0])


@app.route('/delete/<string:id>')
def delete_contact(id):
    # nom = request.form['nombres']
    # telf = request.form['telefono']
    # email = request.form['email']
    # print('DELETE', id, nom, telf, email)
    conn = sqlite3.connect('contactos.db')
    cur = conn.cursor()
    cur.execute("DELETE FROM contactos where id = ?",(id))
    conn.commit()
    flash('Contact deleted succesfully')
    return redirect(url_for('index'))


@app.route('/update/<id>', methods=['POST'])
def update_contact(id):
    if request.method == 'POST':
        nom = request.form['nombres']
        telf = request.form['telefono']
        email = request.form['email']
        print('UPDATE', id, nom, telf, email)
        conn = sqlite3.connect('contactos.db')
        print('Opened db succesfully')
        cur = conn.cursor()
        cur.execute("update contactos set nombre = ?,telefono = ?,email = ? where id = ?",(nom,telf,email, id))
        conn.commit()
        flash('Contact modified succesfully')
        return redirect(url_for('index'))


if __name__ == '__main__':
    app.run()
