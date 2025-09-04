pipeline {
  agent any

  options {
    skipDefaultCheckout(true)
    timestamps()
  }

  environment {
    COMPOSE_PROJECT_NAME = 'atividade-ci'
    COMPOSE_FILE = 'docker-compose.ci.yml'
  }

  stages {
    stage('Cleanup') {
      steps {
        sh '''
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
        sh '''
          set -eux
          docker build -t atividade-web -f Dockerfile.web .
          docker run --rm atividade-web python -c "import flask, sqlalchemy; print('ok')"
        '''
      }
    }

    stage('Entrega') {
      steps {
        sh '''
          set -eux
          # sobe stack de teste (db + web)
          docker compose -p "$COMPOSE_PROJECT_NAME" -f "$COMPOSE_FILE" up -d --build

          # espera a app responder (até ~30s)
          for i in $(seq 1 30); do
            if curl -sf http://localhost:8200/ >/dev/null; then
              echo "app respondeu na tentativa $i"
              break
            fi
            sleep 1
          done

          # mostra um pedaço da home e status dos containers
          curl -sf http://localhost:8200/ | head -n 5 || true
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
