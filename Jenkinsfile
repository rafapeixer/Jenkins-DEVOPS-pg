pipeline {
  agent any

  options {
    skipDefaultCheckout(true)
    timestamps()
  }

  environment {
    COMPOSE_PROJECT_NAME = "atividade-ci"
    COMPOSE_FILE = "docker-compose.ci.yml"
  }

  stages {
    stage('Cleanup') {
      steps {
        sh '''#!/usr/bin/env bash
set -eux
docker compose -p "$COMPOSE_PROJECT_NAME" -f "$COMPOSE_FILE" down -v || true
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
        sh '''#!/usr/bin/env bash
set -eux
docker build -t atividade-web -f Dockerfile.web .
docker run --rm atividade-web python -c "import flask, sqlalchemy; print('ok')"
'''
      }
    }

    stage('Entrega') {
      steps {
        sh '''#!/usr/bin/env bash
set -eux

# Sobe a stack de teste (SEM publicar portas: nada conflita)
docker compose -p "$COMPOSE_PROJECT_NAME" -f "$COMPOSE_FILE" up -d --build

# Aguarda o web responder via um container curl dentro da MESMA rede
for i in $(seq 1 30); do
  if docker run --rm --network "${COMPOSE_PROJECT_NAME}_default" curlimages/curl:8.7.1 -fsS http://web:8200/health >/dev/null; then
    echo "web respondeu na tentativa $i"
    break
  fi
  sleep 1
done

# Mostra um trecho da home e o estado dos serviços
docker run --rm --network "${COMPOSE_PROJECT_NAME}_default" curlimages/curl:8.7.1 -fsS http://web:8200/ | head -n 5 || true
docker compose -p "$COMPOSE_PROJECT_NAME" -f "$COMPOSE_FILE" ps
'''
      }
    }
  }

  post {
    success {
      echo 'Pipeline executada com sucesso.'
    }
    always {
      archiveArtifacts artifacts: 'docker-compose*.yml,Jenkinsfile,**/*.py,**/*.sql,**/Dockerfile*', fingerprint: true
    }
  }
}
