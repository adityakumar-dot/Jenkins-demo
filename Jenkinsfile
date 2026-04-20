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
        ECR_REPO = "483591406306.dkr.ecr.ap-south-1.amazonaws.com/ecr-demo"
        IMAGE_TAG = "latest"
        EC2_IP = "43.205.146.250"
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

        stage('Tag Image') {
            steps {
                sh '''
                docker tag ecr-demo:latest $ECR_REPO:$IMAGE_TAG
                '''
            }
        }

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

        stage('Push to ECR') {
            steps {
                sh '''
                docker push $ECR_REPO:$IMAGE_TAG
                '''
            }
        }

        stage('Deploy to EC2') {
            steps {
                sshagent(['ec2-ssh-key']) {
                    sh """
                    ssh -o StrictHostKeyChecking=no ubuntu@${EC2_IP} '
                    
                    # Login to ECR
                    aws ecr get-login-password --region ${AWS_REGION} | \
                    sudo docker login --username AWS --password-stdin ${ECR_REPO} &&

                    # Pull latest image
                    sudo docker pull ${ECR_REPO}:${IMAGE_TAG} &&

                    # Stop old container (ignore if not exists)
                    sudo docker stop my-app || true &&
                    sudo docker rm my-app || true &&

                    # Run new container
                    sudo docker run -d -p 80:8000 --name my-app \
                    ${ECR_REPO}:${IMAGE_TAG}
                    
                    '
                    """
                }
            }
        }
    }

    post {
        success {
            echo "Pipeline successful! 🚀 App deployed to EC2"
        }
        failure {
            echo "Pipeline failed! ❌ Check logs"
        }
    }
}