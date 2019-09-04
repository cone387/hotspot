ps -ef | grep newsdeploy.py |awk '{print $2}' | xargs kill -9
ps -ef | grep runnews.py |awk '{print $2}' | xargs kill -9

cd /home/admin/acq-news-config


# wget http://logtail-release-cn-hangzhou.oss-cn-hangzhou.aliyuncs.com/linux64/logtail.sh -O logtail.sh; chmod 755 logtail.sh; ./logtail.sh install cn-hangzhou-internet

# pip3 install watchdog
#pip3 install redis

nohup python3 newsdeploy.py -P 1 -t 4 -I 10 > news.log 2>&1 &

echo "deploy"