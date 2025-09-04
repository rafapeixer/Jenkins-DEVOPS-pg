pipeline {
  agent any
  options { timestamps(); ansiColor('xterm'); buildDiscarder(logRotator(numToKeepStr: '10')) }

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
      steps {
        checkout scm
      }
    }

    stage('Construção') {
      steps {
        sh '''
          set -euxo pipefail
          docker compose -p atividade-ci -f docker-compose.ci.yml up -d --build
          for i in $(seq 1 30); do
            if docker compose -p atividade-ci -f docker-compose.ci.yml exec -T db \
                 pg_isready -U pguser -d docker_e_kubernetes; then
              break
            fi
            sleep 2
          done
        '''
      }
    }

    stage('Entrega') {
      steps {
        sh '''
          set -euxo pipefail
          curl --fail --retry 20 --retry-connrefused --retry-delay 1 http://localhost:8200/health
          curl --fail http://localhost:8200/
          docker compose -p atividade-ci -f docker-compose.ci.yml logs --no-color db | tail -n +200 || true
          docker compose -p atividade-ci -f docker-compose.ci.yml logs --no-color web | tail -n +200 || true
        '''
      }
    }
  }

  post {
    always {
      archiveArtifacts artifacts: 'docker-compose.ci.yml,docker-compose.yml,Dockerfile.web,Dockerfile.jenkins,Jenkinsfile,main.py,requirements.txt,codigo.sql',
                        fingerprint: true, allowEmptyArchive: true
      sh 'docker compose -p atividade-ci -f docker-compose.ci.yml down -v || true'
    }
  }
}
