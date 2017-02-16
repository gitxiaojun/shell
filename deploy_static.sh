#set -x
export NODE=$1
export ZIP_FILE=$2
export DEPLOY_FOLDER=$3
export STATIC_FOLDER=$4
export NOW=$(date +"%m-%d-%Y-%s")  

echo "Starting to deploy static to $NODE ......"

echo "Transfering static zip file to $NODE"
scp $ZIP_FILE root@$NODE:$DEPLOY_FOLDER

echo "Backup the old static files"
ssh root@$NODE zip -r $DEPLOY_FOLDER/webstatic_$NOW.zip $STATIC_FOLDER/*

echo "Delete the old static files"
ssh root@$NODE rm -rf $STATIC_FOLDER/*

echo "Copy new version static files"
ssh root@$NODE unzip -o $DEPLOY_FOLDER/webstatic.zip -d $STATIC_FOLDER

echo "Deployment on $NODE end......"