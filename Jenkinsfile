pipeline {
  agent any

  environment {
    REGISTRY = "localhost:5000"
    IMAGE = "${env.REGISTRY}/myflask"
    PORT = "5001"
  }

  stages {
    stage('Checkout') {
      steps {
        checkout scm
      }
    }

    stage('Test') {
      steps {
        // ensure Python deps & run tests. adjust python path if needed.
        sh '''
          python3 -m venv venv_test || true
          . venv_test/bin/activate
          python -m pip install --upgrade pip setuptools wheel
          python -m pip install -r requirements.txt
          PYTHONPATH=. pytest -q
        '''
      }
    }

    stage('Build Image') {
      steps {
        sh '''
          # tag with build number so we can track versions
          sudo /usr/bin/podman build -t ${IMAGE}:${BUILD_NUMBER} .
        '''
      }
    }

    stage('Push Image') {
      steps {
        sh '''
          sudo /usr/bin/podman tag ${IMAGE}:${BUILD_NUMBER} ${IMAGE}:latest || true
          sudo /usr/bin/podman push --tls-verify=false ${IMAGE}:${BUILD_NUMBER}
          sudo /usr/bin/podman push --tls-verify=false ${IMAGE}:latest
        '''
      }
    }

    stage('Deploy') {
      steps {
        sh '''
          # stop & remove previous container (if any)
          if sudo /usr/bin/podman ps -a --format "{{.Names}}" | grep -w myflask-staging; then
            sudo /usr/bin/podman stop myflask-staging || true
            sudo /usr/bin/podman rm myflask-staging || true
          fi

          # run new container (expose host port ${PORT} -> container 5000)
          sudo /usr/bin/podman run -d --name myflask-staging -p ${PORT}:5000 ${IMAGE}:${BUILD_NUMBER}
        '''
      }
    }
  }

  
  post {
    always {
      script {
        echo "Pipeline finished with status: ${currentBuild.currentResult}"
      }
    }
    // failure {
    //   mail to: 'you@example.com',
    //        subject: "Build ${env.JOB_NAME} #${env.BUILD_NUMBER} failed",
    //        body: "Check Jenkins: ${env.BUILD_URL}"
    // }
  }
}
