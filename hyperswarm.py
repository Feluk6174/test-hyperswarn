import subprocess
import json
import os


class HyperswarmInterface:
    def __init__(self, node_path='index.js', cwd=None):
        self.node_path = node_path
        self.cwd = cwd or os.getcwd()
        self.proc = subprocess.Popen(
            ['node', node_path],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            bufsize=1,
            cwd=self.cwd
        )

    def create(self, topic):
        self._send({'cmd': 'create', 'topic': topic})
        return self._recv()

    def send(self, msg):
        self._send({'cmd': 'send', 'msg': msg})
        return self._recv()

    def recv(self):
        self._send({'cmd': 'recv'})
        return self._recv()['msg']

    def nrecv(self):
        self._send({'cmd': 'nrecv'})
        return self._recv()['msg']

    def close(self):
        self.proc.stdin.close()
        self.proc.wait()

    def _send(self, obj):
        self.proc.stdin.write(json.dumps(obj) + '\n')
        self.proc.stdin.flush()

    def _recv(self):
        return json.loads(self.proc.stdout.readline())