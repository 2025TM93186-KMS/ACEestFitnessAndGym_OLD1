pipeline {
    agent any

    stages {
        stage('Environment Audit') {
            steps {
                echo 'Checking Python environment status...'
                // Using bat instead of sh for Windows support
                bat 'pip install -r requirements.txt'
            }
        }

        stage('Pytest Execution Check') {
            steps {
                echo 'Running endpoint status assertions...'
                bat 'pytest test_app.py -v'
            }
        }

        stage('Container Layer Assembly') {
            steps {
                echo 'Compiling stateless Docker container...'
                bat 'docker build -t aceest-fitness-api:1.0 .'
            }
        }
    }
}
