# ok-system-helper

![](https://img.shields.io/badge/python-3.x-blue.svg) ![](https://img.shields.io/badge/version-1.0.0-brightgreen.svg) ![](https://img.shields.io/badge/license-MIT-000000.svg)

ok-system-helper是一个简单的系统硬件的实时信息收集工具，使用python3.x开发，支持哪些硬件：CPU、内存、SWAP、磁盘、网卡流量。用户可在自己的项目中直接引入、开箱即用，或者结合flask等web框架轻松做成http接口供前端调用，亦可通过注册中心（Eureka、Consul、Nacos等）的加持，做成微服务供其他系统调用。



# 提供哪些方法

| 方法名称 | 说明                         |
| :------- | :--------------------------- |
| cpu()    | 获取cpu的使用信息            |
| memory() | 获取 '物理内存' 的使用信息   |
| swap()   | 获取 '交换内存' 的使用信息   |
| disk()   | 获取磁盘的使用信息           |
| net()    | 获取自开机以来，网卡的IO信息 |

提示：具体每个方法使用说明，请参考system_helper.py源码中的注释。



# 配置说明

配置文件config.conf（如果不需要开启流量统计功能及对外提供HTTP服务，则不需要该配置文件）

```
[application]
name=ok-system-helper
host=127.0.0.1
port=7002

[webservice]
appid=123456   # 请求HTTP服务时的唯一验证码（作为GET请求的参数携带）

[redis]
host=127.0.0.1
port=6379
password=foobared

[mysql]
host=127.0.0.1
port=3306
dbname=blog
username=root
password=root
```



# 使用举例

```python
from core.system_helper import SysInfosCollector

collector = SysInfosCollector()

print(collector.cpu())
'''
{
	'platform': 'windows',
	'physical_count': 4,  # 物理数量
	'logical_count': 8,  # 逻辑数量
	'usage_percent': 6.8,
	'user': 0.4,
	'system': 1.6,
	'idle': 97.7,
	'interrupt': 0.2,
	'dpc': 0.2,
	'boot_time': '2019-09-12 18:49:43'
}
'''

print(collector.memory())
'''
{
	'total': 16331.78,  # 单位MB
	'available': 7945.26,
	'used': 8386.52,
	'free': 7945.26,
	'usage_percent': 51.4
}
'''

print(collector.swap())
'''
{
	'total': 18891.78,  # 单位MB
	'used': 15034.0,
	'free': 3857.78,
	'sin': 0.0,
	'sout': 0.0,
	'usage_percent': 79.6
}
'''

print(collector.disk())
'''
{
	'C:\\': {
		'total': 117.85,  # 单位GB
		'used': 91.86,
		'free': 25.98,
		'usage_percent': 78.0
	},
	'D:\\': {
		'total': 300.03,
		'used': 67.83,
		'free': 232.2,
		'usage_percent': 22.6
	},
	'E:\\': {
		'total': 599.64,
		'used': 185.56,
		'free': 414.07,
		'usage_percent': 30.9
	}
}
'''

print(collector.net())
'''
[{
	'name': '以太网',
	'ip': '192.168.1.4',
	'io_in': 165775.09,  # 单位MB
	'io_out': 26482.64  
}, {
	'name': 'WLAN 2',
	'ip': '169.254.209.196',
	'io_in': 0.0,
	'io_out': 0.0
}, {
	'name': '本地连接* 3',
	'ip': '169.254.211.243',
	'io_in': 0.0,
	'io_out': 0.0
}]
'''
```

提示：开启流量统计(需先建库建表，脚本tb_net_io.sql)功能及对外提供HTTP服务，请查看scheduled_task.py和web_service.py中的代码。



# 问题和建议

如果有什么问题、建议、BUG都可以在这个[Issue](https://github.com/superman-stack/mail-helper/issues/1)和我讨论



# 公众号

关注不迷路，微信扫描下方二维码或搜索关键字“**spartacus**”，关注「**spartacus**」公众号，时刻收听**spartacus**更新通知！

在公众号后台回复“**加群**”，即可加入「**spartacus**」扯淡交流群！

![mp_qrcode](imgs/mp_qrcode.jpg)



# 许可证

```
Copyright [2022] [xlvchao]

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
```