"""Prepare a fresh exercise session. No models, secrets or existing files changed."""
from pathlib import Path
import shutil
import tempfile
import sys
import shlex

HERE = Path(__file__).resolve().parent
session = Path(tempfile.mkdtemp(prefix='mlops-2026-exercise5-'))
for name in ['starter', 'controller']:
    shutil.copytree(HERE / name, session / ('service' if name == 'starter' else name))
shutil.copy2(HERE / 'requirements-target.txt', session / 'requirements-target.txt')
q = lambda name: shlex.quote(str(session / name))
commands = f"""MLOps Exercise 5 fresh session: {session}
Run these commands in order. Use Python 3.12 for both venvs.
python3.12 -m venv {q('venv-old')}
{q('venv-old/bin/python')} -m pip install -r {q('service/requirements.txt')}
python3.12 -m venv {q('venv-new')}
{q('venv-new/bin/python')} -m pip install -r {q('requirements-target.txt')}
Baseline before handing the service to the agent:
{shlex.quote(sys.executable)} {q('controller/verify.py')} {q('service')} {q('venv-old/bin/python')}
Open Canvas in this workspace: {session / 'service'}
Target interpreter: {session / 'venv-new/bin/python'}
Candidate check after migration:
REQUIRE_V2=1 {shlex.quote(sys.executable)} {q('controller/verify.py')} {q('service')} {q('venv-new/bin/python')}
No native Stop hook is automatically configured by this preparation script.
Read docs/workshops/mlops-2026/exercises/04-api-migration.md for the fresh-run prompt.
"""
(session / 'WORKSPACES.txt').write_text(commands)
print(commands)
