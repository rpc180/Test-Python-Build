Install base code platform
winget install --id Microsoft.VisualStudioCode --source winget
winget install --id Python.Python.3.13 --source winget
winget install --id Microsoft.PowerShell --source winget
winget install --id Git.Git --source winget
winget install --id GitHub.cli --source winget
winget install --id Microsoft.AzureCLI --source winget

Validate installations using a NEW terminal session
winget --version
code --version
python --version
py --version
pwsh --version
git --version
gh --version

VSCode Extensions (use profile from C:\support of Lenovo notebook)
Update Theme to VSCode Dark
Python (ms-python.python) for language support, debugging, formatting hooks, testing, and environment integration.
Pylance (ms-python.vscode-pylance) for better IntelliSense and type-aware editing.
PowerShell (ms-vscode.PowerShell) for script editing, integrated console support, and debugging.
Jupyter (ms-toolsai.jupyter) only if you truly want notebooks in VS Code. It requires a Python environment with Jupyter installed.
GitHub Pull Requests and Issues if you want PR workflows in VS Code.

You can install them inside VS Code from Extensions (Ctrl+Shift+X) or from the Marketplace pages above. Microsoft also supports using Profiles in VS Code, which is useful if you want one profile for Python/PowerShell dev and another for other work. https://code.visualstudio.com/docs/configure/profiles?utm_source=chatgpt.com

First-run VS Code setup

For portability, use mostly workspace settings rather than too many global user settings. VS Code stores workspace settings in .vscode/settings.json, and workspace settings override user settings for that project.

A good starter .vscode/settings.json for Python + PowerShell projects is:

{
"python.terminal.activateEnvironment": true,
"python.terminal.useEnvFile": true,
"files.trimTrailingWhitespace": true,
"files.insertFinalNewline": true,
"editor.formatOnSave": true,
"[powershell]": {
"editor.defaultFormatter": "ms-vscode.powershell"
}
}

That keeps project behavior consistent when the repo moves to another machine.

Establish AZ login:
Then open a new PowerShell window and run:

az login

If you have access to multiple tenants or subscriptions, also check which account you landed in:

az account show
az account list --output table

If needed, set the right subscription:

az account set --subscription "<your subscription name or id>"

Python setup pattern

The portable pattern is:

install base Python once
create a .venv inside each Python project
install project-specific packages into that .venv
commit a dependency manifest, not the .venv itself

Python’s docs explicitly describe venv as a lightweight isolated environment created from an existing Python installation, and the packaging guide describes using venv, pip, and requirements files together. The Python tutorial also notes that .venv is a common directory name.

Inside a Python project:

py -m venv .venv
.\.venv\Scripts\Activate
python -m pip install --upgrade pip
pip install azure-ai-projects azure-identity python-dotenv
pip freeze > requirements.txt

Then in VS Code, use Python: Select Interpreter and choose .venv\Scripts\python.exe. VS Code’s Python docs cover using Python environments and debugging from the editor.

?? When I clone the repo down - what do I have to run if there is a requirements.txt - does that effectively re-create the .venv contents?

PowerShell setup pattern

For PowerShell, I’d develop primarily in PowerShell 7 (pwsh) but keep Windows PowerShell 5.1 around for compatibility checks, since Microsoft states they install side-by-side.

Useful first checks:

pwsh
$PSVersionTable
Get-ExecutionPolicy -List

Execution policy on Windows controls when scripts can run; Microsoft describes it as a safety feature, not a security boundary. For a personal dev VM, many people set the current user scope to RemoteSigned, which avoids changing machine-wide policy.

Example:
Set-ExecutionPolicy -Scope CurrentUser RemoteSigned

Git and GitHub setup

Configure Git once on the VM:

git config --global user.name "Your Name"
git config --global user.email "you@example.com"
git config --global core.autocrlf true

GitHub documents line-ending handling on Windows, and this setting is the common fix for mixed Windows/Linux repos.

Then authenticate GitHub CLI:

gh auth login

GitHub’s quickstart uses that as the standard first step after installing gh.

Recommended GitHub file structure

Since your repo may contain multiple unrelated experiments, use one top-level “lab” repo and keep each project self-contained. That works well for mixed Python and PowerShell code, and GitHub handles mixed-language repositories fine because Git is content-based rather than language-specific.

foundry-agent-test/
├── .gitignore
├── .env.example
├── README.md
├── requirements.txt
├── .vscode/
│ ├── settings.json
│ └── launch.json
├── src/
│ └── foundry_agent_chat.py
└── tests/

tinker/
├── .gitignore
├── README.md
├── foundry-agent-test/
│ ├── .env.example
│ ├── .gitignore
│ ├── README.md
│ ├── requirements.txt
│ ├── .vscode/
│ │ ├── settings.json
│ │ └── launch.json
│ ├── src/
│ │ └── foundry_agent_chat.py
│ └── tests/
├── powershell-lab/
│ ├── README.md
│ ├── .vscode/
│ │ └── settings.json
│ ├── scripts/
│ │ └── test-script.ps1
│ └── modules/
└── snippets/
└── useful-gists-reference.md

A few rules make this portable:

put .venv inside each Python project, but never commit it
put .env in the project root, not inside .venv
commit .env.example, not the real .env
keep project dependencies in requirements.txt or pyproject.toml
put project-specific VS Code settings in .vscode/settings.json

Stand-alone Repo Root-level files matter more

The repo root should now contain the files that define and document the whole project:

.gitignore
.env.example
README.md
requirements.txt
optionally pyproject.toml later if you modernize the packaging

GitHub recommends a repo .gitignore to exclude files you do not want committed.

Root .gitignore template

At the repo root:

# Python

**/.venv/
**/**pycache**/
\*.pyc
.env

# VS Code

.vscode/

# PowerShell logs / temp

_.ps1xml
_.clixml

# OS

Thumbs.db
.DS_Store

If you want to share .vscode/settings.json, remove .vscode/ from the ignore list and instead ignore only user-specific files. The key idea is still the same: keep generated environments and secrets out of Git.

Standalone Revised .gitignore

For this standalone repo, I would use:

# Python virtual environment

.venv/

# Python cache / build artifacts

**pycache**/
_.pyc
_.pyo
\*.pyd

# Environment variables / secrets

.env

# VS Code local files

.vscode/

# OS files

Thumbs.db
.DS_Store

If later you want to commit shared VS Code settings for the repo, you can stop ignoring all of .vscode/ and instead ignore only user-specific files. But for now, keeping .vscode/ ignored is fine if you want the repo cleaner.

Standalone Revised .env pattern

This stays basically the same, but it now lives directly in the repo root.

.env.example
AZURE_AI_PROJECT_ENDPOINT=
AZURE_AI_AGENT_NAME=

.env
AZURE_AI_PROJECT_ENDPOINT=https://url.services.ai.azure.com/api/projects/whatever_site_name
AZURE_AI_AGENT_NAME=NameOfAgent

The real .env stays out of Git. The .env.example shows the structure without exposing values.

.env and secrets pattern

For a Foundry agent test app, use:

.env.example

AZURE_AI_PROJECT_ENDPOINT=
AZURE_AI_AGENT_NAME=

.env

AZURE_AI_PROJECT_ENDPOINT=https://your-resource.services.ai.azure.com/api/projects/your-project
AZURE_AI_AGENT_NAME=Dining_Agent

This minimizes rewrites when moving between machines: recreate .venv, copy .env.example to .env, fill in secrets or endpoints, and run. That is much more portable than hardcoding values in source.

Foundry agent test project template

For your first Python project on this VM, I’d make the folder like this:

foundry-agent-test/
├── .env.example
├── README.md
├── requirements.txt
├── src/
│ └── foundry_agent_chat.py
└── .vscode/
├── settings.json
└── launch.json

requirements.txt:

azure-ai-projects
azure-identity
python-dotenv

.vscode/launch.json:

{
"version": "0.2.0",
"configurations": [
{
"name": "Run Foundry Agent Test",
"type": "debugpy",
"request": "launch",
"program": "${workspaceFolder}/src/foundry_agent_chat.py",
"console": "integratedTerminal"
}
]
}

VS Code’s Python debugging docs cover this workflow, and workspace-level files make the project easier to reopen elsewhere with minimal setup.

Revised setup flow for a standalone repo

Once you create and clone the repo, the flow becomes:

cd foundry-agent-test
py -m venv .venv
.\.venv\Scripts\Activate
python -m pip install --upgrade pip
pip install azure-ai-projects azure-identity python-dotenv
pip freeze > requirements.txt

Then create .env from .env.example, select the interpreter in VS Code, and run the app.

foundry-agent-test/
├── .gitignore
├── .env.example
├── README.md
├── requirements.txt
├── requirements-lock.txt
├── src/
│ └── foundry_agent_chat.py
└── .vscode/
├── settings.json
└── launch.json

Keeping settings.json so that cloning to other machines is easier since I'm the only developer:
✅ What I recommend for your setup

Instead of ignoring the whole .vscode/ folder, track only specific files:

.gitignore

# Python

.venv/
**pycache**/
\*.pyc

# Secrets

.env

# Ignore all VS Code files by default...

.vscode/\*

# ...but allow specific shared config files

!.vscode/settings.json
!.vscode/launch.json
!.vscode/extensions.json

👉 This is the best-practice pattern

📁 What each file does (and why you want it)
✅ .vscode/settings.json

Keep this — it ensures consistency across machines.

Example (tailored to your setup):

{
"python.defaultInterpreterPath": "${workspaceFolder}\\.venv\\Scripts\\python.exe",
"python.terminal.activateEnvironment": true,
"editor.formatOnSave": true,
"files.trimTrailingWhitespace": true
}

💡 Benefit:

Every machine automatically picks the correct .venv
No reconfiguring VS Code every time

✅ .vscode/launch.json

Keep this — makes running/debugging identical everywhere.

Example:

{
"version": "0.2.0",
"configurations": [
{
"name": "Run Foundry Agent Test",
"type": "debugpy",
"request": "launch",
"program": "${workspaceFolder}/src/foundry_agent_chat.py",
"console": "integratedTerminal"
}
]
}

💡 Benefit:

Same debug/run behavior on every machine

✅ .vscode/extensions.json (optional but nice)
{
"recommendations": [
"ms-python.python",
"ms-python.vscode-pylance",
"ms-vscode.powershell"
]
}

💡 Benefit:

VS Code will prompt you to install required extensions automatically

To bring to another computer:

On my laptop, when I want to clone and work on it there, I would do the following:
open vscode on my laptop, connect use source control to clone the repository locally.
Then:
cd to the local folder destination and type the following:
py -m venv .venv
.\.venv\Scripts\Activate
python -m pip install --upgrade pip
pip install -r requirements.txt
pip install azure-ai-projects azure-identity python-dotenv

Then create copy .env.example .env
Select the interpreter in VS Code <SELECT FILE> folder destination\.venv\Scripts\python.exe

It should work the same then?
