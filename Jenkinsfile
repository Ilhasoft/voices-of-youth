pipeline {
    agent none
    stages {
        stage('Back-end') {
            agent {
                docker { image 'python:3.6-alpine' }
            }
            steps {
                sh 'pip install -U pip'
            }
        }
    }
}
