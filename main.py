from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)

addr = os.getenv("POSTGRES_ADDRESS", "db:5432")
host, port = addr.split(":")
user = os.getenv("POSTGRES_USER", "pguser")
password = os.getenv("POSTGRES_PASSWORD", "pgpass")
dbname = os.getenv("POSTGRES_DBNAME", "docker_e_kubernetes")

app.config["SQLALCHEMY_DATABASE_URI"] = (
    f"postgresql+psycopg2://{user}:{password}@{host}:{port}/{dbname}"
)
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)

@app.route("/")
def home():
    try:
        with db.engine.connect() as conn:
            # conta registros
            count = conn.execute(db.text("SELECT COUNT(*) FROM atividade02")).scalar()
            rows = conn.execute(db.text("SELECT id, firstname, lastname, age, height FROM atividade02 ORDER BY id LIMIT 5")).fetchall()
        html_rows = "".join(
            f"<li>#{r[0]} - {r[1]} {r[2]} | idade: {r[3]} | altura: {r[4]}</li>" for r in rows
        )
        return f"""
        <h1>CI/CD - Flask + Postgres</h1>
        <p>Conexão OK com <b>postgres</b>. Registros na tabela <code>atividade02</code>: <b>{count}</b>.</p>
        <p>Alguns registros:</p>
        <ul>{html_rows}</ul>
        """
    except Exception as e:
        return f"<h1>Erro</h1><pre>{e}</pre>", 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8200)
