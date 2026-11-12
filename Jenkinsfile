pipeline {
    agent any

    stages {

        stage('Checkout') {
            steps {
                echo 'Source code checkout completed'
            }
        }

        stage('Build Docker Image') {
            steps {
                sh 'docker build -t devsecops-app:latest .'
            }
        }

        stage('Deploy Application') {
            steps {
                sh '''
                    docker stop devsecops-container || true
                    docker rm devsecops-container || true

                    docker run -d \
                      --name devsecops-container \
                      -p 5000:5000 \
                      devsecops-app:latest
                '''
            }
        }
    }
}
