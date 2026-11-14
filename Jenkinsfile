// Tests HouseOfPi, then deploys it to the Raspberry Pi at home over SSH. The job (triggers,
// including the daily 07:33 UTC run, and whether it's enabled), the Pi's address (PI_HOST) and its
// pinned host key (PI_KNOWN_HOSTS) are defined in do-k8s-cluster/jenkins/casc, and the ci* steps
// come from that repo's jenkins/shared-library. The pi-ssh key was generated on the CI box.
@Library('ci') _

pipeline {
    agent any
    options {
        timeout(time: 20, unit: 'MINUTES')
    }
    stages {
        stage('Test') {
            steps {
                // The Pi runs Python 3.13 on Debian trixie.
                ciInContainer('python:3.13-trixie') {
                    sh './env-setup/install-test-env && ./env-setup/run-tests'
                }
            }
        }
        stage('Deploy to the Pi') {
            steps {
                sshagent(['pi-ssh']) {
                    // deploy/deploy-to-pi.sh copies the app over and runs deploy/pi-deploy.sh on
                    // the Pi, which puts the previous copy back if the new one doesn't answer.
                    sh '''
                        deploy/deploy-to-pi.sh ssh -o BatchMode=yes -o ConnectTimeout=20 -o ServerAliveInterval=15 \
                            -o StrictHostKeyChecking=yes -o UserKnownHostsFile="$PI_KNOWN_HOSTS" \
                            -o HostKeyAlgorithms=ssh-ed25519 "pi@$PI_HOST"
                    '''
                }
            }
        }
    }
    post {
        // unsuccessful, not failure: a timeout or abort ends the build ABORTED, which also needs a look.
        unsuccessful { ciNotify() }
        fixed { ciNotify() }
    }
}
