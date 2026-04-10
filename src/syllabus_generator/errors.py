"""src/syllabus_generator/errors.py.

Custom exceptions for syllabus generation.
"""


class SyllabusError(Exception):
    """Base exception for syllabus generation."""


class DataLoadError(SyllabusError):
    """Raised when a TOML file cannot be loaded."""


class ValidationError(SyllabusError):
    """Raised when course data fails validation."""


class TemplateError(SyllabusError):
    """Raised when the Word template cannot be processed."""
