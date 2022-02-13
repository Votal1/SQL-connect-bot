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
                dir ('ansible') {
                    sh 'ansible-playbook build.yml'
                }
            }
        }
        stage('deploy') {
            steps {
              dir ('ansible') {
                withCredentials([string(credentialsId: 'TOKEN', variable: 'TOKEN'), string(credentialsId: 'REDIS_HOST', variable: 'REDIS_HOST'), string(credentialsId: 'REDIS_PASSWORD', variable: 'REDIS_PASSWORD')]) {
                  sh ("""
                  ansible-playbook deploy.yml -e '{"TOKEN": "${TOKEN}", "REDIS_HOST": "${REDIS_HOST}", "REDIS_PASSWORD": "${REDIS_PASSWORD}"}'
                  """)
                }
              }
            }
        }
    }
}

