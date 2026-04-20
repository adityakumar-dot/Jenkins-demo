// pipeline {
//     agent any

//     stages {

//         stage('Test') {
//             steps {
//                 sh '''
//                 echo "Running basic test..."
//                 '''
//             }
//         }

//         stage('Build Docker Image') {
//             steps {
//                 echo "Building Docker image..."
//                 sh 'docker compose build'
//             }
//         }

//         stage('Deploy Container') {
//             steps {
//                 sh '''
//                 echo "Deploying container..."
//                 docker compose up -d
//                 '''
//             }
//         }
//     }

//     post {
//         success {
//             echo "Deployment successful! App is live on port 8000"
//         }
//         failure {
//             echo "Pipeline failed!"
//         }
//     }
// }





//New jenkins for ECR

pipeline {
    agent any

    environment {
        AWS_REGION = "ap-south-1"
        ECR_REPO = "<account-id>.dkr.ecr.ap-south-1.amazonaws.com/ecr-demo"
        IMAGE_TAG = "latest"
    }

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
                sh 'docker build -t ecr-demo .'
            }
        }

        // 🔥 NEW STEP: Tag image for ECR
        stage('Tag Image') {
            steps {
                sh '''
                docker tag ecr-demo:latest $ECR_REPO:$IMAGE_TAG
                '''
            }
        }

        // 🔥 THIS IS YOUR STEP 5 (ECR LOGIN)
        stage('Login to ECR') {
            steps {
                withCredentials([[
                    $class: 'AmazonWebServicesCredentialsBinding',
                    credentialsId: 'aws-creds'
                ]]) {
                    sh '''
                    aws ecr get-login-password --region $AWS_REGION | \
                    docker login --username AWS --password-stdin $ECR_REPO
                    '''
                }
            }
        }

        // 🔥 Push image to ECR
        stage('Push to ECR') {
            steps {
                sh '''
                docker push $ECR_REPO:$IMAGE_TAG
                '''
            }
        }

        // (Optional) keep local deployment OR remove later
        stage('Deploy Container (Local)') {
            steps {
                sh '''
                echo "Deploying container locally..."
                docker compose down || true
                docker compose up -d
                '''
            }
        }
    }

    post {
        success {
            echo "Pipeline successful! Image pushed to ECR 🚀"
        }
        failure {
            echo "Pipeline failed!"
        }
    }
}