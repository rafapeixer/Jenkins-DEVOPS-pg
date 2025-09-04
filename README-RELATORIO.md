Como colocar pra rodar

Subir esses arquivos no seu repositório (raiz):
Jenkinsfile, docker-compose.ci.yml, docker-compose.yml, Dockerfile.web, Dockerfile.jenkins, requirements.txt, main.py, codigo.sql.

Jenkins > New Item > Pipeline

Pipeline Definition: Pipeline script from SCM

SCM: Git → https://github.com/<seu-usuario>/<seu-repo>.git

Branch: */main

Script Path: Jenkinsfile

Use Groovy Sandbox: marcado.

Build Now.
A pipeline vai:

Limpar recursos (down -v, prune)

Fazer checkout

Buildar imagem do web

Subir db+web via docker-compose.ci.yml

Aguardar a saúde do Postgres e responder em http://localhost:8200/

Se aparecer erro de porta do Postgres ocupada, é porque outra stack mapeou 5433 no host. No CI resolvemos removendo o mapeamento (não precisa). Para testes locais, o docker-compose.yml usa 5433:5432 para evitar conflito.