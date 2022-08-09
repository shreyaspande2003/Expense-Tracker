from flask import Flask,render_template,request,url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime,date
today = date.today()

from werkzeug.utils import redirect
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///data.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Data(db.Model):
    sno = db.Column(db.Integer, primary_key = True )
    mode = db.Column(db.Text )
    name = db.Column(db.String(150))
    date = db.Column(db.Text)
    amount = db.Column(db.Integer)
    type = db.Column(db.String(50))


@app.route('/')
def home():
    return render_template('home.html')

@app.route('/expense',methods=['GET','POST'])
def expense():

    if request.method=="POST":
        mode = request.form['mode']
        name = request.form['item-name']
        type = request.form['type']
        date = request.form['date']
        amount = request.form['amount']
        data = Data(name = name ,date = date, amount=amount,mode = mode ,type = type)
        db.session.add(data)
        db.session.commit()
    alldata = Data.query.all()


    return render_template('expense.html',alldata=alldata)


@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/index')
def index():
    return render_template('index.html')

@app.route('/cashbook')
def cashbook():
    alldata = Data.query.all()
    debit = 0
    credit = 0
    for data in alldata:
        if data.type=="Debit":
            debit+=data.amount 
        else:
            credit+=data.amount

    return render_template('cashbook.html',alldata=alldata,debit=debit,credit= credit)


@app.route('/delete')
def delete():

    alldata = Data.query.all()
    for data in alldata:

        db.session.delete(data)
    db.session.commit()

    return redirect(url_for('cashbook'))

    
if __name__ == '__main__':
    app.run(debug=True)




