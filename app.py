from flask import Flask, render_template, request
from sense_hat import SenseHat 
import sqlite3 as lite
import sys


sense = SenseHat()

app = Flask(__name__, static_folder="static")

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/send', methods=['POST'])
def sent():
    #get posted form data using names assigned in HTML
    message = request.form['message']
    name = request.form['name']
    #generate string to display on Sense HAT
    display = message + " Love, " + name

    #connect to database and insert message and name
    conn = lite.connect('./data/inspiration_messages.db')
    curs=conn.cursor()
    curs.execute("INSERT INTO messages values((?), (?))", (name, message))
    conn.commit()

    #close database connection
    conn.close()

    #display message on Sense HAT
    sense.show_message(display)

    #display success message to sending user 
    return render_template('sent.html', message=message, name=name)

@app.route('/all')
def display_all():
    #connect to database
    conn = lite.connect('./data/inspiration_messages.db')
    curs=conn.cursor()

    #add all rows in messages table to messages list
    messages = []
    for row in curs.execute("SELECT * FROM messages"):
        messages.append({'name': row[0], 'message': row[1]})
    conn.close()

    #render template showing messages
    return render_template('all.html', messages=messages)

@app.route('/display', methods=['POST'])
def display():
    #get posted form data using name assigned in HTML
    display = request.form['message']

    #display message on Sense HAT
    sense.show_message(display)

    #display success message to sending user 
    return render_template('sent.html', message=display, name='you')


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
