pipeline {
    agent any

    environment {
        DOCKER_COMPOSE_FILE = 'docker-compose.yml'
    }

    stages {
        stage('Checkout') {
            steps {
                git url: 'https://github.com/Prakhar8003/Web-App-Automation.git', branch: 'main'
            }
        }

        stage('Build Docker Images') {
            steps {
                script {
                    // Check if Docker is installed and accessible
                    bat 'docker --version'
                    bat 'docker-compose --version'

                    // Build Docker images using docker-compose
                    bat 'docker-compose -f %DOCKER_COMPOSE_FILE% build'
                }
            }
        }

        stage('Run Docker Compose') {
            steps {
                script {
                    // Run Docker containers in the background (detached mode)
                    bat 'docker-compose -f %DOCKER_COMPOSE_FILE% up -d'
                }
            }
        }

        stage('Test Application') {
            steps {
                script {
                    // Test the running application (you can replace this with your own tests)
                    bat 'curl http://localhost:8765'
                }
            }
        }
    }

    post {
        always {
            // Clean the workspace without stopping the running containers
            cleanWs()
        }
    }
}
