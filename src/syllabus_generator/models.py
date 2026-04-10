"""src/syllabus_generator/models.py.

Data models for syllabus generation.
"""

from dataclasses import dataclass, field

@dataclass(slots=True)
class LearningOutcome:
    """Student learning outcome."""

    id: str
    description: str
    assessment: list[str]


@dataclass(slots=True)
class Instructor:
    """Instructor information."""

    name: str
    last_name: str
    email: str
    office_hours: str
    aside: str


@dataclass(slots=True)
class GradingItem:
    """Grading breakdown item."""

    component: str
    weight: int


@dataclass(slots=True)
class ScheduleItem:
    """Schedule item."""

    week: int
    topic: str
    deliverable: str


@dataclass(slots=True)
class CourseData:
    """Top-level course data."""

    course_prefix: str
    course_number: str
    course_sections: str
    course_year: str
    course_yy: str
    course_season: str
    course_block: str
    course_name_line1: str
    course_name_line2: str
    course_short_name: str
    materials_textbook: str
    materials_other: str
    modules: dict[str, str]
    placement: str
    prereqs: str
    credits: str
    description: str
    rationale: str
    instructor: Instructor
    learning_outcomes: list[LearningOutcome] = field(default_factory=lambda: [])
    grading: list[GradingItem] = field(default_factory=lambda: [])
    schedule: list[ScheduleItem] = field(default_factory=lambda: [])

    @property
    def course_name_full(self) -> str:
        """Return the combined course name."""
        return f"{self.course_name_line1} {self.course_name_line2}".strip()

    @property
    def course_sections_filename(self) -> str:
        """Return section text normalized for filenames."""
        return self.course_sections.replace("/", "")
