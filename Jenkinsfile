@Library('pacifica-jenkins-lib@sonarqube')_
buildRPM(release_name: 'jenkins-demo', maven_enabled: 'true',maven_deploy: 'false', maven_skip_test: 'true')
pipeline {
    agent {
        docker {
            image 'maven:3-alpine' 
            args '-v /root/.m2:/root/.m2' 
        }
    }
    stages {
        stage('Build') { 
            steps {
                sh 'mvn -B -DskipTests clean package' 
            }
        }
    }
}

