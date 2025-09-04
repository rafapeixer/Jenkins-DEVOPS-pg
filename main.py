import os, time
from flask import Flask, jsonify
from sqlalchemy import create_engine, text

def db_url():
    user = os.getenv("POSTGRES_USER", "pguser")
    pwd  = os.getenv("POSTGRES_PASSWORD", "pgpass")
    addr = os.getenv("POSTGRES_ADDRESS", "db:5432")
    db   = os.getenv("POSTGRES_DBNAME", "docker_e_kubernetes")
    return f"postgresql+psycopg2://{user}:{pwd}@{addr}/{db}"

app = Flask(__name__)
engine = create_engine(db_url(), pool_pre_ping=True)

def wait_for_db(max_tries=30, delay=1):
    for i in range(1, max_tries + 1):
        try:
            with engine.connect() as conn:
                conn.execute(text("SELECT 1"))
            print(f"DB OK (tentativa {i})")
            return True
        except Exception as e:
            print(f"DB não pronto (tentativa {i}): {e}")
            time.sleep(delay)
    return False

@app.route("/health")
def health():
    try:
        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))
        return jsonify(status="ok"), 200
    except Exception as e:
        return jsonify(status="down", error=str(e)), 500

@app.route("/")
def index():
    with engine.connect() as conn:
        rows = conn.execute(
            text("SELECT id, firstname, lastname, age, height FROM atividade02 ORDER BY id LIMIT 10")
        ).mappings().all()
    return {"msg": "Hello, DevOps!", "total": len(rows), "sample": [dict(r) for r in rows]}, 200

if __name__ == "__main__":
    wait_for_db()
    app.run(host="0.0.0.0", port=int(os.getenv("PORT", "8200")))
