pipeline {
    agent any

    stages {
        stage('Container Assembly') {
            steps {
                echo 'Compiling stateless Docker container...'
                // Builds the container image locally using your Dockerfile
                bat 'docker build -t aceest-fitness-api:1.1 .'
            }
        }

        stage('Automated Testing') {
            steps {
                echo 'Executing Pytest validation suite INSIDE the container sandbox...'
                // Runs the tests inside the secure, isolated container environment
                bat 'docker run --entrypoint pytest aceest-fitness-api:1.1 test_app.py -v'
            }
        }
    }
}
