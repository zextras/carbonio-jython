def mvnCmd(String cmd) {
    sh 'mvn -B -s settings-jenkins.xml ' + cmd
}
pipeline {
    agent {
        node {
            label 'carbonio-agent-v1'
        }
    }
    parameters {
        booleanParam defaultValue: false, description: 'Skip sonar analysis.', name: 'SKIP_SONARQUBE'
    }
    environment {
        JAVA_OPTS = '-Dfile.encoding=UTF8'
        LC_ALL = 'C.UTF-8'
        MAVEN_OPTS = "-Xmx4g"
        GITHUB_BOT_PR_CREDS = credentials('jenkins-integration-with-github-account')
    }
    options {
        buildDiscarder(logRotator(numToKeepStr: '25'))
        timeout(time: 2, unit: 'HOURS')
        skipDefaultCheckout()
    }
    stages {
        stage('Checkout') {
            steps {
                checkout scm
                withCredentials([file(credentialsId: 'jenkins-maven-settings.xml', variable: 'SETTINGS_PATH')]) {
                    sh "cp ${SETTINGS_PATH} settings-jenkins.xml"
                }
            }
        }
        stage('Build') {
            steps {
                mvnCmd("clean package")
                sh 'cp -r configd package staging'
                stash includes: 'staging/**', name: 'staging'
            }
        }
        stage('Build deb/rpm') {
            stages {
                stage('pacur') {
                    parallel {
                        stage('Ubuntu 20.04') {
                            agent {
                                node {
                                    label 'pacur-agent-ubuntu-20.04-v1'
                                }
                            }
                            steps {
                                unstash 'staging'
                                sh 'cp -r staging /tmp'
                                sh 'sudo pacur build ubuntu-focal /tmp/staging/packages'
                                stash includes: 'artifacts/', name: 'artifacts-ubuntu-focal'
                            }
                            post {
                                always {
                                    archiveArtifacts artifacts: 'artifacts/*.deb', fingerprint: true
                                }
                            }
                        }
                        stage('Rocky 8') {
                            agent {
                                node {
                                    label 'pacur-agent-rocky-8-v1'
                                }
                            }
                            steps {
                                unstash 'staging'
                                sh 'cp -r staging /tmp'
                                sh 'sudo pacur build rocky-8 /tmp/staging/packages'
                                stash includes: 'artifacts/', name: 'artifacts-rocky-8'
                            }
                            post {
                                always {
                                    archiveArtifacts artifacts: 'artifacts/*.rpm', fingerprint: true
                                }
                            }
                        }
                    }
                }
            }
        }
    }
}