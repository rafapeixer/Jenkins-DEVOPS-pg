import os
from flask import Flask, jsonify
from sqlalchemy import create_engine, text

app = Flask(__name__)

DB_USER = os.getenv("POSTGRES_USER", "pguser")
DB_PASS = os.getenv("POSTGRES_PASSWORD", "pgpass")
DB_ADDR = os.getenv("POSTGRES_ADDRESS", "db:5432")   # host:port
DB_NAME = os.getenv("POSTGRES_DBNAME", "docker_e_kubernetes")

DATABASE_URL = f"postgresql+psycopg2://{DB_USER}:{DB_PASS}@{DB_ADDR}/{DB_NAME}"
engine = create_engine(DATABASE_URL, pool_pre_ping=True)

@app.get("/")
def root():
    return jsonify(status="ok", db=DB_NAME)

@app.get("/db")
def db_check():
    with engine.connect() as conn:
        count = conn.execute(text("SELECT COUNT(*) FROM atividade02")).scalar()
    return jsonify(table="atividade02", rows=int(count))

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8200, debug=False)
