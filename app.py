from flask import Flask,render_template,request
from flask_sqlalchemy import SQLAlchemy
import random
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////Users/Enes/Documents/Projects/kura-app/kura.db'
db = SQLAlchemy(app)
db.create_all()

@app.route("/")
def index():
    return render_template("index.html")


@app.route("/result", methods = ["POST"])
def result():
    varlik = request.form.get("varlik").split()
    baslik = request.form.get("baslik")
    asilSayi = int(request.form.get("asil"))
    yedekSayi = int(request.form.get("yedek"))
    tarih = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    asilList = []
    yedekList = []
    if (asilSayi+yedekSayi) <= len(varlik):
        for i in range(asilSayi):
            item = varlik[random.randint(0,len(varlik)-1)]
            if item not in asilList:
                asilList.append(item)
                varlik.remove(item)
        for i in range(yedekSayi):
            item = varlik[random.randint(0,len(varlik)-1)]
            if item not in yedekList:
                yedekList.append(item)
                varlik.remove(item)
    data=[
    {
    'tarih' : tarih,
    'baslik': baslik,
    'asilList': asilList,
    'yedekList': yedekList,
    'asil': asilSayi,
    'yedek': yedekSayi
    }]
    asil = ",".join(asilList)
    yedek = ",".join(yedekList)
    kura = Kuralar(tarih = tarih, baslik =baslik,asil =asil, yedek = yedek)
    db.session.add(kura)
    db.session.commit()
    return render_template("result.html", data = data)

@app.route("/past")
def past():
    data = Kuralar.query.all()
    return render_template("past.html", data = data)

class Kuralar(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    tarih = db.Column(db.String(80), unique=False, nullable=False)
    baslik = db.Column(db.String(120), unique=False, nullable=False)
    asil = db.Column(db.String(120), unique=False, nullable=False)
    yedek = db.Column(db.String(120), unique=False, nullable=True)
    
    def __repr__(self):
        return '<User %r>' % self.username

if __name__ == "__main__":
    app.run(debug = True)