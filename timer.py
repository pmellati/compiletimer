#!/usr/bin/env python3

from subprocess import run
import subprocess
import argparse
import re
import asyncio
import os

# SEE: https://stackoverflow.com/questions/375427/non-blocking-read-on-a-subprocess-pipe-in-python/437888

def escape_ansi(line):
    ansi_escape = re.compile(r'(\x9B|\x1B\[)[0-?]*[ -/]*[@-~]')
    return ansi_escape.sub('', line)

parser = argparse.ArgumentParser()
parser.add_argument("project_root", help="project_root scala project root")
args = parser.parse_args()

project_root = args.project_root

scala_files = list(filter(
    lambda l: l != '',
    run(['git', 'ls-files', '*.scala'], cwd = project_root, stdout = subprocess.PIPE)
        .stdout.decode('UTF-8').split('\n')
))

print('Scala files\n' + str(len(scala_files)))

class SubprocessProtocol(asyncio.SubprocessProtocol):
    def pipe_data_received(self, fd, data):
        if fd == 1: # got stdout data (bytes)
            print('GOT STDOUT:')
            print(escape_ansi(data.decode()))

    def connection_lost(self, exc):
        loop.stop() # end loop.run_forever()

if os.name == 'nt':
    loop = asyncio.ProactorEventLoop() # for subprocess' pipes on Windows
    asyncio.set_event_loop(loop)
else:
    loop = asyncio.get_event_loop()
try:
    loop.run_until_complete(loop.subprocess_exec(SubprocessProtocol, 'sbt', cwd = project_root))
    loop.run_forever()
finally:
    loop.close()
