# denisecase: syllabus-generator

[![PyPI version](https://img.shields.io/pypi/v/denisecase/syllabus-generator)](https://pypi.org/project/denisecase/syllabus-generator/)
[![Latest Release](https://img.shields.io/github/v/release/denisecase/syllabus-generator)](https://github.com/denisecase/syllabus-generator/releases)
[![Docs](https://img.shields.io/badge/docs-live-blue)](https://denisecase.github.io/syllabus-generator/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/license/MIT)
[![CI](https://github.com/denisecase/syllabus-generator/actions/workflows/ci-python-zensical.yml/badge.svg?branch=main)](https://github.com/denisecase/syllabus-generator/actions/workflows/ci-python-zensical.yml)
[![Deploy-Docs](https://github.com/denisecase/syllabus-generator/actions/workflows/deploy-zensical.yml/badge.svg?branch=main)](https://github.com/denisecase/syllabus-generator/actions/workflows/deploy-zensical.yml)
[![Check Links](https://github.com/denisecase/syllabus-generator/actions/workflows/links.yml/badge.svg)](https://github.com/denisecase/syllabus-generator/actions/workflows/links.yml)
[![Dependabot](https://img.shields.io/badge/Dependabot-enabled-brightgreen.svg)](https://github.com/denisecase/syllabus-generator/security)

> This repository creates course and term specific syllabi from a Microsoft Word Syllabus Template.

## Outputs

This repository produces documents under `outputs/`.

Output files are named:

`course_prefix-course_number-course_sections_course_name_line1_course_name_line2_last_name_course_season_course_yy_course_block.docx`

e.g. `44-620-8081_WebMiningAndAppliedNLP_Case_Sp26_OP2.docx`

## Quick start (Generation)

Update/add a data file in courses/.
See example [courses/44-608-2026-FA-OP1.toml](courses/44-608-2026-FA-OP1.toml).

Run the full script either for a single data file or for all:

```shell
uv run python -m syllabus_generator.cli courses/44-608-2026-FA-OP1.toml
uv run python -m syllabus_generator.cli
```

## No Slashes (/ or \)

IMPORTANT: Do not use `\` or `/` in course_sections or course_number.
Just combine, e.g. `613413` and `808103`.

## Adding a New Data Field

To add a new field (e.g., `course_short_name`, `materials_textbook`, `materials_other`), follow these steps.

### 1. Add to the data file (TOML)

Add the new field to your course file in `courses/`.

Example:

```toml
course_short_name = "Web Mining & NLP"

materials_textbook = """
No required textbook. There are no required textbooks for this course.
Mining the Social Web 3rd Edition by Matthew A. Russell (Author), Mikhail Klassen (Author)
ISBN: 978-1491985045 is optional, but recommended; it has a lot of good information and resources.
"""

materials_other = "Additional free resources as directed by instructor."
```

Notes:

- Use triple quotes `"""` for multiline text.
- Triple quotes must open and close on their own line.
- Keep field names consistent across all course files.

### 2. Add to the Word template

Open: `template/Northwest-OnlineProfessional-Syllabus_Template_26.docx`

Insert placeholders where the values should appear:

```text
{{course_short_name}}
{{materials_textbook}}
{{materials_other}}
```

Notes:

- Placeholders must match field names exactly.
- Do not add extra spaces inside `{{ }}`.
- Avoid splitting placeholders across lines or formatting runs.

### 3. Add to the data model (models.py)

Update `CourseData` in: `src/syllabus_generator/models.py`

Add new fields:

```python
course_short_name: str
materials_textbook: str
materials_other: str
```

### 4. Load the field (io_utils.py)

Update the loader in: `src/syllabus_generator/io_utils.py`

Add to the constructor:

```python
course_short_name=_get_required_str(raw, "course_short_name", "root"),
materials_textbook=_get_required_str(raw, "materials_textbook", "root"),
materials_other=_get_required_str(raw, "materials_other", "root"),
```

### 5. Add to replacements (generator.py)

Update: `src/syllabus_generator/generator.py`

Add to `build_replacements()`:

```python
"{{course_short_name}}": course.course_short_name,
"{{materials_textbook}}": course.materials_textbook,
"{{materials_other}}": course.materials_other,
```

### 6. Validate (optional but recommended)

If the field is required, add a check in:
`src/syllabus_generator/validator.py`

Example:

```python
_require_non_empty(course.course_short_name, "course_short_name", errors)
```

### 7. Generate and verify

Run:

```shell
uv run python -m syllabus_generator.cli courses/44-620-2026-SP-OP2.toml
```

Confirm:

- Field appears in output document
- Formatting is correct
- No placeholder text remains

### Design guidance

- Scalar fields → use simple `{{field_name}}` replacement
- Repeated/tabular data → use `[[...]]` in TOML + table row generation in code
- Multiline prose → use triple-quoted TOML strings

Keep the template stable and evolve fields through the data + generator pipeline.

## Command Reference

The commands below are used in the workflow guide above.
They are provided here for convenience.

Follow the guide for the **full instructions**.

<details>
<summary>Show command reference</summary>

### In a machine terminal (open in your `Repos` folder)

After you get a copy of this repo in your own GitHub account,
open a machine terminal in your `Repos` folder:

```shell
# Replace username with YOUR GitHub username.
git clone https://github.com/username/syllabus-generator

cd syllabus-generator
code .
```

### In a VS Code terminal

```shell
uv self update
uv python pin 3.14
uv sync --extra dev --extra docs --upgrade

uvx pre-commit install
git add -A
uvx pre-commit run --all-files

# run Python

uv run ruff format .
uv run ruff check . --fix
uv run zensical build

git add -A
git commit -m "update"
git push -u origin main
```

</details>

## Annotations

[ANNOTATIONS.md](./ANNOTATIONS.md) - REQ/WHY/OBS annotations used

## Citation

[CITATION.cff](./CITATION.cff)

## License

[MIT](./LICENSE)

## SE Manifest

[SE_MANIFEST.toml](./SE_MANIFEST.toml) - project intent, scope, and role
