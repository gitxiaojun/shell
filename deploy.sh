#!/bin/bash
TIME=`date +%F`
APPpath=/opt/app/app
MGTpath=/opt/app/mgt
MAPPpath=/opt/app/mapp
BACKpro=/opt/app/backpro
Back=/home/app/backup
project=/home/app/source1
config=/home/app/scripts

function checkapp(){
        count=`ps -ef |grep app-1 |grep -v grep |wc -l`
        if [ 0 -eq $count ];then
             echo no app process
         else
              /etc/init.d/app  stop
              if [ $? -eq 0 ];then
                 echo app tomcat has stopped
              else
                ps -ef|grep app-1|grep -v grep|awk   '{print $2}'|xargs kill -9
              fi
           
         
         fi
}


function checkmapp(){
        count=`ps -ef |grep mapp |grep -v grep |wc -l`
        if [ 0 -eq $count ];then
             echo no mapp process
         else
              /etc/init.d/mapp stop 
              if [ $? -eq 0 ];then
                 echo mapp tomcat has stopped
              else
                ps -ef|grep mapp|grep -v grep|awk   '{print $2}'|xargs kill -9
              fi
           

         fi
}


  function APP1() {
              checkapp
              cp $APPpath/webapps/ROOT.war   $Back/$TIME-app.war
              sleep 3s
              rm -rf $APPpath/webapps/*
                cp $project/app.war  $APPpath/webapps/ROOT.war
                /etc/init.d/app  start
                sleep 5s
              checkapp
              rm -rf $APPpath/webapps/ROOT/WEB-INF/classes/application.properties && cp /home/app/scripts/application.properties   $APPpath/webapps/ROOT/WEB-INF/classes/ && echo 'weiyin'  >/$APPpath/webapps/ROOT/test.html  &&  rm -f /opt/app/app-1/webapps/ROOT/WEB-INF/classes/redis.properties && cp /home/app/scripts/redis.properties  /opt/app/app-1/webapps/ROOT/WEB-INF/classes/
               /etc/init.d/app  start
             }

              
  function MAPP1() {
              checkmapp
              cd /opt/app/mapp/webapps/  && tar zcf  /home/app/backup/$TIME-mapp.tar.gz  mapp
              sleep 3s
              rm -rf $MAPPpath/webapps/mapp/*
                unzip -q $project/mapp.war  -d $MAPPpath/webapps/mapp
                /etc/init.d/mapp start 
                sleep 5s
                   checkmapp
                    rm -rf  $MAPPpath/webapps/mapp/WEB-INF/classes/config/config.properties
              \cp $config/config.properties   $MAPPpath/webapps/mapp/WEB-INF/classes/config/
                  /etc/init.d/mapp start 
             }


 case $1 in 
        app)
        APP1
        ;;
        mapp)
        MAPP1
        ;;
        all)
        APP1
        MGT1
        MAPP1
        BACKPRO
        ;;
        *)
        echo "you input error!"
        ;;
esac
