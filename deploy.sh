is_mac=0

if [ $is_mac != 1 ]
then
  cd /root/user/hotspot
fi

type=2     # 0, 服务， 1, 采集，2， 全部

if [ $type == 0 ]
then
  sh ./hotspot/depoy_server.sh $is_mac
  echo "deploy server"
elif [ $type == 1 ]
then
  sh ./spider/deploy_spider.sh $is_mac
  echo "deploy spider"
elif [ $type == 2 ]
then
  sh ./hotspot/deploy_server.sh $is_mac
  sh ./spider/deploy_spider.sh $is_mac
  echo "deploy server and spider"
else
  echo "type not found"
fi
echo "deploy"
