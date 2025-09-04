import os
from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

pg_user = os.getenv("POSTGRES_USER", "pguser")
pg_pass = os.getenv("POSTGRES_PASSWORD", "pgpass")
pg_addr = os.getenv("POSTGRES_ADDRESS", "db:5432")   # host:port
pg_db   = os.getenv("POSTGRES_DBNAME", "docker_e_kubernetes")

app.config["SQLALCHEMY_DATABASE_URI"] = f"postgresql+psycopg2://{pg_user}:{pg_pass}@{pg_addr}/{pg_db}"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)

class Atividade02(db.Model):
    __tablename__ = "atividade02"
    id = db.Column("id", db.Integer, primary_key=True)
    firstname = db.Column("firstname", db.String(30), nullable=False)
    lastname = db.Column("lastname", db.String(100))
    age = db.Column("age", db.Integer)
    height = db.Column("height", db.Numeric(4, 2))

@app.route("/")
def index():
    rows = Atividade02.query.order_by(Atividade02.id).all()
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
    return jsonify({"total": len(data), "items": data})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8200)
