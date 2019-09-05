ps -ef | grep manage.py |awk '{print $2}' | xargs kill -9

if [ $1 == '0']
then
  cd /root/user/hotspot/hotspot
fi

python3 manage.py makemigrations
python3 manage.py migrate
python3 manage.py runserver 0.0.0.0:80