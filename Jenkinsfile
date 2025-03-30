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
        stage('Setup Python Environment') {
            steps {
                sh '''
                # Створюємо віртуальне середовище
                python3 -m venv venv
                # Активуємо віртуальне середовище
                source venv/bin/activate
                # Оновлюємо pip
                pip install --upgrade pip
                # Встановлюємо залежності
                pip install -r requirements.txt
                '''
            }
        }
        stage('Run Tests') {
            steps {
                sh '''
                # Активуємо віртуальне середовище
                source venv/bin/activate
                # Запускаємо тести
                python -m unittest discover
                '''
            }
        }
    }
}
