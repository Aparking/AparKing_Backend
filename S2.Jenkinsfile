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
                        --image=${IMAGE} \
                        --machine-type=${MACHINE_TYPE} \
                        --metadata=startup-script='#!/bin/bash
                        git clone -b ${GIT_BRANCH} ${GIT_REPO} /app
                        cd /app
                        docker-compose up --build -d'
                    """
                }
            }
        }
    }
    post {
        always {
            echo 'Pipeline completed.'
            // Aquí puedes añadir comandos para limpiar recursos si es necesario
        }
    }
}
