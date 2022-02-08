import os
import psutil
import datetime


class SysInfosCollector(object):

    platform = 'windows' if os.name=='nt' else 'linux'

    def cpu(self):
        '''
        CPU
        逻辑个数 = 物理个数 × 每个cpu的核数
        返回格式为json
        '''
        cpu_dict = {}
        cpu_dict.update({'platform': self.platform})
        cpu_dict.update({'physical_count': psutil.cpu_count(logical=False)})
        cpu_dict.update({'logical_count': psutil.cpu_count(logical=True)})
        cpu_dict.update({'usage_percent': psutil.cpu_percent(interval=1, percpu=False)})

        cpu_times_percent = psutil.cpu_times_percent(interval=1, percpu=False)
        cpu_dict.update({'user': cpu_times_percent.user})
        cpu_dict.update({'system': cpu_times_percent.system})
        cpu_dict.update({'idle': cpu_times_percent.idle})
        if self.platform=='windows':
            cpu_dict.update({'interrupt': cpu_times_percent.interrupt})
            cpu_dict.update({'dpc': cpu_times_percent.dpc})
        else:
            cpu_dict.update({'iowait': cpu_times_percent.iowait})
        cpu_dict.update({'boot_time': datetime.datetime.fromtimestamp(psutil.boot_time()).strftime("%Y-%m-%d %H:%M:%S")})
        return cpu_dict


    def memory(self):
        '''
        内存
        单位：MB
        返回格式为json
        '''
        mem_dict = {}
        mem_tuple = psutil.virtual_memory()

        mem_total = round(mem_tuple.total / 1024 / 1024, 2)
        mem_available = round(mem_tuple.available / 1024 / 1024, 2)
        mem_used = round(mem_tuple.used / 1024 / 1024, 2)
        mem_free = round(mem_tuple.free / 1024 / 1024, 2)
        mem_percent = mem_tuple.percent
        mem_dict.update({'total': mem_total, 'available': mem_available, 'used': mem_used, 'free': mem_free, 'usage_percent': mem_percent})
        return mem_dict

    def swap(self):
        '''
        内存
        单位：MB
        返回格式为json
        '''
        swap_dict = {}
        swap_tuple = psutil.swap_memory()

        swap_total = round(swap_tuple.total / 1024 / 1024, 2)
        swap_used = round(swap_tuple.used / 1024 / 1024, 2)
        swap_free = round(swap_tuple.free / 1024 / 1024, 2)
        swap_sin = round(swap_tuple.sin / 1024 / 1024, 2)
        swap_sout = round(swap_tuple.sout / 1024 / 1024, 2)
        swap_percent = swap_tuple.percent
        swap_dict.update({'total': swap_total, 'used': swap_used, 'free': swap_free, 'sin': swap_sin, 'sout': swap_sout, 'usage_percent': swap_percent})
        return swap_dict


    def disk(self):
        '''
        硬盘
        单位：GB
        返回格式为json
        '''
        disk_dict = {}
        partitions = psutil.disk_partitions()
        for p in partitions:
            usage_dict = {}
            usage_tuple = psutil.disk_usage(p.mountpoint)
            total = round(usage_tuple.total / 1024 / 1024 / 1024, 2)
            used = round(usage_tuple.used / 1024 / 1024 / 1024, 2)
            free = round(usage_tuple.free / 1024 / 1024 / 1024, 2)
            percent = usage_tuple.percent
            usage_dict.update({'total': total, 'used': used, 'free': free, 'usage_percent': percent})
            disk_dict.update({p.device: usage_dict})
        return disk_dict


    def net(self):
        ''' 获取开机以来 接收/发送 的流量
            单位：MB
            返回格式为json
        '''
        net_io_list = []
        info = psutil.net_if_addrs()
        for k, v in info.items():
            for item in v:
                if item.family == 2 and item.address != '127.0.0.1':
                    net_io_dict = {}
                    net_io_dict.setdefault('name', k)
                    net_io_dict.setdefault('ip', item.address)
                    bytes_recv = round(psutil.net_io_counters(pernic=True).get(k).bytes_recv / 1024 / 1024, 2)
                    bytes_sent = round(psutil.net_io_counters(pernic=True).get(k).bytes_sent / 1024 / 1024, 2)
                    net_io_dict.setdefault('io_in', bytes_recv)  # 各网卡接收的字节数
                    net_io_dict.setdefault('io_out', bytes_sent)  # 各网卡发送的字节数
                    net_io_list.append(net_io_dict)
        return net_io_list