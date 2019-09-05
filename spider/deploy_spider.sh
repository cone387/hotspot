ps -ef | grep hotspot_deploy.py |awk '{print $2}' | xargs kill -9
ps -ef | grep run_hotspot.py |awk '{print $2}' | xargs kill -9

if [ $1 == '0' ]
then
  cd /root/user/hotspot/spider
else
  cd /Users/cone/cone/me/projects/hotspot/spider/
fi

nohup python3 hotspot_deploy.py -P 2 -t 4 -I 10 > website.spider.log 2>&1 &

echo "deploy"
