from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import text
import os, time

app = Flask(__name__)

PG_USER = os.getenv("POSTGRES_USER", "pguser")
PG_PASS = os.getenv("POSTGRES_PASSWORD", "pgpass")
PG_ADDR = os.getenv("POSTGRES_ADDRESS", "db:5432")
PG_DB   = os.getenv("POSTGRES_DBNAME", "docker_e_kubernetes")

app.config["SQLALCHEMY_DATABASE_URI"] = f"postgresql+psycopg2://{PG_USER}:{PG_PASS}@{PG_ADDR}/{PG_DB}"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)

@app.route("/")
def index():
    try:
        with db.engine.connect() as conn:
            # garante que a tabela existe caso rode sem seed
            conn.execute(text("""
                CREATE TABLE IF NOT EXISTS atividade02(
                  id INTEGER PRIMARY KEY,
                  firstname VARCHAR(30) NOT NULL,
                  lastname  VARCHAR(100),
                  age       INTEGER,
                  height    NUMERIC(4,2)
                );
            """))
            rows = conn.execute(text("SELECT id, firstname, lastname, age, height FROM atividade02 ORDER BY id LIMIT 20")).fetchall()
        html = ["<h1>Funciona!</h1>"]
        if not rows:
            html.append("<p>(Tabela vazia. O seed roda apenas na primeira inicialização do volume.)</p>")
        for r in rows:
            html.append(f"<div>{r.id} - {r.firstname} {r.lastname} | idade {r.age} | altura {r.height}</div>")
        return "\n".join(html)
    except Exception as e:
        return f"<h1>Algo quebrou.</h1><pre>{e}</pre>"

if __name__ == "__main__":
    # pequena espera se o container subir muito rápido
    time.sleep(1)
    app.run(host="0.0.0.0", port=8200)
