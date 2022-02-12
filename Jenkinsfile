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
                        echo $(INSTANCE_IP)
                    }
                }
                sh(returnStdout: true, script: '''#!/bin/bash
                    if [ $(sudo docker ps -a -q) ];then
                    sudo docker rm -f $(sudo docker ps -q)
                    fi
                '''.stripIndent())
                sh(returnStdout: true, script: '''#!/bin/bash
                    if [ $(sudo docker images -a -q) ];then
                    sudo docker rmi -f $(sudo docker images -a -q)
                    fi
                '''.stripIndent())
                sh 'sudo docker build -t bot .'
            }
        }
        stage('deploy') {
            steps {
                sh 'sudo docker run bot &'
            }
        }
    }
}
