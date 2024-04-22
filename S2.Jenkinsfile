pipeline {
    agent any
    environment {
        INSTANCE_NAME = "aparking-instance-s2"
        PROJECT = "aparking-g11-s1"
        ZONE = "europe-southwest1-a"
        IMAGE = "jenkins-docker" // La imagen de GCE que tiene Docker y Docker Compose
        MACHINE_TYPE = "e2-medium"
        GIT_REPO = "https://github.com/Aparking/AparKing_Backend.git"
        GIT_BRANCH = "deploy/s2"
    }
    stages {
        stage('Prepare Environment') {
            steps {
                script {
                    // Elimina la instancia existente si existe
                    sh "gcloud compute instances delete ${INSTANCE_NAME} --zone=${ZONE} --project=${PROJECT} --quiet || true"
                    // Crea una nueva instancia
                    sh """
                    gcloud compute instances create ${INSTANCE_NAME} \
                        --zone=${ZONE} \
                        --project=${PROJECT} \
                        --source-machine-image=${IMAGE} \
                        --machine-type=${MACHINE_TYPE} \
                        --metadata=startup-script='#!/bin/bash
                        sudo git clone --single-branch --branch ${GIT_BRANCH} ${GIT_REPO} /app
                        cd /app
                        echo "EMAIL_HOST_USER=aparking.g11@gmail.com" > .env
                        echo "EMAIL_HOST_PASSWORD=${env.EMAIL_HOST_PASSWORD}" >> .env
                        sudo docker compose up --build -d'
                    """
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
                body: """El despliegue de la instancia ${INSTANCE_NAME} ha sido completado. 
                En unos minutos podrás acceder a través de la dirección IP: ${'http://'+sh(script: "gcloud compute instances describe ${INSTANCE_NAME} --zone=${ZONE} --format='get(networkInterfaces[0].accessConfigs[0].natIP)'", returnStdout: true).trim()}:3000."""
        }
        failure {
            mail to: 'juancarlosralop@gmail.com, sergiosantiago0403@gmail.com, maria-vico@hotmail.es',
                subject: "Despliegue Fallido: ${INSTANCE_NAME}",
                body: "El despliegue de la instancia ${INSTANCE_NAME} ha fallado."
        }
    }
}
