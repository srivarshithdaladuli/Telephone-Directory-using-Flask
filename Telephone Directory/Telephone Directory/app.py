# import Libraries
from flask import Flask, render_template, request,redirect,url_for
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import os

tele = Flask(__name__)
##############Database Configuration ########################
basedir = os.path.abspath(os.path.dirname(__file__))
tele.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'logs.sqlite')
tele.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(tele)
Migrate(tele, db)
#############################################################

############## Model Creation ###############################
class Contacts(db.Model):
    __tablename__ = 'contacts'
    id = db.Column(db.Integer, primary_key = True)
    entry = db.Column(db.Text)
    phone = db.Column(db.Integer)

    def __init__(self, entry, phone):
        self.entry = entry
        self.phone = phone
    def __repr__(self):
        return "{}  {}".format(self.entry,self.phone)


#############################################################
@tele.route("/")
def layout():
    return render_template("layout.html")

@tele.route("/add", methods=['GET','POST'])
def add():
    if request.method == "POST":
        name = request.form.get("enter_name")
        phone = request.form.get("enter_phone_number")
        logs = Contacts(name,phone)
        db.session.add(logs)
        db.session.commit()
        print("Contact added Sucessfully")
        print(name, phone)
    return render_template("add2.html")



@tele.route("/display")
def display():
    info= Contacts.query.all()
    return render_template("display2.html",items_info=info)

@tele.route("/search",methods=["GET","POST"])
def search():
    inp = request.form.get("input")
    search = Contacts.query.filter_by(entry=inp).all()
    ##if search:
    return render_template("search.html",search1=search)
    ##return render_template("search.html")

@tele.route("/delete",methods=["GET","POST"])
def delete():
    inp1 = request.form.get("input1")
    log =Contacts.query.filter_by(entry=inp1).first()
    if log:
        db.session.delete(log)
        db.session.commit()
        return render_template("delete.html")
    return render_template("delete.html")

if __name__ == "__main__":
    db.create_all()
    tele.run(debug=True)
