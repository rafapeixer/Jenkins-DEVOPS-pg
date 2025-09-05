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
        sh '''#!/usr/bin/env bash
set -eu
docker compose -p atividade-ci -f docker-compose.ci.yml down -v || true
docker system prune -af || true
find . -name __pycache__ -type d -exec rm -rf {} +
'''
      }
    }

    stage('Checkout') {
      steps { checkout scm }
    }

    stage('Construção') {
      steps {
        // 1º: sobe o ambiente e builda imagens
        sh '''#!/usr/bin/env bash
set -euo pipefail
docker compose -p atividade-ci -f docker-compose.ci.yml up -d --build
'''
        // 2º: espera o Postgres ficar OK (sem "\" no fim da linha)
        sh '''#!/usr/bin/env bash
set -euo pipefail
for i in $(seq 1 30); do
  if docker compose -p atividade-ci -f docker-compose.ci.yml exec -T db pg_isready -U pguser -d docker_e_kubernetes >/dev/null 2>&1; then
    echo "Postgres saudável."; exit 0
  fi
  echo "Aguardando Postgres ($i/30) ..."; sleep 2
done
echo "DB não respondeu a tempo."; exit 1
'''
      }
    }

    stage('Entrega') {
      steps {
        // Faz os curls de DENTRO do container web
        sh '''#!/usr/bin/env bash
set -euo pipefail
docker compose -p atividade-ci -f docker-compose.ci.yml exec -T web curl --fail --silent http://localhost:8200/health >/dev/null
docker compose -p atividade-ci -f docker-compose.ci.yml exec -T web curl --fail --silent http://localhost:8200/        >/dev/null
echo "===== LOG DB ====="
docker compose -p atividade-ci -f docker-compose.ci.yml logs --no-color db  | tail -n +1 || true
echo "===== LOG WEB ====="
docker compose -p atividade-ci -f docker-compose.ci.yml logs --no-color web | tail -n +1 || true
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
