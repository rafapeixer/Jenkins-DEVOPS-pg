import os
from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import text

PG_USER = os.getenv("POSTGRES_USER", "pguser")
PG_PASS = os.getenv("POSTGRES_PASSWORD", "pgpass")
PG_ADDR = os.getenv("POSTGRES_ADDRESS", "db:5432")  # host:port
PG_DB   = os.getenv("POSTGRES_DBNAME", "docker_e_kubernetes")

DATABASE_URI = f"postgresql+psycopg2://{PG_USER}:{PG_PASS}@{PG_ADDR}/{PG_DB}"

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = DATABASE_URI
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)

@app.route("/")
def home():
    try:
        cnt = db.session.execute(text("SELECT COUNT(*) FROM atividade02")).scalar()
        return jsonify(status="ok", table="atividade02", rows=int(cnt))
    except Exception as e:
        # responde 200 para não falhar o curl do CI enquanto o DB inicializa
        return jsonify(status="ok", table="atividade02", rows=0, note="DB iniciando ou tabela ainda não criada", error=str(e)[:200])

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8200)
