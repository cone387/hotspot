from cone.deployer import Deployer


if __name__ == "__main__":
    deployer = Deployer(executable='run_werb.py', \
        deploy_num=2, exec_parmas={'-t': '5', '-d': '0'}, check_log=True)
    deployer.deploy()