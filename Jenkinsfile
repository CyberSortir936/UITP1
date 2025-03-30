pipeline {
    agent any
    environment {
        // Додаткове середовище для Python
        PYTHON_ENV = 'venv'
    }
    stages {
        stage('Clone Repository') {
            steps {
                git 'https://github.com/CyberSortir936/UITP1.git'
            }
        }
        stage('Setup Python') {
            steps {
                script {
                    // Створення virtualenv, якщо не використовується в системі
                    sh 'python -m venv $PYTHON_ENV'
                    // Активація virtualenv
                    sh '. $PYTHON_ENV/bin/activate && pip install -r requirements.txt'
                }
            }
        }
        stage('Run Tests') {
            steps {
                script {
                    // Запуск тестів
                    sh '. $PYTHON_ENV/bin/activate && python -m unittest discover tests/'
                }
            }
        }
    }
    post {
        always {
            // Очищення середовища після виконання пайплайну
            cleanWs()
        }
    }
}
