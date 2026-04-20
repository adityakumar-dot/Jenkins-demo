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


        stage('Deploy to EC2') {
            environment {
                EC2_IP = 43.205.146.250
            }   
            steps {
                sshagent(['ec2-ssh-key']) {
                    sh '''
                    ssh -o StrictHostKeyChecking=no ubuntu@$EC2_IP << EOF

                    # Login to ECR
                    aws ecr get-login-password --region ap-south-1 | \
                    sudo docker login --username AWS --password-stdin 483591406306.dkr.ecr.ap-south-1.amazonaws.com

                    # Pull latest image
                    sudo docker pull 483591406306.dkr.ecr.ap-south-1.amazonaws.com/ecr-demo:latest

                    # Stop old container
                    sudo docker stop my-app || true

                    # Remove old container
                    sudo docker rm my-app || true

                    # Run new container
                    sudo docker run -d -p 80:8000 --name my-app \
                    483591406306.dkr.ecr.ap-south-1.amazonaws.com/ecr-demo:latest

                    EOF
                    '''
                }
            }
}
        // (Optional) keep local deployment OR remove later
        // stage('Deploy Container (Local)') {
        //     steps {
        //         sh '''
        //         echo "Deploying container locally..."
        //         docker compose down || true
        //         docker compose up -d
        //         '''
        //     }
        // }
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