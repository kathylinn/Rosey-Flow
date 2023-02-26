from flask import Flask, render_template, request
import pandas as pd

app = Flask(__name__)

@app.route('/', methods=['GET'])
def index():
    return render_template('base.html')

@app.route('/moreinfo')
def moreinfo():
  return render_template("moreinfo.html")

@app.route('/aboutus')
def aboutus():
  return render_template("aboutus.html")

@app.route('/submit', methods=['GET','POST'])
def submit():
    fname = request.form['fname']
    lname = request.form['lname']
    email = request.form['email']
    phoneno = request.form['phoneno']
    lastperiod = request.form['lastperiod']

    row = pd.DataFrame([[fname, lname, email, phoneno, lastperiod]])

    row.to_csv('csv/users.csv', mode='a')

    return render_template('base.html')


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=8080, debug=True)


