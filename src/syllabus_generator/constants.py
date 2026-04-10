"""src/syllabus_generator/constants.py.

Project constants.
"""

from pathlib import Path

PACKAGE_ROOT = Path(__file__).resolve().parent
PROJECT_ROOT = PACKAGE_ROOT.parent.parent

COURSES_DIR = PROJECT_ROOT / "courses"
TEMPLATE_DIR = PROJECT_ROOT / "template"
OUTPUTS_DIR = PROJECT_ROOT / "outputs"

DEFAULT_TEMPLATE_NAME = "Northwest-OnlineProfessional-Syllabus_Template_26.docx"
DEFAULT_TEMPLATE_PATH = TEMPLATE_DIR / DEFAULT_TEMPLATE_NAME

LEARNING_OUTCOMES_PLACEHOLDER = "{{learning_outcomes_rows}}"
GRADING_PLACEHOLDER = "{{grading_rows}}"
SCHEDULE_PLACEHOLDER = "{{schedule_rows}}"
