from __future__ import annotations

import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, Integer, String, Float
from sqlalchemy.ext.declarative import declarative_base

def verifica_variaveis_ambiente():
    res = []
    chaves = ['POSTGRES_USER', 'POSTGRES_PASSWORD', 'POSTGRES_ADDRESS', 'POSTGRES_DBNAME']
    for chave in chaves:
        valor = os.environ.get(chave)
        if valor is None:
            print("Faltou a variável de ambiente", chave)
            raise SystemExit(1)
        res.append(valor)
    return res

db = SQLAlchemy()
app = Flask(__name__)

username, password, server, dbname = verifica_variaveis_ambiente()
userpass = f'postgresql+psycopg2://{username}:{password}@'

app.config['SQLALCHEMY_DATABASE_URI'] = userpass + server + '/' + dbname
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

Base = declarative_base()

class Usuario(Base):
    __tablename__ = 'atividade02'
    id = Column(Integer, primary_key=True)
    FirstName = Column(String(30), nullable=False)
    LastName = Column(String(100))
    Age = Column(Integer)
    Height = Column(Float)  # será NUMERIC(4,2) no banco

    def __str__(self) -> str:
        return f"{self.FirstName} {self.LastName}, {self.Age}, {self.Height}"

@app.route('/')
def testdb():
    try:
        a = db.session.query(Usuario).all()
        b = '<h1>Funciona!</h1>'
        for line in a:
            b += f"<h2>{line}</h2>"
        return b
    except Exception as e:
        return '<h1>Something is broken.</h1>' + "<h2>The error:<br>" + str(e) + "</h2>"

if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=8200)