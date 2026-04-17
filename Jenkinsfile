pipeline {
    agent any

    stages {

        stage('Test') {
            steps {
                sh '''
                echo "Running basic test..."
                '''
            }
        }

        stage('Build Docker Image') {
            steps {
                echo "Building Docker image..."
                sh 'docker compose build'
            }
        }

        stage('Deploy Container') {
            steps {
                sh '''
                echo "Deploying container..."
                docker compose up -d
                '''
            }
        }
    }

    post {
        success {
            echo "Deployment successful! App is live on port 8000"
        }
        failure {
            echo "Pipeline failed!"
        }
    }
}