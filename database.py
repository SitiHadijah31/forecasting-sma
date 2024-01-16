from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class data_train(db.Model):
    __tablename__ = 'data_train'
    Date = db.Column(db.Date, primary_key=True)
    Open = db.Column(db.Integer)
    High = db.Column(db.Integer)
    Low = db.Column(db.Integer)
    Close = db.Column(db.Integer)
    Adj = db.Column(db.Integer)
    Volume = db.Column(db.Integer)
    # Definisikan kolom lain sesuai dengan struktur tabel

class data_test(db.Model):
    __tablename__ = 'data_test'
    Date = db.Column(db.Date, primary_key=True)
    Close = db.Column(db.Integer)

class resultSMA(db.Model):
    __tablename__ = 'result'
    id = db.Column(db.Integer, primary_key=True)
    Date = db.Column(db.Date)
    Close = db.Column(db.Integer)
    Result = db.Column(db.Integer)
