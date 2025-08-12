# Software Design Python - Django Demo
The project can be used as a reference for the SWD lab course and shows an `example` python project using Django as the web-development framework.

This project consists of several apps with a focus on loose coupling and dependency injection.
A good article about separation of concerns in Django projects can be found `https://emcarrio.medium.com/business-logic-in-a-django-project-a25abc64718c`.
Good Django tutorials can be found `https://www.djangoproject.com/start/` or `https://cs50.harvard.edu/web/2020/weeks/3/`.

## 1. Requirements

### Shell for CLI workflow
Software development needs to interact with the system. Therefor we will encounter an number of CLI (command line interface) tools. To do this effectively we need to use a shell.

In a **Unix-like environments** like Mac/Linux typically a good shell is available out of the box (bash, zsh) in combination with a terminal (terminal, iTerm, Konsole, gnome-terminal, ...). 

For **Windows** a good combination of shell/terminal is [PowerShell](https://github.com/PowerShell/PowerShell)/[Windows Terminal](https://learn.microsoft.com/en-us/windows/terminal/). 

> [!TIP]
>**Powershell**: For windows users it is quite helpful to set the execution-policy for powershell:
>
>```bash
>Set-ExecutionPolicy RemoteSigned -Scope CurrentUser
>```

> [!TIP]
> **Windows NOTE**:  When you want to execute python in a `shell` and the Windows App-Store opens, you need to deactivate this Windows-Behavior: https://stackoverflow.com/questions/58754860/cmd-opens-windows-store-when-i-type-python

### Python
What is python?

> [!NOTE]
> Python is an interpreted, object-oriented, high-level programming language with dynamic semantics. (https://www.python.org/doc/essays/blurb/)

For this example the most recent python version is used https://peps.python.org/pep-0719/

- `python 3.13.x` 

To install python itself and as a python package manager we are using the tool [uv - 'An extremely fast Python package and project manager, written in Rust.'](https://docs.astral.sh/uv/)

- **uv install**: Easy via shell/cli: https://docs.astral.sh/uv/getting-started/installation/
- **uv/python version:** It can be used to install the needed python version quite easily: https://docs.astral.sh/uv/concepts/python-versions/


## 2. Development
Best practice for any python development is to start with a virtual environment. This approach and workflow is already integrated into [uv - Project Environment](https://docs.astral.sh/uv/concepts/projects/layout/#the-project-environment)

> [!NOTE]
> You benefit from the virtual environment since packages can be installed confidently and will not interfere with another project’s environment.

### Usage

1. Install dependencies with the projects main directory: `uv sync`.
2. Activate the virtual environment: `source .venv/bin/activate` / `./.venv/bin/activate.ps1`
3. Create the database tables: `uv run python manage.py migrate`
4. Create an admin user: `uv run python manage.py createsuperuser`
5. Run unit tests: `uv run python manage.py test -v 2`
6. Run the development server: `uv run python manage.py runserver`.
7. Open the website in your browser: `http://localhost:8000/admin`, `http://localhost:8000/products`.

Or if you want to start with a fresh Django project from scratch:

1. Initialize a new project: `uv init --python 3.13`.
2. Add Django: `uv add Django`
3. Install dependencies with the projects main directory: `uv sync`.
4. Activate the virtual environment: `source .venv/bin/activate` / `./.venv/bin/activate.ps1`
5. Create a new Django project: `uv run django-admin startproject django_project .`
6. Add Django applications: `uv run manage.py startapp app_name`

> [!TIP]
>**Windows**: A realtime virus scanning engine like [Windows Defender](https://www.microsoft.com/en-us/windows/comprehensive-security?r=1) sometimes gets in the way during development. As a result common development actions (compilation, execution of scripts, ..) take ages. To speed up the process it can make sense to disable realtime-scanning during compilation or exclude paths in the scan engine (be aware that this has a security impact!)
>
>- [Deactivate Real-Time Scanning](https://support.microsoft.com/en-us/windows/turn-off-defender-antivirus-protection-in-windows-security-99e6004f-c54c-8509-773c-a4d776b77960)
>- [Exclude Folder for Scanning](https://support.microsoft.com/en-us/windows/add-an-exclusion-to-windows-security-811816c0-4dfd-af4a-47e4-c301afe13b26)

### IDE
There are a number of IDEs available for python development. You can choose between different variants like [VSCode](https://code.visualstudio.com/), [PyCharm](https://www.jetbrains.com/pycharm/), [VIM](https://realpython.com/vim-and-python-a-match-made-in-heaven/), ...

### Dependency Injection
This project uses the python dependency injection module, which is not part of Django itself.
`https://python-dependency-injector.ets-labs.org/examples/django.html`



