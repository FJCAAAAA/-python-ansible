#!/usr/local/python3.6/bin/python3.6
#-*- coding:utf-8 -*-
import sys
import os
import hashlib
import time
import traceback
import getpass
import urllib.request
import subprocess

#定义环境标志
biaozhi= '''
    ***************************************************** 
    *                                                   *
    *      55555       #  #          PPPPP   EEEEE      *
    *      5         #######         P    P  E          *
    *      55555      #  #           PPPPP   EEEEE      *
    *           5   #######          P       E          *
    *      55555     #  #            P       EEEEE      *
    *                                                   *
    *     B环境-盲启流程即将启动，请慎重选择输入！！！  *
    *                                                   *
    *****************************************************
'''
DBHOSTNAME='bjape05-rac'
all_checkurl='data/checkurl.txt'
all_checkdb='data/checkdb.txt'
all_switch='data/all_switch_txt'
bizbase_checkurl='data/bizbasecheckurl.txt'
bizbase_checkdb='data/bizbasecheckdb.txt'
bizbase_switch='data/bizbase_switch'

#密码验证函数
def pass_check():
    password='4bfbc71fc8e101d536aac98c4d6e6604'
    my_pass=str(getpass.getpass("请输入密码："))
    m=hashlib.md5()
    m.update(my_pass.encode('utf8'))
    if m.hexdigest() == password:
        print ("密码正确，开启盲启流程。")
        time.sleep(3)
    else:
        print ("密码错误，即将退出！")
        sys.exit()

#核对IP地址列表函数
def IP_check():
    with open('hosts','r') as f:
        print(f.read())
    my_IPcomp=int(input("是否继续（1 继续，2 退出）："))
    if my_IPcomp == 1:
        print("IP正确！")
    elif my_IPcomp == 2:
        print("IP有误，请手工核对！")
        sys.exit()
    else:
        print("输入的数字无效！")
        sys.exit()

#用于装饰器，检查完URL和数据源函数后，如果开关文件存在，判断是否再次检查
def again(f):
    def inner(a,b,c,d):
        f(a,b,c,d)
        while os.path.exists(c):
            os.remove(c)
            my_again = input("是否再次检查yes/no:")
            if my_again == 'yes':
                f(a, b, c, d)
            else:
                pass
    return inner

#检查URL和数据源函数
'''
checkurl：表示URL路径
checkdb：表示数据源路径
switch：表示开关文件，包括all_switch和bizbase_switch
yes_no：表示是否删除开关文件
'''
@again
def url_db_check(checkurl,checkdb,switch,yes_no):
    falseurl=[]
    falsedb=[]
    # switch = '_'.join([piece, 'switch'])
    with open(checkurl,'r') as f1:
        my_url=f1.readlines()
    with open(checkdb,'r') as f2:
        my_db=f2.readlines()
    for url in my_url:
        try:
            url_response=urllib.request.urlopen(url,timeout=3)
            url_code=url_response.code
            url_page=url_response.read().decode('utf8')
            url_status=int(url_page.count('OK'))
            if url_status < 1:
                falseurl.append(url)
        except:
            falseurl.append(url)
    for db in my_db:
        try:
            db_response = urllib.request.urlopen(db, timeout=3)
            db_code = db_response.code
            db_page = db_response.read().decode('utf8')
            if DBHOSTNAME not in db_page:
                falsedb.append(db)
        except:
            falsedb.append(db)
    if falseurl:
        print("某些checkurl检查异常，这些checkurl分别是：")
        for m in falseurl:
            print(m)
        with open(switch,'w') as f:
            f.write('1')
    else:
        print("checkurl检查正常！")
    if falsedb:
        print("某些数据源检查异常，对应的url分别是：")
        for n in falsedb:
            print(n)
        with open(switch,'a') as f:
            f.write('\n2')
    else:
        print("数据源检查正常！")
    if os.path.exists(switch):
        if yes_no == 'yes':
            os.remove(switch)


#停止domain及服务函数
def stop_Biz_manage():
    subprocess.call('ansible-playbook -i hosts Biz_manage.yml --tags=stopdomain',shell=True)
def stop_Biz_gateway():
    subprocess.call('ansible-playbook -i hosts Biz_gateway.yml --tags=killdomain',shell=True)
def stop_Biz_platform():
    subprocess.call('ansible-playbook -i hosts Biz_platform.yml --tags=killdomain',shell=True)
def stop_Biz_account():
    subprocess.call('ansible-playbook -i hosts Biz_account.yml --tags=killdomain',shell=True)
def stop_Biz_base():
    subprocess.call('ansible-playbook -i hosts Biz_base.yml --tags=killdomain',shell=True)
def stop_Mid():
    subprocess.call('ansible-playbook -i hosts Mid.yml --tags=stopservice',shell=True)
def stop_Mid_redis():
    subprocess.call('ansible-playbook -i hosts Mid_redis.yml --tags=killredis',shell=True)

#启动domain及服务函数
def start_Biz_manage():
    subprocess.call('ansible-playbook -i hosts Biz_manage.yml --tags=startdomain',shell=True)
def start_Biz_gateway():
    subprocess.call('ansible-playbook -i hosts Biz_gateway.yml --tags=startdomain',shell=True)
def start_Biz_platform():
    subprocess.call('ansible-playbook -i hosts Biz_platform.yml --tags=startdomain',shell=True)
def start_Biz_account():
    subprocess.call('ansible-playbook -i hosts Biz_account.yml --tags=startdomain',shell=True)
def start_Biz_base():
    subprocess.call('ansible-playbook -i hosts Biz_base.yml --tags=startdomain',shell=True)
def start_Mid():
    subprocess.call('ansible-playbook -i hosts Mid.yml --tags=startservice',shell=True)
def start_Mid_redis():
    subprocess.call('ansible-playbook -i hosts Mid_redis.yml --tags=startredis',shell=True)

#重启ha函数
def restart_ha():
    subprocess.call('ansible ha -m service -a "name=haproxy state=restarted"',shell=True)

#用于装饰器，判断是否执行
def confirm(f):
    def inner():
        my_confirm = input("请输入yes/no:")
        if my_confirm == 'yes':
            f()
        else:
            print("请重新选择！")
            pass
    return inner

#停止各层domain
@confirm
def all_stop():
    stop_Biz_manage()
    time.sleep(10)
    stop_Biz_gateway()
    stop_Biz_platform()
    stop_Biz_account()
    stop_Biz_base()
    time.sleep(2)
    restart_ha()
    stop_Mid()
    stop_Mid_redis()

#启动各层domain
@confirm
def all_start():
    start_Mid()
    start_Mid_redis()
    time.sleep(2)
    start_Biz_base()
    time.sleep(30)
    url_db_check(bizbase_checkurl,bizbase_checkdb,bizbase_switch,'no')
    start_Biz_account()
    start_Biz_platform()
    start_Biz_gateway()
    time.sleep(80)
    url_db_check(all_checkurl,all_checkdb,all_switch,'no')
    start_Biz_manage()
    time.sleep(20)
    url_db_check(all_checkurl, all_checkdb, all_switch, 'no')

#重启网关层
@confirm
def Biz_gateway_restart():
    stop_Biz_gateway()
    time.sleep(2)
    start_Biz_gateway()
    time.sleep(20)
    url_db_check(all_checkurl,all_checkdb,all_switch,'no')

#重启中间件层
@confirm
def Mid_restart():
    stop_Mid()
    stop_Mid_redis()
    time.sleep(4)
    restart_ha()
    start_Mid()
    start_Mid_redis()
    time.sleep(2)
    url_db_check(all_checkurl, all_checkdb, all_switch, 'no')

#重启平台层
@confirm
def Biz_platform_restart():
    stop_Biz_platform()
    time.sleep(2)
    start_Biz_platform()
    time.sleep(40)
    url_db_check(all_checkurl, all_checkdb, all_switch, 'no')

#重启账务层
@confirm
def Biz_account_restart():
    stop_Biz_account()
    time.sleep(2)
    start_Biz_account()
    time.sleep(20)
    url_db_check(all_checkurl, all_checkdb, all_switch, 'no')

#重启基础服务层
@confirm
def Biz_base_restart():
    stop_Biz_base()
    time.sleep(2)
    start_Biz_base()
    time.sleep(20)
    url_db_check(all_checkurl, all_checkdb, all_switch, 'no')

#重启管理层
@confirm
def Biz_manage_restart():
    stop_Biz_manage()
    time.sleep(10)
    start_Biz_manage()
    time.sleep(20)
    url_db_check(all_checkurl, all_checkdb, all_switch, 'no')


#选择全局重启or局部重启or退出函数
def restart():
    while True:
        print("help:\n a（全局启动流程）;\n b（局部启动流程）;\n e (退出)")
        my_letter = input("请输入字母：")
        if my_letter == 'a':
            while True:
                print("help:\n 1（停止各层domain及服务）;\n 2（启动各层domain及服务）;\n 0 (退回到入口)")
                all_restar_letter = int(input("请输入数字:"))
                if all_restar_letter == 1:
                    all_stop()
                elif all_restar_letter == 2:
                    all_start()
                elif all_restar_letter == 0:
                    break
        if my_letter == 'b':
            while True:
                print(
                    "help:\n 0（退回）;\n 1（重启业务-网关层）;\n 2 (重启中间件层);\n 3 (重启业务-平台层);\n 4 (重启业务-账务层);\n 5 (重启业务-基础服务层);\n 6 (重启业务-管理层)")
                restart_letter = int(input("请输入数字:"))
                if restart_letter == 1:
                    Biz_gateway_restart()
                elif restart_letter == 2:
                    Mid_restart()
                elif restart_letter == 3:
                    Biz_platform_restart()
                elif restart_letter == 4:
                    Biz_account_restart()
                elif restart_letter == 5:
                    Biz_base_restart()
                elif restart_letter == 6:
                    Biz_manage_restart()
                elif restart_letter == 0:
                    break
        if my_letter == 'e':
            sys.exit()


if __name__ == "__main__":
    try:
        print(biaozhi)
        pass_check()
        IP_check()
        url_db_check(all_checkurl,all_checkdb,all_switch,'yes')
        restart()
    except SystemExit:
        print("程序即将退出！")
        time.sleep(3)
    except:
        traceback.print_exc()
