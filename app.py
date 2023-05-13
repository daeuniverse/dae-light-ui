# coding=utf8
from flask import Flask, render_template, request, jsonify
import subprocess
import psutil
import datetime
import time
import socket
app = Flask(__name__,template_folder='templates')

#打印日志
@app.route('/journal')
def journal():
    command = 'journalctl -xu dae -n 250 --reverse'
    output = subprocess.check_output(command.split()).decode('utf-8')
    return render_template('journal.html', output=output)

# 启动dae服务
def start_dae():
    subprocess.call(['systemctl', 'start', 'dae'])

# 停止dae服务
def stop_dae():
    subprocess.call(['systemctl', 'stop', 'dae'])

# 重载dae服务

# 读取主题文件
def read_select():
    with open('/root/dae-ui/theme', 'r') as f:
        select = f.readline()
    return select

# 写入主题文件
def write_select(select):
    with open('/root/dae-ui/theme', 'w') as f:
        f.write(select)

# 读取配置文件
def read_config():
    with open('/usr/local/etc/dae/config.dae', 'r') as f:
        config = f.read()
    return config

# 写入配置文件
def write_config(config):
    with open('/usr/local/etc/dae/config.dae', 'w') as f:
        f.write(config)		

# 启动dae服务
def start_dae():
    # 使用subprocess模块调用systemctl命令
    cmd = '/usr/bin/systemctl start dae.service'
    result = subprocess.run(cmd.split(), capture_output=True)

    #  打印输出结果和错误信息
    print(result.stdout.decode('utf-8'))
    print(result.stderr.decode('utf-8'))

# 停止dae服务
def stop_dae():
    # 使用subprocess模块调用systemctl命令
    cmd = '/usr/bin/systemctl stop dae.service'
    result = subprocess.run(cmd.split(), capture_output=True)

    #  打印输出结果和错误信息
    print(result.stdout.decode('utf-8'))
    print(result.stderr.decode('utf-8'))
# 重载dae服务
def reload_dae():
    subprocess.call(['systemctl', 'reload', 'dae.service'])

# 重启dae服务
def restart_dae():
    subprocess.call(['/usr/bin/systemctl', 'restart', 'dae.service'])

# 获取dae运行时长
def get_dae_runtime():
    process_path = 'dae'
    for proc in psutil.process_iter(['pid', 'create_time', 'name']):
        if proc.name() == process_path:
            create_time = datetime.datetime.fromtimestamp(proc.create_time())
            uptime = datetime.datetime.now() - create_time
            days = uptime.days
            hours, remainder = divmod(uptime.seconds, 3600)
            minutes, seconds = divmod(remainder, 60)
            #return uptime_days, uptime_hours, uptime_minutes, uptime_seconds
            return [f"{days}天{hours}小时{minutes}分钟{seconds}秒","stop","green"]
    return ["dae未启动!","start","red"]

# 更新geo文件
def updateGeo():
    # 运行shell脚本
    subprocess.run(['chmod', '+x', '/root/dae-ui/install-dat-release.sh'])
    subprocess.call(['/root/dae-ui/install-dat-release.sh'])
    reload_dae()

# 主页
@app.route('/', methods=['GET', 'POST'])
def index():
    # 获取配置文件内容
    config = read_config()
    select = read_select()
    if request.method == 'POST':
        # 获取表单数据
        action = request.form['action']
        config = request.form['config']
        select = request.form['select']
        if action == 'Save':
            # 写入配置文件
            write_config(config)
			# 重载dae服务
            reload_dae()
        elif action == 'Start':
            # 启动dae服务
            start_dae()
        elif action == 'Stop':
            # 停止dae服务
            stop_dae()
        elif action == 'Reload':
            # 重载dae服务
            reload_dae()
        elif action == 'Restart':
            # 重启dae服务
            restart_dae()
        elif action == '保存主题':
           # 写入主题文件
            write_select(select)
        elif action == '更新geo文件':
           # 更新geo文件
            updateGeo()

        # 重新读取配置文件
        config = read_config()
        select = read_select()
    return render_template('index.html', config=config,select=select,runtime=get_dae_runtime())

if __name__ == '__main__':
    app.run(host='0.0.0.0',port='5000')