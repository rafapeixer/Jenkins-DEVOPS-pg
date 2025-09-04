from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os

def build_pg_uri():
    user = os.getenv("POSTGRES_USER", "pguser")
    pwd = os.getenv("POSTGRES_PASSWORD", "pgpass")
    addr = os.getenv("POSTGRES_ADDRESS", "db:5432")
    dbname = os.getenv("POSTGRES_DBNAME", "docker_e_kubernetes")
    if ":" in addr:
        host, port = addr.split(":", 1)
    else:
        host, port = addr, "5432"
    return f"postgresql+psycopg2://{user}:{pwd}@{host}:{port}/{dbname}"

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = build_pg_uri()
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)

class Pessoa(db.Model):
    __tablename__ = "atividade02"
    id = db.Column(db.Integer, primary_key=True)
    firstname = db.Column(db.String(30), nullable=False)
    lastname = db.Column(db.String(100))
    age = db.Column(db.Integer)
    height = db.Column(db.Numeric(4, 2))

@app.get("/health")
def health():
    # Tenta selecionar 1 linha só pra validar conexão
    db.session.execute(db.text("SELECT 1"))
    return {"status": "ok"}

@app.get("/")
def index():
    total = db.session.execute(db.text("SELECT COUNT(*) FROM atividade02")).scalar_one()
    rows = db.session.execute(db.text(
        "SELECT id, firstname, lastname, age, height FROM atividade02 ORDER BY id LIMIT 5"
    )).mappings().all()
    preview = [dict(r) for r in rows]
    return {"total": total, "preview": preview}

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=8200)
