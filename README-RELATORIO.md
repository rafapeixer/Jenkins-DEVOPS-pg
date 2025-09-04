# Esteira DevOps — Jenkins + Docker (CI/CD) com PostgreSQL

**Integrantes:** _preencha com 1 a 3 nomes_

## 1) Integração Contínua (CI)

### 1.1 Objetivo
Garantir que a aplicação Flask seja construída a cada commit, com validação mínima de dependências e build das imagens Docker.

### 1.2 Stages e Evidências
- **Cleanup** — limpeza do workspace e camadas Docker antigas. _(Anexe print do console do Jenkins com `docker system prune`)_
- **Checkout** — código baixado do SCM. _(Anexe print do changelog do Jenkins)_
- **Construção** — `docker build` da imagem web + teste rápido (`import flask, sqlalchemy`). _(Anexe print do console com sucesso)_

### 1.3 Pipeline (Jenkinsfile)
Veja o arquivo `Jenkinsfile` na raiz do repositório. Ele executa os estágios: Cleanup → Checkout → Construção → Entrega.

## 2) Entrega Contínua (CD)

### 2.1 Objetivo
Subir o ambiente de homologação via `docker compose`, expondo a aplicação em `http://localhost:8200` (web) e `5432` (Postgres).

### 2.2 Stages e Evidências
- **Entrega** — `docker compose up -d --build` com `db` (PostgreSQL) e `web` (Flask).
  - _(Print do `docker ps` com os 3 containers: db, web, jenkins)_
  - _(Print do navegador com “Funciona!” em `http://localhost:8200/`)_

### 2.3 Arquivos de Infra
- `docker-compose.yml` — orquestra Postgres, Web e Jenkins
- `Dockerfile.web` — imagem da aplicação Flask
- `codigo.sql` — seed executado automaticamente no Postgres
- `requirements.txt`, `main.py`

## 3) Como executar

```bash
# Build e subida
docker compose up -d --build

# Verificar containers
docker ps

# Testar aplicação
curl http://localhost:8200/
# ou abrir no navegador
```

## 4) Perguntas

**1. Como a automação (CI/CD) ajuda no longo prazo?**  
- Feedback contínuo a cada commit (quebra detectada cedo).  
- Padroniza builds e deploys, reduzindo erros humanos.  
- Logs e artefatos versionados → rastreabilidade e rollback.  
- Encoraja testes, lint e scans automáticos → qualidade e segurança.  
- Libera tempo do time para tarefas de maior valor.

**2. Como poderíamos realizar telemetria do pipeline?**  
- **Jenkins + Prometheus** (plugin) → métricas de builds (status, duração, fila) exibidas no **Grafana** (DORA: Lead Time, MTTR, CFR).  
- **Logs** do console enviados a ELK/OpenSearch com alertas (ex.: falha no estágio Construção).  
- **Notificações** via Slack/Email/Webhooks a cada mudança de estado.  
- **Auditoria** (aprovadores, gatilhos manuais, autoria dos deploys).

---

> Após rodar localmente, gere os **prints** solicitados e exporte este relatório em PDF para entrega.