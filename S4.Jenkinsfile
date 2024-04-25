pipeline {
    agent any
    environment {
        INSTANCE_NAME = "aparking-backend-s4"
        PROJECT = "aparking-g11-s3"
        GIT_REPO = "https://github.com/Aparking/AparKing_Backend.git"
        GIT_BRANCH = "deploy/s4"
        ZONE = "europe-southwest1-a"
    }
    stages {
        stage('Clone Repository') {
            steps {
                checkout([$class: 'GitSCM', branches: [[name: "*/${GIT_BRANCH}"]], userRemoteConfigs: [[url: "${GIT_REPO}"]]])
            }
        }
        stage('Prepare Environment') {
            steps {
                script {
                    sh """
                    echo "EMAIL_HOST_USER=aparking.g11@gmail.com" > .env
                    echo "EMAIL_HOST_PASSWORD=${env.EMAIL_HOST_PASSWORD}" >> .env
                    """
                }
            }
        }
        stage('Initialize App Engine') {
            steps {
                script {
                    // Intenta crear la aplicación de App Engine y captura cualquier error
                    def output = sh(script: "gcloud app create --region=europe-west --project=${PROJECT} || true", returnStdout: true).trim()
                    if (output.contains("already exists")) {
                        echo "App Engine application already exists."
                    } else {
                        echo "App Engine application created or checked successfully."
                    }
                }
            }
        }
        stage('Deploy to App Engine') {
            steps {
                script {
                    sh 'cp ./docker/backend.Dockerfile ./Dockerfile'
                    // Despliega la aplicación
                    sh "gcloud app deploy app.yaml --quiet --project=${PROJECT}"
                    sh 'rm ./Dockerfile'
                }
            }
        }
    }
    post {
        always {
            echo 'Pipeline completed.'
        }
        success {
            mail to: 'juancarlosralop@gmail.com, sergiosantiago0403@gmail.com, maria-vico@hotmail.es',
                subject: "Despliegue Completado: ${INSTANCE_NAME}",
                body: "El despliegue de ${INSTANCE_NAME} en App Engine ha sido completado exitosamente. \n Puedes verificar la aplicación en la consola de Google Cloud."
        }
        failure {
            mail to: 'juancarlosralop@gmail.com, sergiosantiago0403@gmail.com, maria-vico@hotmail.es',
                subject: "Despliegue Fallido: ${INSTANCE_NAME}",
                body: "El despliegue de ${INSTANCE_NAME} en App Engine ha fallado."
        }
    }
}