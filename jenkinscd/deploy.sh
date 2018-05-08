sudo su
su jenkins
ssh jenkins@46.101.135.45 <<EOF
 cd /var/www/kcsf-api
 sudo su
 eval `ssh-agent -s`
 ssh-add /jenkins/.ssh/id_rsa
 git pull
 rm -rf venv
 service apache2 restart
 exit       
EOF
