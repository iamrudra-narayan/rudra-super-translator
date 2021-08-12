from flask import Flask,render_template,request,redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from googletrans import Translator
app = Flask(__name__)
app.config["SECRET_KEY"]= 'secret_key'
app.config["SQLALCHEMY_DATABASE_URI"] = 'sqlite:///translatorwebsite.db'
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False  
db = SQLAlchemy(app)

class Contacts(db.Model):
    Slno = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(40), nullable=False)
    subject = db.Column(db.String(100), nullable=False)
    msg = db.Column(db.String(500),nullable=False)
    date = db.Column(db.DateTime, default=datetime.utcnow)

@app.route("/",methods=["GET", "POST"])
def home():
    if request.method == "POST":
     t_sentence = request.form["sentence"]
     language = request.form['inputvalue']
     output = Translator().translate(t_sentence, dest=language)
    else:
        return render_template("home.html")
    return render_template('home.html',output=output,sentence=t_sentence)

@app.route('/contact', methods=["GET","POST"])
def contactdetailspage():
    if request.method=="POST":

      name = request.form['name']
      email = request.form['email']
      subject = request.form['subject']
      message  = request.form['message']

      entry = Contacts(name= name, email= email, subject= subject, msg= message)
      
      db.session.add(entry)
      db.session.commit()

    return render_template("home.html")  


@app.route("/admin", methods=["GET", "POST"])
def admin_post():
    if request.method == 'GET':
     post = Contacts.query.all()    
    return render_template('admin.html',post=post)

@app.route("/admin/delete/<int:Slno>")
def admin_post_delete(Slno):
    
    post = Contacts.query.filter_by(Slno=Slno).first()
    db.session.delete(post)
    db.session.commit()
    return redirect('/admin')


if __name__ == '__main__':
    app.run(debug=True)

