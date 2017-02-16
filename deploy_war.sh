#set -x
export NODE=$1
export SERVICE=$2
export WAR_FILE=$3
export DEPLOY_FOLDER=$4
export TOMCAT_FOLDER=$5
export TOMCAT_WEBAPP=$6
export NOW=$(date +"%m-%d-%Y-%s")  

echo "Starting to deploy $SERVICE to $NODE ......"

echo "Transfering war to $NODE"
scp $WAR_FILE root@$NODE:$DEPLOY_FOLDER
ssh root@$NODE chown appuser:appuser $DEPLOY_FOLDER/$TOMCAT_WEBAPP.war 

echo "Stopping $NODE $SERVICE Service"
ssh root@$NODE systemctl stop $SERVICE

echo "Backup the old war files"
ssh root@$NODE zip -r $DEPLOY_FOLDER/$SERVICE_$NOW.zip $TOMCAT_FOLDER/webapps/$TOMCAT_WEBAPP/*
ssh root@$NODE chown appuser:appuser $DEPLOY_FOLDER/*.zip

echo "Delete the old war files"
ssh root@$NODE rm -rf $TOMCAT_FOLDER/webapps/$TOMCAT_WEBAPP

echo "Copy new version files"
ssh root@$NODE unzip -q $DEPLOY_FOLDER/$TOMCAT_WEBAPP.war -d $TOMCAT_FOLDER/webapps/$TOMCAT_WEBAPP
ssh root@$NODE chown -R appuser:appuser $TOMCAT_FOLDER/webapps/$TOMCAT_WEBAPP

echo "Starting $SERVICE Service"
ssh root@$NODE systemctl start $SERVICE

echo "Deployment on $NODE FOR $SERVICE end......"