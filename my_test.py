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
	'total': 16331.78,
	'available': 7945.26,
	'used': 8386.52,
	'free': 7945.26,
	'usage_percent': 51.4
}
'''

print(collector.swap())
'''
{
	'total': 18891.78,
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
		'total': 117.85,
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
	'io_in': 165775.09,
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
}, {
	'name': '本地连接* 6',
	'ip': '169.254.185.110',
	'io_in': 0.0,
	'io_out': 0.0
}, {
	'name': 'VMware Network Adapter VMnet1',
	'ip': '192.168.15.1',
	'io_in': 0.0,
	'io_out': 0.02
}, {
	'name': 'VMware Network Adapter VMnet8',
	'ip': '192.168.33.2',
	'io_in': 0.0,
	'io_out': 0.02
}, {
	'name': '以太网 3',
	'ip': '169.254.97.237',
	'io_in': 0.0,
	'io_out': 0.0
}, {
	'name': 'SSTAP 1',
	'ip': '10.198.75.60',
	'io_in': 0.0,
	'io_out': 0.0
}, {
	'name': 'SSTAP 1',
	'ip': '169.254.134.215',
	'io_in': 0.0,
	'io_out': 0.0
}]
'''