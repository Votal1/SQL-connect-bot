properties([pipelineTriggers([githubPush()])])

pipeline {
    agent {
        label 'python'
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
                dir (terraform) {
                    sh 'ls'
                }
                sh 'ls'
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
