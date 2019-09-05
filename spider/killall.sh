ps -ef | grep hotspot_deploy.py |awk '{print $2}' | xargs kill -9
ps -ef | grep run_hotspot.py |awk '{print $2}' | xargs kill -9
