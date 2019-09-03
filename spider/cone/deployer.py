
import subprocess
import time
import sys
from os.path import getsize
import getopt
import os


def init_logfile(logfile):
    with open(logfile, 'w', encoding='utf-8') as f:
        pass


class Deployer(object):
    """
        # 理想的部署情况应该是，
        1、要运行那个脚本
        2、要启动几个该脚本
        2、要传递那些参数给脚本或程序
        3、提供一种监控日志的方法来监控程序在不在正常运行
        所以应该提供一下参数：
        executable: 要执行的文件
        deploy_num: 要运行多少个，默认为1个
        runner: 运行程序
        exec_params: 要传递给脚本的参数
        daemon: 是启动以后就退出该部署进程还是继续运行以监控脚本的异常
        check_log: 分配日志文件给子进程，并且持续监控日志文件的变化，没有变化则重启程序。日志文件传递给自己程以固定的参数形式--logfile='logfile'
        logdir: 分配的日志文件在那个文件夹
        可以通过命令行传递以下参数：
        -F或--filenmae=: 要执行的文件
        -R或--runner=: 执行程序, 默认为python3
        -D或--daemon=: 1或0, 对应daemon为True或False, 默认为1即True
        -P或--process=: int, 对应你deploy_num, 默认为1即
        -l或--logdir=: 日志文件夹, 对应logdir, 默认为logs
        -C或--checklog=: 1或0, 对应check_log为True或False, 默认为0即False
        -H或--help: 输出帮助信息
        传递的其余小写的参数均会传递给启动的子进程
    """
    def __init__(self, executable=None, deploy_num=1, runner='python3', exec_parmas={}, \
        is_linux=False, logdir='logs', interval=2, check_log=False, daemon=True):
        self.executable = executable
        self.runner = runner
        self.arg_list = []
        self.is_linux = is_linux
        self.process_map = {}
        self.num = deploy_num
        self.check_log = check_log
        self.logdir = logdir
        self.interval = interval   # 单位分钟
        self.daemon = daemon
        opts, _ = getopt.getopt(sys.argv[1:], 'F:R:P:L:D:I:C:H%s' % ':'.join([chr(x) for x in range(97, 123)]), ['--filename=', '--runner=', '--help', 'logdir=', "interval=", "process=", 'checklog=', 'daemon='])
        for opt, arg in opts:
            if opt in ('-P', '--process'):
                self.num = int(arg)
            elif opt in ('-C', '--checklog'):
                self.check_log = arg == '1'
            elif opt in ('-D', '--daemon'):
                self.daemon = arg == '1'
            elif opt in ('-I', '--interval'):
                self.interval = float(arg)
            elif opt in ('-L', '--logdir'):
                self.logdir = arg
            elif opt in ('-R', '--runner'):
                self.runner = 'python3'
            elif opt in ('-F', '--fielname'):
                self.executable = arg
            elif opt in ('-H', '--help'):
                print(self.__doc__)
                exit(0)
            else:
                exec_parmas[opt] = arg
        for k, v in exec_parmas.items():
            self.arg_list.append(k)
            self.arg_list.append(v)
        assert self.executable is not None, '执行文件不能为空'
        if not os.path.exists(self.logdir):
            os.mkdir(self.logdir)
        print(
            "Deployer with:\n\
            executeable: %s\n\
            runner: %s\n\
            deploy_num: %s\n\
            daemon: %s\n\
            checklogfile: %s\n\
            check_interval: %s(min)\n\
            execute params: %s"%(self.executable, self.runner, self.num, self.daemon, self.check_log, self.interval, self.arg_list))
        
    def deploy(self):
        for i in range(self.num):
            log_file = os.path.join(self.logdir, '%s_%s.log'%(self.executable.split('.')[0], i))
            init_logfile(log_file)
            command_list = [self.runner, self.executable] + self.arg_list
            if self.check_log:
                command_list.append('-l')
                command_list.append(log_file)
            popen = subprocess.Popen(command_list)
            self.process_map[popen.pid] = {'popen': popen, 'log-size': 0, 'command-list': command_list, 'log-file': log_file}
        if self.daemon:
            self.monitor_process()


    def kill_process(self, pid=None):
        if pid is None:
            for pid, process in self.process_map.items():
                process['popen'].kill()
                print("killed process<%s>"%pid)
            self.process_map.clear()
        else:
            process = self.process_map.get(pid)
            if process:
                process['popen'].kill()
                print("killed process<%s> "%pid)
                del self.process_map[pid]

    def is_process_alive(self, process):
        return process.poll() is None

    def restart_process(self, process):
        new_process = process.copy()
        process['popen'].kill()
        new_process['popen'] = subprocess.Popen(process['command-list'])
        self.process_map[new_process['popen'].pid] = new_process
        print("Restart %s, pid is %s now"%(process['popen'].pid, new_process['popen'].pid))
        if new_process['popen'].pid != process['popen'].pid:
            del self.process_map[process['popen'].pid]
        
    def clear_logfile(self, logfile):
        with open(logfile, 'w', encoding='utf-8') as f:
            pass
        
    def monitor_process(self):
        while True:
            try:
                # print("Moniting...")
                time.sleep((self.interval * 60) or 60)  # frequency分钟监控一次
            except KeyboardInterrupt:
                break
            for pid, process in list(self.process_map.items()):
                if not self.is_process_alive(process['popen']):  # 若果没有该进程了则重新启动并更新内部的process_map
                    self.restart_process(process)
                    continue
                if not self.check_log:   # 是否要根据日志进一步判断进程有没有活动
                    continue
                log_size = getsize(process['log-file'])
                if process['log-size'] == log_size: # 日过日志大小没有变化
                    print(f"[{pid}]logsize doesn't change")
                    self.restart_process(process)
                else:
                    self.process_map[pid]['log-size'] = log_size
        self.kill_process()


if __name__ == "__main__":
    deployer = Deployer('test.py')
    deployer.deploy()


    