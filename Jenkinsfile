pipeline {
    agent any
    stages {
        stage('Check pip') {
            steps {
        sh 'which pip3'  // Виводить шлях до pip3
            }
        }
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
    }
}
