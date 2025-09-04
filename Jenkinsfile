pipeline {
  agent any

  options {
    skipDefaultCheckout(true)
    timestamps()
  }

  environment {
    COMPOSE_PROJECT_NAME = "atividade-ci"
    COMPOSE_FILE_CI      = "docker-compose.ci.yml"
  }

  stages {
    stage('Cleanup') {
      steps {
        sh '''
          set -eux
          docker compose -p "$COMPOSE_PROJECT_NAME" -f "$COMPOSE_FILE_CI" down -v || true
          docker system prune -af || true
          find . -name __pycache__ -type d -exec rm -rf {} +
        '''
      }
    }

    stage('Checkout') {
      steps {
        checkout([
          $class: 'GitSCM',
          branches: [[name: '*/main']],
          userRemoteConfigs: [[url: 'https://github.com/rafapeixer/Jenkins-DEVOPS-pg']]
        ])
      }
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

          # Sobe web + db
          docker compose -p "$COMPOSE_PROJECT_NAME" -f "$COMPOSE_FILE_CI" up -d --build

          echo "Aguardando DB ficar saudável..."
          for i in $(seq 1 60); do
            if docker compose -p "$COMPOSE_PROJECT_NAME" -f "$COMPOSE_FILE_CI" ps --format json \
              | jq -e '.[] | select(.Service=="db") | .Health=="healthy"' > /dev/null; then
              echo "DB saudável em $i s"
              break
            fi
            sleep 1
          done

          echo "Aguardando Web responder..."
          for i in $(seq 1 30); do
            if curl -sf http://localhost:8200/ >/dev/null; then
              echo "Web OK (tentativa $i)"
              break
            fi
            sleep 1
          done

          # Mostra um trecho da resposta só para evidência
          curl -sf http://localhost:8200/ | head -n 5 || true

          docker compose -p "$COMPOSE_PROJECT_NAME" -f "$COMPOSE_FILE_CI" ps
        '''
      }
    }
  }

  post {
    always {
      archiveArtifacts artifacts: 'docker-compose*.yml,Jenkinsfile,**/*.py,**/*.sql,**/Dockerfile*', fingerprint: true
    }
  }
}
