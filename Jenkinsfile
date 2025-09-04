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
        sh '''#!/usr/bin/env sh
          set -eux
          docker compose -p "$COMPOSE_PROJECT_NAME" -f "$COMPOSE_FILE" down -v || true
          docker system prune -af || true
          find . -name "__pycache__" -type d -exec rm -rf {} + || true
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
        sh '''#!/usr/bin/env sh
          set -eux
          docker build -t atividade-web -f Dockerfile.web .
          docker run --rm atividade-web python -c "import flask, sqlalchemy; print('ok')" 
        '''
      }
    }

    stage('Entrega') {
      steps {
        sh '''#!/usr/bin/env sh
          set -eux

          # Sobe stack de teste
          docker compose -p "$COMPOSE_PROJECT_NAME" -f "$COMPOSE_FILE" up -d --build

          # Aguarda DB healthy (até ~45s)
          i=0
          until [ "$i" -ge 45 ]; do
            status=$(docker inspect -f '{{.State.Health.Status}}' ${COMPOSE_PROJECT_NAME}-db-1 2>/dev/null || true)
            [ "$status" = "healthy" ] && break
            i=$((i+1))
            sleep 1
          done

          # Aguarda web responder (até ~60s)
          j=0
          until [ "$j" -ge 60 ]; do
            if curl -sf http://localhost:8200/ >/dev/null; then
              echo "web respondeu na tentativa $j"
              break
            fi
            j=$((j+1))
            sleep 1
          done

          # Mostra parte da home
          curl -sf http://localhost:8200/ | head -n 10 || true

          docker compose -p "$COMPOSE_PROJECT_NAME" -f "$COMPOSE_FILE" ps

          # Se web não respondeu, mostra logs e falha
          if ! curl -sf http://localhost:8200/ >/dev/null; then
            echo "==== DB LOGS ===="
            docker logs ${COMPOSE_PROJECT_NAME}-db-1 || true
            echo "==== WEB LOGS ===="
            docker logs ${COMPOSE_PROJECT_NAME}-web-1 || true
            exit 1
          fi
        '''
      }
    }
  }

  post {
    success { echo 'Pipeline executada com sucesso.' }
    always {
      archiveArtifacts artifacts: 'docker-compose*.yml,Jenkinsfile,**/*.py,**/*.sql,**/Dockerfile*', fingerprint: true
    }
  }
}
