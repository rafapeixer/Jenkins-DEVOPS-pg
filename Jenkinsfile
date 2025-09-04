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
      steps { checkout scm }
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
          docker compose -p "$COMPOSE_PROJECT_NAME" -f "$COMPOSE_FILE" up -d --build

          # espera o web responder (até ~40s)
          for i in $(seq 1 40); do
            if curl -sf http://localhost:8200/ >/dev/null; then
              echo "app respondeu na tentativa $i"; break
            fi
            sleep 1
          done

          # evidências
          curl -sf http://localhost:8200/ | head -n 5 || true
          docker compose -p "$COMPOSE_PROJECT_NAME" -f "$COMPOSE_FILE" ps
        '''
      }
    }
  }

  post {
    always {
      archiveArtifacts artifacts: 'docker-compose*.yml,Jenkinsfile,**/*.py,**/*.sql,**/Dockerfile*', fingerprint: true
    }
    success { echo 'Pipeline executada com sucesso.' }
  }
}
