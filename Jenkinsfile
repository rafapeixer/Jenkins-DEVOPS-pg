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
#!/usr/bin/env bash
set -euo pipefail
docker compose -p atividade-ci -f docker-compose.ci.yml down -v || true
docker system prune -af || true
find . -name __pycache__ -type d -exec rm -rf {} +
'''
      }
    }

    stage('Checkout') {
      steps {
        // Se o job for "Pipeline from SCM", o Jenkins faz o checkout automático.
        // Mantemos para compatibilidade com o padrão da professora:
        checkout scm
      }
    }

    stage('Construção') {
      steps {
        sh '''
#!/usr/bin/env bash
set -euo pipefail

# Sobe web + db do arquivo CI
docker compose -p atividade-ci -f docker-compose.ci.yml up -d --build

# Espera o Postgres ficar pronto (usa as mesmas credenciais do docker-compose.ci.yml)
for i in $(seq 1 30); do
  if docker compose -p atividade-ci -f docker-compose.ci.yml exec -T db \
       pg_isready -U pguser -d docker_e_kubernetes >/dev/null 2>&1; then
    echo "Postgres saudável."
    break
  fi
  echo "Aguardando Postgres (${i}/30)..."
  sleep 2
done

# Se ainda não estiver saudável, falha o build
docker compose -p atividade-ci -f docker-compose.ci.yml exec -T db \
  pg_isready -U pguser -d docker_e_kubernetes
'''
      }
    }

    stage('Entrega') {
      steps {
        sh '''
#!/usr/bin/env bash
set -euo pipefail

# Smoke tests do serviço web (porta 8200 mapeada no CI)
curl --fail --retry 20 --retry-connrefused --retry-delay 1 http://localhost:8200/health
curl --fail http://localhost:8200/

# Logs para evidência
echo "===== LOG DB ====="
docker compose -p atividade-ci -f docker-compose.ci.yml logs --no-color db  | tail -n +1 || true
echo "===== LOG WEB ====="
docker compose -p atividade-ci -f docker-compose.ci.yml logs --no-color web | tail -n +1 || true
'''
      }
    }
  }

  post {
    always {
      archiveArtifacts artifacts: 'docker-compose.ci.yml,docker-compose.yml,Dockerfile.web,Dockerfile.jenkins,Jenkinsfile,main.py,requirements.txt,codigo.sql',
                        fingerprint: true, allowEmptyArchive: true
      sh '''
#!/usr/bin/env bash
set -euo pipefail
docker compose -p atividade-ci -f docker-compose.ci.yml down -v || true
'''
    }
  }
}
