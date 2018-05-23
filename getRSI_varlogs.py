from flask import Flask, request
from flask_restful import abort
from jnpr.junos import Device
from jnpr.junos.utils.start_shell import StartShell
from jnpr.junos.utils.scp import SCP
from jnpr.junos.utils.fs import FS
import json
import datetime
#import pdb; pdb.set_trace()

app = Flask(__name__)
date = datetime.datetime.now()

def get_rsi_varlogs(host):

    dev = Device(host, user='lab', passwd='lab')
    dev.open()

    fileSystem = FS(dev)
    fileSystem.tgz("/var/log/*","/var/tmp/pyez_varlog.tgz")

    ss = StartShell(dev)
    ss.open()

    ss.run('cli -c "request support information | save /var/tmp/rsi.txt"', timeout=600)
    with SCP(dev) as scp:
        scp.get("/var/tmp/rsi.txt", local_path="/var/log/pyez/pyez_rsi_"+dev.hostname+"_"+str(date.strftime('%Y%m%d_%H%M%S'))+".txt")
        scp.get("/var/tmp/pyez_varlog.tgz", local_path="/var/log/pyez/pyez_varlog_"+dev.hostname+"_"+str(date.strftime('%Y%m%d_%H%M%S'))+".tgz")

    dev.close()
    
@app.route('/', methods=['POST'])
def app_message_post():
    try:
        if request.headers['Content-Type'] != 'application/json':
            return json.dumps({'result': message})
        data = request.json
        status = data['status']
        if status['state'] == 'active':
            host = status['entityId']
            get_rsi_varlogs(host)
        return json.dumps({'result': message})
    except Exception as e:
        abort(400, message="Hit an issue when proessing message: {}"
                           .format(e))

if __name__ == '__main__':
    FLASK_PORT = 8000
    app.run(
        host="0.0.0.0",
        port=int(FLASK_PORT),
        debug=True
    )
