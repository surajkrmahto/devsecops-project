
pipeline {
    agent any

    environment {
        IMAGE_NAME = 'devsecops-app:latest'
        CONTAINER_NAME = 'devsecops-container'
        TRIVY_CACHE = '/var/jenkins_home/.cache/trivy'
    }

    stages {

        stage('Checkout') {
            steps {
                checkout scm
                echo 'Source code checkout completed'
            }
        }

        stage('SonarQube Code Analysis') {
            steps {
                script {
                    def scannerHome = tool 'SonarScanner'

                    withSonarQubeEnv('SonarQube-Local') {
                        sh """
                            "${scannerHome}/bin/sonar-scanner" \
                               -Dsonar.projectKey=DevSecOps-Flask-App \
                               -Dsonar.projectName="DevSecOps Flask App" \
                              -Dsonar.sources=. \
                              -Dsonar.exclusions="**/venv/**,**/__pycache__/**"
                        """
                    }
                }
            }
        }

        stage('Build Docker Image') {
            steps {
                sh 'docker build -t devsecops-app:latest .'
            }
        }

        stage('Trivy Security Scan') {
            steps {
                sh '''
                    mkdir -p "$TRIVY_CACHE"

                    trivy image \
                      --cache-dir "$TRIVY_CACHE" \
                      --severity HIGH,CRITICAL \
                      --ignore-unfixed \
                      --exit-code 1 \
                      devsecops-app:latest
                '''
            }
        }

        stage('Deploy Application') {
            steps {
                sh '''
                    docker rm -f devsecops-container || true

                    docker run -d \
                      --name devsecops-container \
                      --restart unless-stopped \
                      --network monitoring-network \
                      -p 5000:5000 \
                      devsecops-app:latest
                '''
            }
        }
    }

    post {
        success {
            echo 'Pipeline completed successfully!'
        }
        failure {
            echo 'Pipeline failed. Check the stage logs.'
        }
        always {
            echo 'DevSecOps pipeline execution finished.'
        }
    }
}
