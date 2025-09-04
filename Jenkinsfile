pipeline {
  agent any
  options { timestamps() }

  stages {
    stage('Cleanup') {
      steps {
        sh '''
          set -eux
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
          docker compose -p atividade-ci -f docker-compose.ci.yml up -d --build

          # espera o banco ficar OK
          for i in $(seq 1 30); do
            if docker compose -p atividade-ci -f docker-compose.ci.yml exec -T db pg_isready -U pguser -d docker_e_kubernetes; then
              break
            fi
            sleep 2
          done

          # healthcheck da aplicação
          curl --fail --retry 10 --retry-connrefused --retry-delay 1 http://localhost:8200/health
        '''
      }
    }
  }

  post {
    always {
      archiveArtifacts artifacts: 'codigo.sql,docker-compose.ci.yml,docker-compose.yml,Dockerfile.web,Dockerfile.jenkins,Jenkinsfile,main.py,requirements.txt',
                        fingerprint: true, allowEmptyArchive: true
    }
  }
}
