"""src/syllabus_generator/naming.py.

Output filename generation.
"""

import re

from syllabus_generator.models import CourseData


def _slugify_compact(value: str) -> str:
    """Return a compact filename-safe token."""
    cleaned = re.sub(r"[^A-Za-z0-9]+", "", value)
    return cleaned.strip()


def build_output_filename(course: CourseData) -> str:
    """Build the syllabus output filename."""
    line1 = _slugify_compact(course.course_name_line1)
    line2 = _slugify_compact(course.course_name_line2)
    last_name = _slugify_compact(course.instructor.last_name)
    season = _slugify_compact(course.course_season)
    block = _slugify_compact(course.course_block)

    return (
        f"{course.course_prefix}-"
        f"{course.course_number}-"
        f"{course.course_sections_filename}_"
        f"{line1}_"
        f"{line2}_"
        f"{last_name}_"
        f"{season}{course.course_yy}_"
        f"{block}.docx"
    )
