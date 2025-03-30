pipeline {
    agent any
    stages {
        stage('Clone Repository') {
            steps {
                git 'https://github.com/CyberSortir936/UITP1.git'
            }
        }
        stage('Setup Python') {
            steps {
                sh 'pip install -r requirements.txt'
            }
        }
        stage('Run Tests') {
            steps {
                sh 'python -m unittest discover tests/'
            }
        }
    }
}
