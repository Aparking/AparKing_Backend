pipeline {
    agent any
    stages {
        stage('Checkout') {
            steps {
                checkout scm // Clona el repositorio
            }
        }
        stage('Build') {
            steps {
                sh 'docker-compose up --build -d' // Ejecuta docker-compose en el agente
            }
        }
        // Añade más etapas según sea necesario, por ejemplo, para pruebas o despliegue
    }
    post {
        always {
            // Aquí puedes añadir pasos de limpieza o notificaciones
            echo 'Pipeline completado'
        }
    }
}