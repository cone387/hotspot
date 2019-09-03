ps -ef | grep newsdeploy.py |awk '{print $2}' | xargs kill -9
ps -ef | grep runnews.py |awk '{print $2}' | xargs kill -9
