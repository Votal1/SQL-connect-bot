properties([pipelineTriggers([githubPush()])])

pipeline {
    agent any
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
        stage('prepare workspace') {
            steps {
                dir ('terraform') {
                    sh 'terraform init'
                    // sh 'terraform destroy --auto-approve'
                    sh 'terraform apply --auto-approve'
                    script {
                        INSTANCE_IP = sh(returnStdout: true, script: "terraform output -raw instance_public_ip").trim()
                    }
                    writeFile (file: '../ansible/hosts.txt', text: '[server]\n' + INSTANCE_IP)
                    sleep(10)
                }
                dir ('ansible') {
                    sh 'ansible-playbook prepare.yml'
                }
            }
        }
        stage('build') {
            steps {
                dir ('ansible') {
                    sh 'ansible-playbook build.yml'
                }
            }
        }
        stage('test') {
            steps {
                dir ('ansible') {
                    sh 'ansible-playbook test.yml'
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
    post {
     success { 
        withCredentials([string(credentialsId: 'TOKEN2', variable: 'TOKEN2')]) {
        sh  ("""
            curl -s -X POST https://api.telegram.org/bot${TOKEN2}/sendMessage -d chat_id=456514639 -d text='\u2705 Build ${env.BUILD_NUMBER} successful.\nJob - ${env.JOB_NAME}'
        """)
        }
     }
     failure {
        withCredentials([string(credentialsId: 'TOKEN2', variable: 'TOKEN2')]) {
        sh  ("""
            curl -s -X POST https://api.telegram.org/bot${TOKEN2}/sendMessage -d chat_id=456514639 -d text='\u274E Build ${env.BUILD_NUMBER} failed.\nJob - ${env.JOB_NAME}'
        """)
        }
     }

    }

}

