<#
.SYNOPSIS
The powershell 'cli.ps1' scipt provides the most-often used commands for this application in a convenient was.

.DESCRIPTION
USAGE
    .\cli.ps1 <command>

COMMANDS
    migrate             📜 Executing database migrations...
    adminuser           🤖 Create a admin-user via django...
    requirements.txt    📦 Create requirements.txt to use with pip
    test                🧪 Executing unit-tests...
    runserver           🚀 Starting Django development server...
    compose             🚀 Starting containers with docker compose...
    docker-simple       🚀 Start one docker container...
    help, -?            show this help message
#>
param(
  [Parameter(Position=0)]
  [ValidateSet("migrate", "adminuser", "requirements.txt", "test", "runserver", "compose", "docker-simple", "help")]
  [string]$Command
)

function Command-Help { Get-Help $PSCommandPath }

function Command-migrate {
    Write-Host -ForegroundColor Green "📜 Executing database migrations..."
    uv run python manage.py migrate
}

function Command-adminuser {
    Write-Host -ForegroundColor Green "🤖 Create a admin-user via django..."
    uv run python manage.py createsuperuser
}

function Command-requirements {
    Write-Host -ForegroundColor Green "📦 Create requirements.txt ..."
    uv pip freeze > requirements.txt
}

function Command-test {
    Write-Host -ForegroundColor Green "🧪 Executing tests..."
    uv run python manage.py test -v 2
}

function Command-runserver {
    Write-Host -ForegroundColor Green "🚀 Starting Django webserver..."
    uv run python manage.py runserver
}

function Command-compose {
    Write-Host -ForegroundColor Green "🚀 Prepare static files for serving..."
    If (Test-Path ./static_dir) { Remove-Item -force -recurse ./static_dir }
    
    python manage.py collectstatic -c

    Write-Host -ForegroundColor Green "🚀 Starting containers with docker compose..."
    docker compose -f ./containers/compose.yaml rm && docker compose -f ./containers/compose.yaml up --build 
}

function Command-docker-simple {
    Write-Host -ForegroundColor Green "🚀 Docker build and run..."
    docker build -t django-simple -f ./containers/simple/Dockerfile .
    docker run -it -p 8000:8000 django-simple
}   


if (!$Command) {
    Command-Help
    exit
}

switch ($Command) {
    "migrate" { Command-migrate }
    "adminuser" { Command-adminuser }
    "requirements.txt" { Command-requirements }
    "test" { Command-test }
    "runserver" { Command-runserver }
    "compose" { Command-compose }
    "docker-simple" { Command-docker-simple }
    "help"  { Command-Help }
}
