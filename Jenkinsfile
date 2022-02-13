properties([pipelineTriggers([githubPush()])])

pipeline {
    agent {
        label 'python'
    }

    environment {
        INSTANCE_IP = ''
    }

    stages {
        stage('git') {
            steps {
                checkout([
                    $class: 'GitSCM',
                    branches: [[name: 'main']],
                    userRemoteConfigs: [[url: 'https://github.com/Votal1/SQL-connect-bot.git']]
                ])
            }
        }
        stage('build') {
            steps {
                dir ('terraform') {
                    sh 'terraform init'
                    sh 'terraform destroy --auto-approve'
                    sh 'terraform apply --auto-approve'
                    script {
                        INSTANCE_IP = sh(returnStdout: true, script: "terraform output -raw instance_public_ip").trim()
                    }
                    writeFile (file: '../ansible/hosts.txt', text: '[server]\n' + INSTANCE_IP)
                    sleep(10)
                }
            }
        }
        stage('deploy') {
            steps {
              dir ('ansible') {
                sh 'ansible-playbook deploy.yml'
              }
            }
        }
    }
}

