<#
.SYNOPSIS
The powershell 'cli.ps1' scipt provides the most-often used commands for this application in a convenient was.

.DESCRIPTION
USAGE
    .\cli.ps1 <command>

COMMANDS
    migrate             📜 Executing database migrations...
    test                🧪 Executing unit-tests...
    runserver           🚀 Starting Django development server..
    help, -?            show this help message
#>
param(
  [Parameter(Position=0)]
  [ValidateSet("migrate", "test", "runserver", "help")]
  [string]$Command
)

function Command-Help { Get-Help $PSCommandPath }

function Command-migrate {
    Write-Host -ForegroundColor Green "📜 Executing database migrations..."
    uv run python manage.py migrate
}

function Command-test {
    Write-Host -ForegroundColor Green "🧪 Executing tests..."
    uv run python manage.py test -v 2
}

function Command-runserver {
    Write-Host -ForegroundColor Green "🚀 Starting Django webserver..."
    uv run python manage.py runserver
}


if (!$Command) {
    Command-Help
    exit
}

switch ($Command) {
    "migrate" { Command-migrate }
    "test" { Command-test }
    "runserver" { Command-runserver }
    "help"  { Command-Help }
}
