import os
import subprocess
import sys
from pathlib import Path

repo_dir = Path(r"D:/My data/Applying/AIML PREPARATION/AI AGENT PROJECTS/POWERED AI DETECTION AND HUMANIZED CONTENT 2")
remote_url = "https://github.com/VARADHARAJAN4/AI_Powered_Data_Content_Processing--Stage1-AI_Detector_Agent.git"

print('Working directory:', repo_dir)
if not repo_dir.exists():
    print('ERROR: repo directory does not exist')
    sys.exit(1)

os.chdir(repo_dir)

def run(cmd, **kwargs):
    print('->', ' '.join(cmd))
    r = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, **kwargs)
    print('STDOUT:\n', r.stdout)
    print('STDERR:\n', r.stderr)
    return r

# check git
r = run(['git', '--version'])
if r.returncode != 0:
    print('git not found; please install git and retry')
    sys.exit(1)

# init repo if needed
if not (repo_dir / '.git').exists():
    print('Initializing new git repo...')
    r = run(['git', 'init'])
    if r.returncode != 0:
        print('git init failed')
        sys.exit(1)
else:
    print('.git exists; skipping init')

# add all
r = run(['git', 'add', '.'])
# commit (allow empty commit if nothing to commit)
r = run(['git', 'commit', '-m', 'Initial commit: AI Humanizer Agent'], input=None)

# remove remote if exists
run(['git', 'remote', 'remove', 'origin'])
# add remote
r = run(['git', 'remote', 'add', 'origin', remote_url])
if r.returncode != 0:
    print('Failed to add remote; aborting')
    sys.exit(1)

# set branch main
run(['git', 'branch', '-M', 'main'])

# attempt push with no terminal prompt
env = os.environ.copy()
env['GIT_TERMINAL_PROMPT'] = '0'
print('Pushing to remote (non-interactive). If this fails due to authentication, set up SSH or a PAT and try manually.')
r = subprocess.run(['git', 'push', '-u', 'origin', 'main'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, env=env)
print('PUSH STDOUT:\n', r.stdout)
print('PUSH STDERR:\n', r.stderr)
if r.returncode != 0:
    print('\nPush failed (likely authentication required).\n')
    print('To push manually:')
    print('1) Configure your Git credentials (PAT or SSH).')
    print("2) Then run these commands in PowerShell:\n")
    print('   cd "', str(repo_dir), '"')
    print('   git add .')
    print("   git commit -m \"Initial commit: AI Humanizer Agent\"")
    print('   git remote add origin ', remote_url)
    print('   git branch -M main')
    print('   git push -u origin main')
    sys.exit(1)

print('Push completed successfully')
