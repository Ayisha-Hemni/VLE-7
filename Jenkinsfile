pipeline {
    agent any

    environment {
        IMAGE_NAME = "vle7-monitoring-app"
    }

    stages {

        stage('Checkout') {
            steps {
                checkout scm
                echo 'Source code downloaded successfully!'
            }
        }

        stage('Build Docker Image') {
            steps {
                sh '''
                    docker build -t ${IMAGE_NAME}:${BUILD_NUMBER} .
                '''
            }
        }

        stage('Test Application') {
            steps {
                sh '''
                    set -e

                    docker run -d \
                        --name vle7-test-${BUILD_NUMBER} \
                        -p 5001:5000 \
                        ${IMAGE_NAME}:${BUILD_NUMBER}

                    trap 'docker rm -f vle7-test-${BUILD_NUMBER} >/dev/null 2>&1 || true' EXIT

                    for i in $(seq 1 15); do
                        if curl -fsS http://localhost:5001/health; then
                            echo "Application health check passed!"
                            exit 0
                        fi
                        sleep 2
                    done

                    echo "Application health check failed!"
                    exit 1
                '''
            }
        }
    }

    post {
        success {
            echo 'CI pipeline completed successfully!'
        }

        failure {
            echo 'CI pipeline failed. Check the console output.'
        }
    }
}
