pipeline {
    agent any

    stages {
        stage('Environment Audit') {
            steps {
                echo 'Checking Python environment status...'
                // Install locked dictionary dependencies
                sh 'pip install -r requirements.txt'
            }
        }

        stage('Pytest Execution Check') {
            steps {
                echo 'Running endpoint status assertions...'
                // Executes assertions checking status code logic matches hardcoded values
                sh 'pytest test_app.py -v'
            }
        }

        stage('Container Layer Assembly') {
            steps {
                echo 'Compiling stateless Docker container...'
                // Compiles high-efficiency database-free container image
                sh 'docker build -t aceest-fitness-api:1.0 .'
            }
        }
    }
}
