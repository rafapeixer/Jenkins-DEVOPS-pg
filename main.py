# main.py
from __future__ import annotations
import os
from typing import Any, Dict, List
from html import escape

from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import text

# =============================================================================
# Config de ambiente (PostgreSQL)
# =============================================================================
REQUIRED_ENVS = ["POSTGRES_USER", "POSTGRES_PASSWORD", "POSTGRES_ADDRESS", "POSTGRES_DBNAME"]
missing = [k for k in REQUIRED_ENVS if not os.getenv(k)]
if missing:
    raise SystemExit(f"Faltou a(s) variável(is) de ambiente: {', '.join(missing)}")

PG_USER = os.getenv("POSTGRES_USER")
PG_PASS = os.getenv("POSTGRES_PASSWORD")
PG_ADDR = os.getenv("POSTGRES_ADDRESS")   # ex.: "pg:5432"
PG_DB   = os.getenv("POSTGRES_DBNAME")    # ex.: "docker_e_kubernetes"

def build_pg_uri(user: str, pwd: str, addr: str, db: str) -> str:
    # Formato SQLAlchemy/psycopg2
    return f"postgresql+psycopg2://{user}:{pwd}@{addr}/{db}"

# =============================================================================
# App + SQLAlchemy (engine com pool estável)
# =============================================================================
app = Flask(__name__)
app.config.update(
    SQLALCHEMY_DATABASE_URI=build_pg_uri(PG_USER, PG_PASS, PG_ADDR, PG_DB),
    SQLALCHEMY_TRACK_MODIFICATIONS=False,
    SQLALCHEMY_ENGINE_OPTIONS={
        "pool_pre_ping": True,   # evita conexões zumbis
        "pool_recycle": 1800,    # recicla após 30min
        "pool_size": 5,
        "max_overflow": 5,
    },
)
db = SQLAlchemy(app)

# =============================================================================
# (Opcional) Telemetria Prometheus – descomente para expor /metrics
# =============================================================================
# try:
#     from prometheus_flask_exporter import PrometheusMetrics
#     metrics = PrometheusMetrics(app)
# except Exception:
#     # Não falhar se a lib não estiver instalada
#     pass

# =============================================================================
# Hooks de ciclo de vida
# =============================================================================
@app.teardown_appcontext
def shutdown_session(exception=None):
    # Limpa a sessão ao fim de cada request/erro
    db.session.remove()

# =============================================================================
# Rotas
# =============================================================================
@app.get("/health")
def health() -> Any:
    """
    Verifica conexão com o banco.
    Retorna: {"status": "ok"} ou {"status":"down","error": "..."}
    """
    try:
        db.session.execute(text("SELECT 1"))
        return jsonify({"status": "ok"}), 200
    except Exception as e:
        return jsonify({"status": "down", "error": str(e)}), 500

@app.get("/")
def index() -> Any:
    """
    Lista registros com paginação simples e total.
    Parâmetros: ?limit=5&offset=0
    Retorna JSON: {"total": N, "preview": [...]}
    """
    # Sanitização simples (default: 5/0)
    try:
        limit = max(1, min(100, int(request.args.get("limit", 5))))
    except Exception:
        limit = 5
    try:
        offset = max(0, int(request.args.get("offset", 0)))
    except Exception:
        offset = 0

    # COUNT total
    total = db.session.execute(text("SELECT COUNT(*) FROM atividade02")).scalar_one()

    # Preview paginado
    rows = db.session.execute(
        text("""
            SELECT id, firstname, lastname, age, height
            FROM atividade02
            ORDER BY id
            LIMIT :limit OFFSET :offset
        """),
        {"limit": limit, "offset": offset},
    ).mappings().all()

    preview: List[Dict[str, Any]] = [dict(r) for r in rows]
    return jsonify({"total": total, "preview": preview}), 200

@app.get("/ui")
def ui() -> Any:
    """
    Tabela HTML simples com até N registros (default 20).
    Parâmetros: ?limit=20&offset=0
    """
    try:
        limit = max(1, min(100, int(request.args.get("limit", 20))))
    except Exception:
        limit = 20
    try:
        offset = max(0, int(request.args.get("offset", 0)))
    except Exception:
        offset = 0

    rows = db.session.execute(
        text("""
            SELECT id, firstname, lastname, age, height
            FROM atividade02
            ORDER BY id
            LIMIT :limit OFFSET :offset
        """),
        {"limit": limit, "offset": offset},
    ).mappings().all()

    html = [
        "<!doctype html><meta charset='utf-8'>",
        "<style>body{font-family:Arial,Helvetica,sans-serif;margin:24px}table{border-collapse:collapse}th,td{border:1px solid #ddd;padding:8px}th{background:#f4f6f8}</style>",
        "<h1>Atividade02 (PostgreSQL)</h1>",
        f"<p><b>Total visualizado:</b> {len(rows)} &nbsp; <b>offset:</b> {offset}</p>",
        "<table><tr><th>ID</th><th>FirstName</th><th>LastName</th><th>Age</th><th>Height</th></tr>",
    ]
    for r in rows:
        html.append(
            "<tr>"
            f"<td>{r['id']}</td>"
            f"<td>{escape(str(r['firstname']))}</td>"
            f"<td>{escape(str(r['lastname']))}</td>"
            f"<td>{r['age']}</td>"
            f"<td>{r['height']}</td>"
            "</tr>"
        )
    html.append("</table>")
    html.append("<p><a href='/'>Ver JSON</a> | <a href='/health'>Health</a></p>")
    return "".join(html), 200

# =============================================================================
# Bootstrap local (em container use GUnicorn)
# =============================================================================
if __name__ == "__main__":
    # Execução local (dev). Em produção use:
    # gunicorn -b 0.0.0.0:8200 -w 2 main:app
    app.run(host="0.0.0.0", port=8200, debug=True)
