from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import text
import os

app = Flask(__name__)

# Env vars (prefer POSTGRES_*, aceita MYSQL_* como fallback)
user = os.getenv("POSTGRES_USER") or os.getenv("MYSQL_USERNAME", "pguser")
password = os.getenv("POSTGRES_PASSWORD") or os.getenv("MYSQL_PASSWORD", "pgpass")
address = os.getenv("POSTGRES_ADDRESS") or os.getenv("MYSQL_ADDRESS", "db:5432")
dbname = os.getenv("POSTGRES_DBNAME") or os.getenv("MYSQL_DBNAME", "docker_e_kubernetes")

host, port = (address.split(":", 1) + ["5432"])[:2]
app.config["SQLALCHEMY_DATABASE_URI"] = f"postgresql+psycopg2://{user}:{password}@{host}:{port}/{dbname}"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)

@app.get("/health")
def health():
    try:
        db.session.execute(text("SELECT 1"))
        return "OK", 200
    except Exception as e:
        return f"DB DOWN: {e}", 500

@app.get("/")
def root():
    try:
        total = db.session.execute(text("SELECT COUNT(*) FROM atividade02")).scalar()
        return jsonify(status="ok", rows=total)
    except Exception as e:
        return jsonify(status="error", error=str(e)), 500

@app.get("/people")
def people():
    rows = db.session.execute(
        text("SELECT id, firstname, lastname, age, height FROM atividade02 ORDER BY id")
    ).mappings().all()
    return jsonify([dict(r) for r in rows])

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8200)
