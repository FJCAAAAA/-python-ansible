# -python-ansible
发生未知故障时，自动化重启各个应用。
site.py入口文件：
盲启流程入口文件，功能包括：全局重启、局部重启、checkurl及数据源连接检测，重启部分依赖ansible调用playbook、检测部分依赖对data目录下个文件中URL的返回结果。

Playbook文件：
tasks.yml：任务模板文件，各层的任务一般都可以写到该文件中，指定不同的tags。
Lb_out.yml：外部负载层
Biz_gateway.yml：业务-网关层
Biz_platform.yml：业务-平台层
Mid.yml：中间件层
Mid_redis.yml：redis（redis不是系统服务，不能和其他中间件使用同样的命令，所以单独配置playbook文件）
Biz_base.yml：业务-业务基础层
Biz_account.yml：业务-账务层
Biz_manage.yml：业务-管理层
hosts：ansible的hosts文件

data文件：
checkurl.txt：各层的checkurl
checkdb.txt：各层的检测数据源连接的url
bizbasecheckurl.txt：业务-基础层的checkurl
bizbasecheckdb.txt：业务-基础层的检测数据源连接的url
