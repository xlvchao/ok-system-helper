from rediscluster import RedisCluster
import configparser
import pymysql
import datetime as dt
from datetime import datetime
from core.system_helper import SysInfosCollector
from apscheduler.schedulers.blocking import BlockingScheduler
import traceback
from utils.snowflake import Snow
import os
from utils.log_helper import LoggerFactory

# 获取配置
base_dir = os.path.dirname(os.path.abspath(__file__))
conf = configparser.ConfigParser()
conf.read(os.path.join(base_dir, 'config.conf'))

# application
application_name = conf.get("application", "name")
application_host = conf.get("application", "host")
application_port = conf.getint("application", "port")

# redis
redis_cluster_nodes = conf.get("redis", "redis_cluster_nodes")
redis_password = conf.get("redis", "password")

# mysql
mysql_host = conf.get("mysql", "host")
mysql_port = conf.getint("mysql", "port")
mysql_dbname = conf.get("mysql", "dbname")
mysql_username = conf.get("mysql", "username")
mysql_password = conf.get("mysql", "password")

logger = LoggerFactory().getLogger()
sys_infos_collector = SysInfosCollector()


def gen_redis_connection():
    '''
        获取一个redis cluster的connection
    '''
    startup_nodes = []
    for i in redis_cluster_nodes.split(','):
        node = {}
        node['host'] = i.split(':')[0]
        node['port'] = i.split(':')[1]
        startup_nodes.append(node)
    try:
        con = RedisCluster(startup_nodes=startup_nodes,
                            skip_full_coverage_check=True,
                            decode_responses=True, password=redis_password)
        logger.info('get redis connection success!')
        return con
    except:
        logger.error('get redis connection exeception!')
        traceback.print_exc()
        return


def refresh_ip_port_into_redis():
    '''
        刷新服务器的IP地址、端口号
    '''
    redis = gen_redis_connection()
    if not redis.hexists(name='monitor:server:hosts', key=application_host):
        redis.hset(name='monitor:server:hosts', key=application_host, value=application_port)
    logger.info('refresh_ip_port_into_redis refresh completed!')


def refresh_netio_count_into_redis():
    '''
        统计网卡正点时刻的累计流量
    '''
    redis = gen_redis_connection()
    net_io_dict = sys_infos_collector.net()
    io_in = float(net_io_dict.get('io_in'))
    io_out = float(net_io_dict.get('io_out'))

    # 插入当前正点的键值对
    prefix_hour = datetime.now().replace(minute=0, second=0, microsecond=0)
    prefix = prefix_hour.strftime("%Y-%m-%d %H:%M:%S")
    redis.set((application_host + '_' + prefix + '_io_in').replace('.', '_').replace(' ', '_'), io_in)
    redis.set((application_host + '_' + prefix + '_io_out').replace('.', '_').replace(' ', '_'), io_out)
    logger.info('refresh_netio_count_into_redis refresh completed!')

    # 删除上一正点的键值对
    prefix_hour = datetime.now().replace(minute=0, second=0, microsecond=0) + dt.timedelta(hours=-1)
    prefix = prefix_hour.strftime("%Y-%m-%d %H:%M:%S")
    redis.delete((application_host + '_' + prefix + '_io_in').replace('.', '_').replace(' ', '_'))
    redis.delete((application_host + '_' + prefix + '_io_out').replace('.', '_').replace(' ', '_'))
    logger.info('refresh_netio_count_into_redis delete completed!')


def refresh_netio_count_into_database():
    '''
        分时段统计网卡流量，比如00:00点~01:00点，网卡出网流量100MB、入网流量100MB
    '''
    # 获取当前正点时间、网卡累计流量
    next_hour = datetime.now().replace(minute=0, second=0, microsecond=0) + dt.timedelta(hours=1)
    count_hour = next_hour.strftime("%Y-%m-%d %H:%M:%S")

    net_io_list = sys_infos_collector.net()
    current_io_in = float(0)
    current_io_out = float(0)
    for net_io in net_io_list:
        current_io_in += float(net_io.get('io_in'))
        current_io_out += float(net_io.get('io_out'))

    # 获取上一正点时间、网卡累计流量
    redis = gen_redis_connection()
    prefix_hour = datetime.now().replace(minute=0, second=0, microsecond=0)
    prefix = prefix_hour.strftime("%Y-%m-%d %H:%M:%S")
    redis_io_in = 0
    redis_io_out = 0

    io_in_key = (application_host + '_' + prefix + '_io_in').replace('.', '_').replace(' ', '_')
    if redis.exists(io_in_key):
        redis_io_in = float(redis.get(io_in_key))
    io_out_key = (application_host + '_' + prefix + '_io_out').replace('.', '_').replace(' ', '_')
    if redis.exists(io_out_key):
        redis_io_out = float(redis.get(io_out_key))

    conn = pymysql.connect(host=mysql_host, port=mysql_port, user=mysql_username, passwd=mysql_password, db=mysql_dbname, charset="utf8")
    cursor = conn.cursor()
    try:
        sql = "select * from tb_net_io where insert_date=%s and ip=%s"
        params = (count_hour, application_host)
        count = cursor.execute(sql, params)
        conn.commit()

        if count == 1:
            sql = "update tb_net_io set io_in=%s, io_out=%s where insert_date=%s and ip=%s"
            params = (current_io_in - redis_io_in, current_io_out - redis_io_out, count_hour, application_host)
            count = cursor.execute(sql, params)
            conn.commit()
        else:
            id = Snow().get()
            sql = "insert into tb_net_io(id,insert_date,io_in,io_out,ip) values(%s,%s,%s,%s,%s)"
            params = (id, count_hour, current_io_in - redis_io_in, current_io_out - redis_io_out, application_host)
            count = cursor.execute(sql, params)
            conn.commit()
    except:
        logger.error('refresh_netio_count_into_database refresh exeception!')
        conn.rollback()
        traceback.print_exc()
        return
    else:
        logger.info('refresh_netio_count_into_database refresh completed!')
    finally:
        cursor.close()
        conn.close()


if __name__ == "__main__":
    logger.info('ok-system-helper scheduled_task starting...')

    # 先干一下子再说
    refresh_ip_port_into_redis()

    # 生成一个BlockingScheduler调度器，使用默认的任务存储MemoryJobStore、默认的执行器ThreadPoolExecutor，且最大线程数为10
    scheduler = BlockingScheduler()
    scheduler.add_job(refresh_ip_port_into_redis, 'cron', hour='0-23', id='refresh_ip_port_into_redis')
    scheduler.add_job(refresh_netio_count_into_redis, 'cron', hour='0-23', id='refresh_netio_count_into_redis')
    scheduler.add_job(refresh_netio_count_into_database, 'cron', minute='0-59', id='refresh_netio_count_into_database')
    scheduler.start()
