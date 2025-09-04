from flask import Flask, jsonify
import os
import time
import psycopg2

app = Flask(__name__)

def db_conn():
    host_port = os.getenv("POSTGRES_ADDRESS", "db:5432")
    host, port = host_port.split(":")
    return psycopg2.connect(
        host=host,
        port=port,
        user=os.getenv("POSTGRES_USER", "pguser"),
        password=os.getenv("POSTGRES_PASSWORD", "pgpass"),
        dbname=os.getenv("POSTGRES_DBNAME", "docker_e_kubernetes"),
    )

@app.route("/")
def home():
    # tentativas rápidas para o caso do DB ainda estar subindo
    for _ in range(10):
        try:
            with db_conn() as con, con.cursor() as cur:
                cur.execute('SELECT COUNT(*) FROM atividade02')
                n = cur.fetchone()[0]
                return jsonify(ok=True, registros=n)
        except Exception as e:
            time.sleep(1)
            last = str(e)
    return jsonify(ok=False, error=last), 503

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8200)
