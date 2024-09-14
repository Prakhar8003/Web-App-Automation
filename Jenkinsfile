pipeline {
    agent any

    environment {
        MYSQL_HOST = 'db'
        MYSQL_USER = 'root'
        MYSQL_PASSWORD = 'rootpassword'
        MYSQL_DATABASE = 'myapp'
        REDIS_HOST = 'cache'
    }

    stages {
        stage('Checkout') {
            steps {
                // No credentials required since the repository is public
                git url: 'https://github.com/Prakhar8003/Web-App-Automation.git', branch: 'main'
            }
        }

        stage('Build Docker Images') {
            steps {
                script {
                    sh 'docker-compose build'
                }
            }
        }

        stage('Run Docker Compose') {
            steps {
                script {
                    sh 'docker-compose up -d'
                }
            }
        }

        stage('Test Application') {
            steps {
                script {
                    // Here you can add any tests or health checks you want to perform
                    sh 'curl http://localhost:8765'
                }
            }
        }

        stage('Clean Up') {
            steps {
                script {
                    // Optionally bring down the containers after tests
                    sh 'docker-compose down'
                }
            }
        }
    }
}
