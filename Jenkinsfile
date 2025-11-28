pipeline {
    agent any


    parameters {
        string(name: 'IMAGE_NAME', defaultValue: 'fmanon/nginx', description: 'Docker image name')
        string(name: 'IMAGE_TAG', defaultValue: 'latest', description: 'Docker image tag')
        string(name: 'NGINX_DIR', defaultValue: 'deployment/nginx', description: 'Directory containing Dockerfile and HTML')
    }


    environment {
        DOCKER_HOST = "tcp://host.docker.internal:2375"
        // Replace 'docker-hub-creds' with your Jenkins Username/Password credential ID
        DOCKERHUB_CRED = credentials('dockerhub-creds')
    }


    stages {


        stage('Checkout') {
            steps {
                checkout scm
            }
        }


        stage('Build & Push Docker Image') {
            steps {
                script {
                    def dirPath = "${env.WORKSPACE}/${params.NGINX_DIR}"
                    if (!fileExists(dirPath)) {
                        error "Directory ${dirPath} does not exist!"
                    }


                    sh """
                        set -e
                        cd "${dirPath}"
                        echo "Building Docker image: ${params.IMAGE_NAME}:${params.IMAGE_TAG}"
                        docker build -t "${params.IMAGE_NAME}:${params.IMAGE_TAG}" .


                        echo "Logging in to Docker Hub"
                        echo "$DOCKERHUB_CRED_PSW" | docker login -u "$DOCKERHUB_CRED_USR" --password-stdin


                        echo "Pushing Docker image"
                        docker push "${params.IMAGE_NAME}:${params.IMAGE_TAG}"


                        docker logout
                    """
                }
            }
        }
    }


    post {
        always {
            echo 'Pipeline finished.'
        }
        success {
            echo "Docker image ${params.IMAGE_NAME}:${params.IMAGE_TAG} successfully pushed."
        }
        failure {
            echo 'Pipeline failed.'
        }
    }
}
