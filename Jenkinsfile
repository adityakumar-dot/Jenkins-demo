pipeline {
    agent any

    environment {
        IMAGE_NAME = "python-jenkins"
        CONTAINER_NAME = "python-jenkins"
        PORT = "8001"
    }

    stages {

        stage('Checkout Code') {
            steps {
                git branch: 'main', url: 'https://github.com/adityakumar-dot/Jenkins-demo.git'
            }
        }

        // stage('Build (Install Dependencies)') {
        //     steps {
        //         sh '''
        //         echo "Installing dependencies..."
        //         pip3 install -r requirements.txt
        //         '''
        //     }   
        // }

        stage('Test') {
            steps {
                sh '''
                echo "Running basic test..."
                python3 -c "import main"
                '''
            }
        }

        stage('Build Docker Image') {
            steps {
                sh '''
                echo "Building Docker image..."
                docker build -t $IMAGE_NAME .
                '''
            }
        }

        stage('Deploy Container') {
            steps {
                sh '''
                echo "Deploying container..."

                docker rm -f $CONTAINER_NAME || true

                docker run -d -p $PORT:8000 \
                --name $CONTAINER_NAME \
                $IMAGE_NAME
                '''
            }
        }
    }

    post {
        success {
            echo "✅ Deployment successful! App is live on port ${PORT}"
        }
        failure {
            echo "❌ Pipeline failed!"
        }
    }
}