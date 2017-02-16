NOW=$(date +"%m-%d-%Y")
sftp -b /dev/stdin -P 6689 root@112.64.186.42 << EOF 2>&1 >> sftp_log_$NOW.log
cd /var/lib/jenkins/deploy/dodopal-release/
get *.war
get *.zip
bye
EOF