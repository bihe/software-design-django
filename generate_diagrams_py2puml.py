#!/usr/bin/env python
"""
Generate UML class diagrams for Django models using py2puml.
This script properly initializes Django before running py2puml.

Usage:
    python generate_diagrams.py <app_name> [output_file]

Examples:
    python generate_diagrams.py customers
    python generate_diagrams.py customers customers_diagram.puml
    python generate_diagrams.py products products.puml
"""
import os
import sys
import django
from pathlib import Path

# Set up Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'swd_django_demo.settings')
django.setup()

# Now import py2puml after Django is set up
from py2puml.py2puml import py2puml


def main():
    if len(sys.argv) < 2:
        print("Usage: python generate_diagrams.py <app_name> [output_file]")
        print("\nExamples:")
        print("  python generate_diagrams.py customers")
        print("  python generate_diagrams.py customers customers_diagram.puml")
        sys.exit(1)

    app_name = sys.argv[1]
    output_file = sys.argv[2] if len(sys.argv) > 2 else f"{app_name}_diagram.puml"

    # Get the path to the app directory
    app_path = str(Path.cwd() / app_name)

    # Check if the app directory exists
    if not Path(app_path).exists():
        print(f"Error: App directory '{app_name}' not found in current directory")
        sys.exit(1)

    # Generate the PlantUML diagram
    print(f"Generating class diagram for {app_name}...")
    try:
        puml_content = py2puml(app_path, app_name)

        # Write to file
        with open(output_file, 'w') as f:
            f.write(''.join(puml_content))

        print(f"Class diagram generated successfully: {output_file}")
        print(f"\nYou can view it at: http://www.plantuml.com/plantuml/uml/")
        print(f"Or convert to image with: plantuml {output_file}")

    except Exception as e:
        print(f"Error generating diagram: {e}")
        sys.exit(1)


if __name__ == '__main__':
    main()
