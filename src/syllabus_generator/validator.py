"""src/syllabus_generator/validator.py.

Validation for course data.
"""

from pathlib import Path
import re

from syllabus_generator.errors import ValidationError
from syllabus_generator.models import CourseData


def _require_non_empty(value: str, field_name: str, errors: list[str]) -> None:
    """Require a non-empty string."""
    if not value.strip():
        errors.append(f"{field_name} must not be empty.")


def validate_course_data(course: CourseData, template_path: Path) -> None:
    """Validate a CourseData instance."""
    errors: list[str] = []

    if not template_path.exists():
        errors.append(f"Template file not found: {template_path}")

    scalar_fields = {
        "course_prefix": course.course_prefix,
        "course_number": course.course_number,
        "course_sections": course.course_sections,
        "course_year": course.course_year,
        "course_yy": course.course_yy,
        "course_season": course.course_season,
        "course_block": course.course_block,
        "course_name_line1": course.course_name_line1,
        "course_name_line2": course.course_name_line2,
        "course_short_name": course.course_short_name,
        "materials_textbook": course.materials_textbook,
        "materials_other": course.materials_other,
        "placement": course.placement,
        "prereqs": course.prereqs,
        "credits": course.credits,
        "description": course.description,
        "rationale": course.rationale,
        "instructor.name": course.instructor.name,
        "instructor.last_name": course.instructor.last_name,
        "instructor.email": course.instructor.email,
        "instructor.office_hours": course.instructor.office_hours,
        "instructor.aside": course.instructor.aside,
    }

    for field_name, value in scalar_fields.items():
        _require_non_empty(value, field_name, errors)

    if not re.fullmatch(r"\d{4}", course.course_year):
        errors.append("course_year must be a 4-digit year, for example 2026.")

    if not re.fullmatch(r"\d{2}", course.course_yy):
        errors.append("course_yy must be a 2-digit year, for example 26.")

    if not course.learning_outcomes:
        errors.append("At least one learning outcome is required.")

    for index, item in enumerate(course.learning_outcomes, start=1):
        if not item.id:
            errors.append(f"learning_outcomes[{index}] missing id.")
        elif not re.fullmatch(r"LO\d+", item.id):
            errors.append(
                f"learning_outcomes[{index}] id must look like LO1, LO2, etc."
            )

        if not item.description:
            errors.append(f"learning_outcomes[{index}] missing description.")

        if not item.assessment:
            errors.append(f"learning_outcomes[{index}] must include assessment items.")

    if not course.grading:
        errors.append("At least one grading item is required.")

    grading_total = 0
    for index, item in enumerate(course.grading, start=1):
        if not item.component:
            errors.append(f"grading[{index}] missing component.")
        if item.weight < 0:
            errors.append(f"grading[{index}] weight must be non-negative.")
        grading_total += item.weight

    if grading_total != 100:
        errors.append(f"Grading weights must sum to 100. Found {grading_total}.")

    for index, item in enumerate(course.schedule, start=1):
        if item.week < 1:
            errors.append(f"schedule[{index}] week must be >= 1.")
        if not item.topic:
            errors.append(f"schedule[{index}] missing topic.")
        if not item.deliverable:
            errors.append(f"schedule[{index}] missing deliverable.")

    if errors:
        raise ValidationError(
            f"Validation failed for {course.course_number}:\n" + "\n".join(errors)
        )
