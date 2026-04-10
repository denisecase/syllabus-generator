"""src/syllabus_generator/io_utils.py.

Load course data from TOML.
"""



from pathlib import Path
import tomllib

from syllabus_generator.errors import DataLoadError
from syllabus_generator.models import (
    CourseData,
    GradingItem,
    Instructor,
    LearningOutcome,
    ScheduleItem,
)


def load_toml_file(path: Path) -> dict[str, object]:
    """Load and return a TOML document."""
    try:
        with path.open("rb") as handle:
            return tomllib.load(handle)
    except FileNotFoundError as exc:
        raise DataLoadError(f"Course file not found: {path}") from exc
    except tomllib.TOMLDecodeError as exc:
        raise DataLoadError(f"Invalid TOML in {path}: {exc}") from exc


def _get_required_str(mapping: dict[str, object], key: str, section: str) -> str:
    """Return a required string field with a useful error if missing."""
    if key not in mapping:
        available = ", ".join(sorted(mapping.keys()))
        raise DataLoadError(
            f"Missing required key '{key}' in section [{section}]. "
            f"Available keys: {available}"
        )
    return str(mapping[key]).strip()


def _get_required_int(mapping: dict[str, object], key: str, section: str) -> int:
    """Return a required int field with a useful error if missing."""
    if key not in mapping:
        available = ", ".join(sorted(mapping.keys()))
        raise DataLoadError(
            f"Missing required key '{key}' in section [{section}]. "
            f"Available keys: {available}"
        )
    try:
        return int(str(mapping[key]))
    except (TypeError, ValueError) as exc:
        raise DataLoadError(
            f"Key '{key}' in section [{section}] must be an integer. "
            f"Found: {mapping[key]!r}"
        ) from exc

def load_instructor_data(base_path: Path) -> Instructor:
    """Load instructor data from courses/instructor.toml."""
    instructor_path = base_path.parent / "instructor.toml"
    raw = load_toml_file(instructor_path)

    if "instructor" not in raw:
        raise DataLoadError("Missing required [instructor] section in instructor.toml.")

    instructor_raw: dict[str, object] = (
        dict(raw["instructor"]) if isinstance(raw["instructor"], dict) else {}
    )

    return Instructor(
        name=_get_required_str(instructor_raw, "instructor_name", "instructor"),
        last_name=_get_required_str(instructor_raw, "instructor_last_name", "instructor"),
        email=_get_required_str(instructor_raw, "instructor_email", "instructor"),
        office_hours=_get_required_str(instructor_raw, "instructor_office_hours", "instructor"),
        aside=_get_required_str(instructor_raw, "instructor_aside", "instructor"),
    )

def load_toml_with_extends(
    path: Path, seen: set[Path] | None = None
) -> dict[str, object]:
    """Load TOML with optional 'extends' support (shallow merge)."""
    if seen is None:
        seen = set()

    resolved_path = path.resolve()

    if resolved_path in seen:
        raise DataLoadError(f"Circular extends detected: {resolved_path}")

    seen.add(resolved_path)

    raw = load_toml_file(resolved_path)

    if "extends" not in raw:
        return raw

    parent_path = (resolved_path.parent / str(raw["extends"])).resolve()
    parent = load_toml_with_extends(parent_path, seen)

    merged = dict(parent)
    merged.update({k: v for k, v in raw.items() if k != "extends"})
    return merged

def load_course_data(path: Path) -> CourseData:
    """Load one course TOML file into CourseData."""
    raw = load_toml_with_extends(path)

    instructor = load_instructor_data(path)

    learning_outcomes_raw: object = raw.get("learning_outcomes", [])
    grading_raw = raw.get("grading", [])
    schedule_raw = raw.get("schedule", [])

    modules_raw = raw.get("modules", {})
    modules = dict(modules_raw) if isinstance(modules_raw, dict) else {}

    learning_outcomes: list[LearningOutcome] = []
    for idx, item in enumerate(learning_outcomes_raw, start=1):
        section = f"learning_outcomes[{idx}]"
        item: dict[str, object] = dict(item) if isinstance(item, dict) else {}
        assessment = item.get("assessment", [])
        learning_outcomes.append(
            LearningOutcome(
                id=_get_required_str(item, "id", section),
                description=_get_required_str(item, "description", section),
                assessment=[str(value).strip() for value in assessment],
            )
        )

    grading: list[GradingItem] = []
    for idx, item in enumerate(grading_raw, start=1):
        section = f"grading[{idx}]"
        item = dict(item) if isinstance(item, dict) else {}
        grading.append(
            GradingItem(
                component=_get_required_str(item, "component", section),
                weight=_get_required_int(item, "weight", section),
            )
        )

    schedule: list[ScheduleItem] = []
    for idx, item in enumerate(schedule_raw, start=1):
        section = f"schedule[{idx}]"
        item = dict(item) if isinstance(item, dict) else {}
        schedule.append(
            ScheduleItem(
                week=_get_required_int(item, "week", section),
                topic=_get_required_str(item, "topic", section),
                deliverable=_get_required_str(item, "deliverable", section),
            )
        )

    return CourseData(
        course_prefix=_get_required_str(raw, "course_prefix", "root"),
        course_number=_get_required_str(raw, "course_number", "root"),
        course_sections=_get_required_str(raw, "course_sections", "root"),
        course_year=_get_required_str(raw, "course_year", "root"),
        course_yy=_get_required_str(raw, "course_yy", "root"),
        course_season=_get_required_str(raw, "course_season", "root"),
        course_block=_get_required_str(raw, "course_block", "root"),
        course_name_line1=_get_required_str(raw, "course_name_line1", "root"),
        course_name_line2=_get_required_str(raw, "course_name_line2", "root"),
        course_short_name=_get_required_str(raw, "course_short_name", "root"),
        materials_textbook=_get_required_str(raw, "materials_textbook", "root"),
        materials_other=_get_required_str(raw, "materials_other", "root"),
        modules=modules,
        placement=_get_required_str(raw, "placement", "root"),
        prereqs=_get_required_str(raw, "prereqs", "root"),
        credits=_get_required_str(raw, "credits", "root"),
        description=_get_required_str(raw, "description", "root"),
        rationale=_get_required_str(raw, "rationale", "root"),
        instructor=instructor,
        learning_outcomes=learning_outcomes,
        grading=grading,
        schedule=schedule,
    )
