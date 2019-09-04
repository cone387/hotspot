cd /root/user/hotspot

ps -ef | grep manage.py |awk '{print $2}' | xargs kill -9

type = 0     # 0, 采集， 1, 服务，2， 全部

if [$type == 0]
then
  cd hotspot
  python3 manage.py makemigrations
  python3 manage.py migrate
  python3 manage.py runserver 0.0.0.0:80
elif [$type == 1]
then
  nohup python3 deploy_spider.py -P 2 -t 4 -I > website.spider.log 2>&1 &
elif [$tpye == 2]
then
  cd hotspot
  python3 manage.py makemigrations
  python3 manage.py migrate
  python3 manage.py runserver 0.0.0.0:80
  cd ..
  nohup python3 deploy_spider.py -P 2 -t 4 -I > website.spider.log 2>&1 &
else
  echo "not type"
echo "deploy"
