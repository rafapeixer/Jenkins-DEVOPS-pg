pipeline {
  agent any

  options {
    skipDefaultCheckout(true)
    timestamps()
  }

  environment {
    COMPOSE_PROJECT_NAME = "atividade-ci"
  }

  stages {
    stage('Cleanup') {
      steps {
        sh '''#!/usr/bin/env bash
          set -euxo pipefail
          docker system prune -af || true
          rm -rf .venv || true
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
          set -euxo pipefail
          docker build -t atividade-web -f Dockerfile.web .
          docker run --rm atividade-web python -c "import flask, sqlalchemy; print('ok')"
        '''
      }
    }

    stage('Entrega') {
      steps {
        sh '''#!/usr/bin/env bash
          set -euxo pipefail
          docker compose down || true
          docker compose up -d --build
          sleep 8
          curl -sf http://localhost:8200/ | head -n 5 || true
          docker ps
        '''
      }
    }
  }

  post {
    success {
      echo 'Pipeline executada com sucesso.'
    }
    always {
      archiveArtifacts artifacts: 'docker-compose.yml,Jenkinsfile,**/*.py,**/*.sql,**/Dockerfile*', fingerprint: true
    }
  }
}