#!/usr/bin/env python
"""
Generate class diagrams for Python applications using pyreverse.
Excludes test files, test classes, and migrations from the output.
"""

import argparse
import os
import subprocess
import sys
import tempfile
import shutil
from pathlib import Path


def find_python_files(app_path, exclude_tests=True, exclude_migrations=True):
    """
    Find all Python files in the given path.

    Args:
        app_path: Path to the application directory
        exclude_tests: Whether to exclude test files
        exclude_migrations: Whether to exclude migration files

    Returns:
        List of Python file paths
    """
    app_path = Path(app_path)
    python_files = []

    for py_file in app_path.rglob("*.py"):
        # Skip __pycache__ directories
        if "__pycache__" in str(py_file):
            continue

        # Skip test files if requested
        if exclude_tests:
            filename = py_file.name.lower()
            if filename.startswith("test_") or filename.startswith("tests_"):
                continue
            if filename == "test.py" or filename == "tests.py":
                continue
            if "test" in py_file.parent.name.lower():
                continue

        # Skip migration files if requested
        if exclude_migrations:
            # Check if file is in a migrations directory
            if "migrations" in [p.name for p in py_file.parents]:
                continue
            # Also check if parent directory is named 'migrations'
            if py_file.parent.name == "migrations":
                continue

        python_files.append(py_file)

    return python_files


def create_temp_structure(files, base_path):
    """
    Create a temporary directory structure with only non-test files.

    Args:
        files: List of file paths to include
        base_path: Base path of the original application

    Returns:
        Path to temporary directory
    """
    temp_dir = Path(tempfile.mkdtemp(prefix="pyreverse_"))
    base_path = Path(base_path).resolve()

    for file_path in files:
        file_path = Path(file_path).resolve()
        # Calculate relative path from base
        try:
            rel_path = file_path.relative_to(base_path)
        except ValueError:
            # If file is not relative to base, skip it
            continue

        # Create destination path
        dest_path = temp_dir / rel_path
        dest_path.parent.mkdir(parents=True, exist_ok=True)

        # Copy file
        shutil.copy2(file_path, dest_path)

    return temp_dir


def run_pyreverse(path, project_name, output_format, output_dir=None):
    """
    Run pyreverse to generate class diagrams.

    Args:
        path: Path to analyze
        project_name: Name for the project
        output_format: Output format (png, svg, puml, etc.)
        output_dir: Optional output directory

    Returns:
        Tuple of (success, message)
    """
    cmd = ["pyreverse", "-o", output_format, "-p", project_name]

    if output_dir:
        cmd.extend(["-d", output_dir])

    cmd.append(str(path))

    try:
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            check=True
        )
        return True, result.stdout
    except subprocess.CalledProcessError as e:
        return False, f"Error running pyreverse: {e.stderr}"
    except FileNotFoundError:
        return False, "pyreverse not found. Install it with: pip install pylint"


def main():
    parser = argparse.ArgumentParser(
        description="Generate class diagrams for Python applications, excluding tests and migrations.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s orders/
  %(prog)s orders/ -p my_orders -f svg
  %(prog)s orders/ -p orders -f puml -o diagrams/
  %(prog)s orders/ --include-tests --include-migrations
        """
    )

    parser.add_argument(
        "path",
        help="Path to the Python application/package to analyze"
    )

    parser.add_argument(
        "-p", "--project",
        default=None,
        help="Project name for the diagram (default: directory name)"
    )

    parser.add_argument(
        "-f", "--format",
        default="png",
        choices=["png", "svg", "puml", "dot", "vcg"],
        help="Output format (default: png)"
    )

    parser.add_argument(
        "-o", "--output",
        default=None,
        help="Output directory for generated diagrams (default: current directory)"
    )

    parser.add_argument(
        "--include-tests",
        action="store_true",
        help="Include test files and test classes in the diagram"
    )

    parser.add_argument(
        "--include-migrations",
        action="store_true",
        help="Include Django migration files in the diagram"
    )

    parser.add_argument(
        "--keep-temp",
        action="store_true",
        help="Keep temporary directory (for debugging)"
    )

    args = parser.parse_args()

    # Validate input path
    app_path = Path(args.path)
    if not app_path.exists():
        print(f"Error: Path '{args.path}' does not exist", file=sys.stderr)
        return 1

    if not app_path.is_dir():
        print(f"Error: Path '{args.path}' is not a directory", file=sys.stderr)
        return 1

    # Determine project name
    project_name = args.project or app_path.name

    # Create output directory if specified
    if args.output:
        output_dir = Path(args.output)
        output_dir.mkdir(parents=True, exist_ok=True)
    else:
        output_dir = Path.cwd()

    print(f"Analyzing: {app_path}")
    print(f"Project name: {project_name}")
    print(f"Output format: {args.format}")
    print(f"Output directory: {output_dir}")
    print(f"Exclude tests: {not args.include_tests}")
    print(f"Exclude migrations: {not args.include_migrations}")
    print()

    # If including everything, run pyreverse directly
    if args.include_tests and args.include_migrations:
        print("Running pyreverse on full application...")
        success, message = run_pyreverse(
            app_path,
            project_name,
            args.format,
            str(output_dir)
        )

        if success:
            print("✓ Diagrams generated successfully!")
            print(message)
            return 0
        else:
            print(f"✗ {message}", file=sys.stderr)
            return 1

    # Find Python files with exclusions
    exclusion_msg = []
    if not args.include_tests:
        exclusion_msg.append("tests")
    if not args.include_migrations:
        exclusion_msg.append("migrations")

    print(f"Finding Python files (excluding {', '.join(exclusion_msg)})...")
    python_files = find_python_files(
        app_path,
        exclude_tests=not args.include_tests,
        exclude_migrations=not args.include_migrations
    )

    if not python_files:
        print(f"Error: No Python files found (excluding {', '.join(exclusion_msg)})", file=sys.stderr)
        return 1

    print(f"Found {len(python_files)} Python files")

    # Create temporary structure
    print("Creating temporary directory structure...")
    temp_dir = None
    try:
        temp_dir = create_temp_structure(python_files, app_path)

        if args.keep_temp:
            print(f"Temporary directory: {temp_dir}")

        # Run pyreverse on temporary structure
        print("Running pyreverse...")
        success, message = run_pyreverse(
            temp_dir,
            project_name,
            args.format,
            str(output_dir)
        )

        if success:
            print("✓ Diagrams generated successfully!")
            print(message)

            # List generated files
            print("\nGenerated files:")
            for pattern in [f"classes_{project_name}.*", f"packages_{project_name}.*"]:
                for file in output_dir.glob(pattern):
                    print(f"  - {file}")

            return 0
        else:
            print(f"✗ {message}", file=sys.stderr)
            return 1

    finally:
        # Clean up temporary directory
        if temp_dir and temp_dir.exists() and not args.keep_temp:
            shutil.rmtree(temp_dir)
            print("\nTemporary directory cleaned up")


if __name__ == "__main__":
    sys.exit(main())
