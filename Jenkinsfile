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
        sh '''
          set -euxo pipefail
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
          set -euxo pipefail
          docker build -t atividade-web -f Dockerfile.web .
          docker run --rm atividade-web python -c "import flask, sqlalchemy; print('ok')"
        '''
      }
    }

    stage('Entrega') {
      steps {
        sh '''
          set -euxo pipefail
          docker compose -p "$COMPOSE_PROJECT_NAME" -f "$COMPOSE_FILE" up -d --build

          # espera o web responder (até 40s)
          ok=0
          for i in $(seq 1 40); do
            if curl -sf http://localhost:8200/ >/dev/null; then
              echo "app respondeu na tentativa $i"
              ok=1
              break
            fi
            sleep 1
          done

          # sempre mostra status
          docker compose -p "$COMPOSE_PROJECT_NAME" -f "$COMPOSE_FILE" ps

          if [ "$ok" -ne 1 ]; then
            echo "web não respondeu em 40s; logs do DB para diagnóstico:"
            docker compose -p "$COMPOSE_PROJECT_NAME" -f "$COMPOSE_FILE" logs --no-color db | tail -n 200 || true
            exit 1
          fi

          curl -sf http://localhost:8200/ | head -n 10 || true
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
