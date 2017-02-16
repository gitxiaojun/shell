NOW=$(date +"%m-%d-%Y")
NODE = $1

echo "Deployment on $NODE are started!"

#echo "getting war files from shanghai 230 server"
#./sftp/sftp_get_war.sh

echo "deploying test on $NODE ..."
./deploy_war.sh $NODE test sftp/test.war /home/appuser/deploy/test /home/appuser/test test

echo "deploying user1 on $NODE ..."
./deploy_war.sh $NODE user1 sftp/test.war /home/appuser/deploy/user1 /home/appuser/user1 user1

echo "deploying portal on $NODE cluster 1 ..."
./deploy_war.sh $NODE c1 sftp/ment.war /home/appuser/deploy/portal /home/appuser/cluster_1 ment

echo "deploying portal on $NODE cluster 2 ..."
./deploy_war.sh $NODE c2 sftp/ment.war /home/appuser/deploy/portal /home/appuser/cluster_2 ment

echo "deploying product on $NODE ..."
./deploy_war.sh $NODE product sftp/webapp.war /home/appuser/deploy/product /home/appuser/product webapp

echo "deploying web on $NODE ..."
./deploy_war.sh $NODE web sftp/web.war /home/appuser/deploy/web /home/appuser/web web

echo "deploy static on $NODE"
./deploy_static.sh $NODE sftp/static.zip /home/appuser/deploy/static /opt/static

echo "Deployment on $NODE are finished!"

