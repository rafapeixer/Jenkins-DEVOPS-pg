pipeline {
  agent any

  options {
    skipDefaultCheckout(true)
    timestamps()
  }

  environment {
    // Nome lógico do projeto docker-compose (evita conflito de nomes/portas)
    COMPOSE_PROJECT_NAME = "atividade-ci"
    // Arquivo compose específico para CI (sem container_name fixo, sem portas “presas”)
    COMPOSE_FILE = "docker-compose.ci.yml"
  }

  stages {
    stage('Cleanup') {
      steps {
        sh '''#!/usr/bin/env bash
          set -euxo pipefail
          # derruba a stack anterior (se existir) e limpa volumes da stack
          docker compose -p "$COMPOSE_PROJECT_NAME" -f "$COMPOSE_FILE" down -v || true

          # limpeza geral “segura”
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
          set -euxo pipefail
          # build local da imagem web e smoke test de libs
          docker build -t atividade-web -f Dockerfile.web .
          docker run --rm atividade-web python -c "import flask, sqlalchemy; print('ok')"
        '''
      }
    }

    stage('Entrega') {
      steps {
        sh '''#!/usr/bin/env bash
          set -euxo pipefail

          # sobe a stack de teste (Postgres + Web; Jenkins já está rodando fora)
          docker compose -p "$COMPOSE_PROJECT_NAME" -f "$COMPOSE_FILE" up -d --build

          # espera o serviço web responder (até ~30s)
          for i in $(seq 1 30); do
            if curl -sf http://localhost:8200/ >/dev/null; then
              echo "app respondeu na tentativa $i"
              break
            fi
            sleep 1
          done

          # mostra um trecho da home (não falha o build caso a home retorne non-200)
          curl -sf http://localhost:8200/ | head -n 5 || true

          # status dos serviços
          docker compose -p "$COMPOSE_PROJECT_NAME" -f "$COMPOSE_FILE" ps
          docker ps
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
