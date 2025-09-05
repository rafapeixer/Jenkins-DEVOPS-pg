pipeline {
  agent any
  options {
    timestamps()
    buildDiscarder(logRotator(numToKeepStr: '10'))
    ansiColor('xterm')
  }

  stages {

    stage('Cleanup') {
      steps {
        // usa shebang + bash; nada de "bash -lc '...'"
        sh '''#!/usr/bin/env bash
set -eu
docker compose -p atividade-ci -f docker-compose.ci.yml down -v || true
docker system prune -af || true
find . -name "__pycache__" -type d -exec rm -rf {} +
'''
      }
    }

    stage('Checkout') {
      steps {
        checkout scm
      }
    }

    stage('Construção') {
      steps {
        // mesmo padrão de cima (sem aspas aninhadas)
        sh '''#!/usr/bin/env bash
set -euo pipefail

# sobe o ambiente de CI (builda imagens)
docker compose -p atividade-ci -f docker-compose.ci.yml up -d --build

# espera o Postgres ficar saudável
for i in $(seq 1 30); do
  if docker compose -p atividade-ci -f docker-compose.ci.yml exec -T db \
       pg_isready -U pguser -d docker_e_kubernetes >/dev/null 2>&1; then
    echo "Postgres saudável."
    break
  fi
  echo "Aguardando Postgres (${i}/30)..."
  sleep 2
done

# falha explicitamente se não estiver saudável
docker compose -p atividade-ci -f docker-compose.ci.yml exec -T db \
  pg_isready -U pguser -d docker_e_kubernetes
'''
      }
    }

    stage('Entrega') {
      steps {
        // faz o curl de DENTRO do container web (evita problema de rede/localhost)
        sh '''#!/usr/bin/env bash
set -euo pipefail

# smoke tests do web (exec dentro do container)
docker compose -p atividade-ci -f docker-compose.ci.yml exec -T web \
  curl --fail --silent http://localhost:8200/health >/dev/null

docker compose -p atividade-ci -f docker-compose.ci.yml exec -T web \
  curl --fail --silent http://localhost:8200/ >/dev/null

echo "===== LOG DB ====="
docker compose -p atividade-ci -f docker-compose.ci.yml logs --no-color db  | tail -n +200 || true
echo "===== LOG WEB ====="
docker compose -p atividade-ci -f docker-compose.ci.yml logs --no-color web | tail -n +200 || true
'''
      }
    }
  }

  post {
    always {
      archiveArtifacts artifacts: 'docker-compose.ci.yml,docker-compose.yml,Dockerfile.web,Dockerfile.jenkins,Jenkinsfile,main.py,requirements.txt,codigo.sql',
                        fingerprint: true, allowEmptyArchive: true
      sh '''#!/usr/bin/env bash
set -eu
docker compose -p atividade-ci -f docker-compose.ci.yml down -v || true
'''
    }
  }
}