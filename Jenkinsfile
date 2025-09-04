pipeline {
  agent any
  options {
    timestamps()
    buildDiscarder(logRotator(numToKeepStr: '10'))
  }

  stages {
    stage('Cleanup') {
      steps {
        sh '''
set -eu
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
        // 👇 FORÇA BASH (resolve "Illegal option -o pipefail")
        sh '''bash -lc '
set -euo pipefail

docker compose -p atividade-ci -f docker-compose.ci.yml up -d --build

for i in $(seq 1 30); do
  if docker compose -p atividade-ci -f docker-compose.ci.yml exec -T db \
       pg_isready -U pguser -d docker_e_kubernetes >/dev/null 2>&1; then
    echo "Postgres saudável."
    break
  fi
  echo "Aguardando Postgres (${i}/30)..."
  sleep 2
done

# Falha explicitamente se não estiver ok
docker compose -p atividade-ci -f docker-compose.ci.yml exec -T db \
  pg_isready -U pguser -d docker_e_kubernetes
''''
      }
    }

    stage('Entrega') {
      steps {
        // 👇 FORÇA BASH AQUI TAMBÉM
        sh '''bash -lc '
set -euo pipefail

curl --fail --retry 20 --retry-connrefused --retry-delay 1 http://localhost:8200/health
curl --fail http://localhost:8200/

echo "===== LOG DB ====="
docker compose -p atividade-ci -f docker-compose.ci.yml logs --no-color db  | tail -n +1 || true
echo "===== LOG WEB ====="
docker compose -p atividade-ci -f docker-compose.ci.yml logs --no-color web | tail -n +1 || true
''''
      }
    }
  }

  post {
    always {
      archiveArtifacts artifacts: 'docker-compose.ci.yml,docker-compose.yml,Dockerfile.web,Dockerfile.jenkins,Jenkinsfile,main.py,requirements.txt,codigo.sql',
                        fingerprint: true, allowEmptyArchive: true
      sh '''
set -eu
docker compose -p atividade-ci -f docker-compose.ci.yml down -v || true
'''
    }
  }
}
