from flask import Flask, render_template, request
from sense_hat import SenseHat 

sense = SenseHat()

app = Flask(__name__, static_folder="static")

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/send', methods=['POST'])
def sent():
    message = request.form['message']
    sense.show_message(message)
    return render_template('sent.html', message=message)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
