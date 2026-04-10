"""src/syllabus_generator/cli.py.

Command-line interface for syllabus generation.
"""

import argparse
from pathlib import Path
import sys

from syllabus_generator.constants import COURSES_DIR, DEFAULT_TEMPLATE_PATH
from syllabus_generator.generator import generate_syllabus
from syllabus_generator.io_utils import load_course_data
from syllabus_generator.validator import validate_course_data


def build_parser() -> argparse.ArgumentParser:
    """Build the CLI argument parser."""
    parser = argparse.ArgumentParser(
        description="Generate syllabus documents from TOML course files."
    )
    parser.add_argument(
        "course_file",
        nargs="?",
        help="Path to a course TOML file. If omitted, all TOML files in courses/ are used.",
    )
    parser.add_argument(
        "--template",
        default=str(DEFAULT_TEMPLATE_PATH),
        help="Path to the Word template.",
    )
    return parser


def _collect_course_files(course_file_arg: str | None) -> list[Path]:
    """Return the course files to process."""
    if course_file_arg:
        return [Path(course_file_arg)]

    return sorted(p for p in COURSES_DIR.glob("*.toml") if p.name != "instructor.toml")


def main() -> int:
    """Run the CLI."""
    parser = build_parser()
    args = parser.parse_args()

    template_path = Path(args.template)
    course_files = _collect_course_files(args.course_file)

    if not course_files:
        print("No course TOML files found.", file=sys.stderr)
        return 1

    failures = 0

    for course_file in course_files:
        try:
            course = load_course_data(course_file)
            validate_course_data(course, template_path)
            output_path = generate_syllabus(course, template_path)
            print(f"OK: {course_file} -> {output_path}")
        except Exception as exc:
            failures += 1
            print(f"ERROR: {course_file}", file=sys.stderr)
            print(f"{type(exc).__name__}: {exc}", file=sys.stderr)

    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
