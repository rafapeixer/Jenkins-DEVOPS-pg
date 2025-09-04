import os
from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy

PG_HOSTPORT = os.getenv("POSTGRES_ADDRESS", "db:5432")
PG_USER     = os.getenv("POSTGRES_USER", "pguser")
PG_PASS     = os.getenv("POSTGRES_PASSWORD", "pgpass")
PG_DB       = os.getenv("POSTGRES_DB", "docker_e_kubernetes")

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = f"postgresql+psycopg2://{PG_USER}:{PG_PASS}@{PG_HOSTPORT}/{PG_DB}"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)

# Model ligado à tabela seedada
class Atividade02(db.Model):
    __tablename__ = "atividade02"
    id = db.Column(db.Integer, primary_key=True)
    firstname = db.Column(db.String(30), nullable=False)
    lastname = db.Column(db.String(100))
    age = db.Column(db.Integer)
    height = db.Column(db.Numeric(4, 2))

@app.route("/")
def home():
    try:
        rows = Atividade02.query.order_by(Atividade02.id).limit(5).all()
        data = [
            dict(
                id=r.id,
                firstname=r.firstname,
                lastname=r.lastname,
                age=r.age,
                height=float(r.height) if r.height is not None else None,
            )
            for r in rows
        ]
        return jsonify(
            status="ok",
            db=f"{PG_USER}@{PG_HOSTPORT}/{PG_DB}",
            sample=data
        )
    except Exception as e:
        return jsonify(status="error", message=str(e)), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8200)
