pipeline {
  agent { label 'podman-agent' }
  environment {
    REGISTRY = "localhost:5000"
    IMAGE = "${REGISTRY}/myflask"
  }
  options {
    buildDiscarder(logRotator(numToKeepStr: '10'))
    timestamps()
  }
  stages {
    stage('Checkout') {
      steps { checkout scm }
    }

    stage('Lint (optional)') {
      steps {
        sh 'python3 -m venv venv_test || true; . venv_test/bin/activate; pip install flake8 || true; flake8 || true'
      }
    }

    stage('Test') {
      steps {
        sh '''
          python3 -m venv venv_test
          . venv_test/bin/activate
          pip install -r requirements.txt
          PYTHONPATH=. pytest -q
        '''
      }
    }

    stage('Build Image') {
      steps {
        script {
          IMAGE_TAG = "${IMAGE}:${BUILD_NUMBER}"
        }
        sh "sudo /usr/bin/podman build -t ${IMAGE_TAG} ."
        sh "sudo /usr/bin/podman tag ${IMAGE_TAG} ${IMAGE}:latest"
      }
    }

    stage('Push Image') {
      steps {
        sh "sudo /usr/bin/podman push --tls-verify=false ${IMAGE_TAG}"
      }
    }

    stage('Deploy (safe)') {
      steps {
        sh '''
          # pull new image locally
          sudo /usr/bin/podman pull --tls-verify=false ${IMAGE_TAG} || true

          # run new container with temporary name
          NEW_NAME="myflask-new-${BUILD_NUMBER}"
          sudo /usr/bin/podman rm -f $NEW_NAME || true
          sudo /usr/bin/podman run -d --name $NEW_NAME -p 5002:5000 ${IMAGE_TAG}

          # wait for health on port 5002
          for i in $(seq 1 15); do
            if curl -sSf http://127.0.0.1:5002/health >/dev/null 2>&1; then
              echo "new container healthy"
              break
            fi
            sleep 2
          done

          # swap: stop old and run new on 5001
          sudo /usr/bin/podman rm -f myflask-staging || true
          sudo /usr/bin/podman run -d --name myflask-staging -p 5001:5000 ${IMAGE_TAG}
          # cleanup new temporary
          sudo /usr/bin/podman rm -f $NEW_NAME || true
        '''
      }
    }

    stage('Post Deploy Check') {
      steps {
        sh '''
          # quick smoke test
          curl -sSf http://127.0.0.1:5001/health || (echo "smoke failed" && exit 1)
        '''
      }
    }
  }

  post {
    success {
      script {
        // Add build metadata to env for containerized app to show
        sh "git rev-parse --short HEAD > gitrev.txt || true"
      }
      echo "Build ${BUILD_NUMBER} succeeded"
    }
    failure {
      echo "Build failed"
    }
    always {
      script {
        echo "Pipeline finished with status: ${currentBuild.currentResult}"
      }
    }
  }
}
