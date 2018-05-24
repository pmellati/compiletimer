from subprocess import run
import subprocess
import argparse
import re

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

sbt = subprocess.Popen(['sbt'], cwd = project_root, stdin = subprocess.PIPE, stdout = subprocess.PIPE)

line = escape_ansi(sbt.stdout.readline().decode())

print('SBT LINES:\n' + line[0:6])
print(len(line))
