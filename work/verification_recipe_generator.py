#!/usr/bin/env python3
"""Verification Recipe Generator.

Emit a human-executable verification recipe (Markdown) for a confirmed finding,
following `knowledge/human/verification-recipe-template.md`. This is an
instruction sheet for a human to verify a finding; it is NOT proof of a
vulnerability and never submits reports.

The generator is deterministic for a given input+date and validates that every
referenced raw-evidence file exists before writing. It never invents values: it
emits only the fields present in the input finding record, marking missing
optional sections as "Not recorded / not applicable".

Usage:
    python verification_recipe_generator.py \
        --input <finding.json> --output <recipe.md> [--date YYYY-MM-DD]

Runs offline; does not contact any target.
"""

import argparse
import json
import os
import sys

VERSION = "1.0.0"

BANNER = (
    "> :warning: THIS RECIPE IS NOT PROOF OF A VULNERABILITY.\n"
    "> It is an instruction sheet for a human to verify a finding the system\n"
    "> believes is confirmed. A human must manually reproduce and validate the\n"
    "> finding before it may be reported. This system never submits bug-bounty\n"
    "> reports automatically."
)

# Section order and the keys they read from the finding record.
# Section 1 (Recipe identification) is emitted manually in
# generate_recipe_markdown(); it is intentionally not listed here.
SECTIONS = [
    ("2. Finding and vulnerability class", ["class"], "REQUIRED"),
    ("3. Target endpoint/surface", ["component"], "REQUIRED"),
    ("4. Preconditions and required authorization", ["preconditions"], "REQUIRED"),
    ("5. Exact reproduction steps", ["reproduction_steps"], "REQUIRED"),
    ("6. Minimal test input/request", ["minimal_request"], "REQUIRED"),
    ("7. Benign control test", ["control_test"], "REQUIRED"),
    ("8. Expected vulnerable vs. safe behavior",
     ["expected_vulnerable", "expected_safe"], "REQUIRED"),
    ("9. Evidence to capture", ["evidence_to_capture", "evidence_files"], "REQUIRED"),
    ("10. Safety limits and stop conditions", ["safety_limits", "stop_conditions"], "REQUIRED"),
    ("11. Cleanup requirements", ["cleanup"], "REQUIRED"),
    ("12. Reporting notes", ["reporting_notes"], "REQUIRED"),
]


def _rules(base_dir, path):
    """Return full path for a repo-relative path, or None if outside base_dir."""
    full = os.path.normpath(os.path.join(base_dir, path))
    root = os.path.normpath(base_dir)
    if full != root and not full.startswith(root + os.sep):
        return None
    return full


def _render_value(finding, keys, markdown_code=False):
    """Render a section value from one or more finding keys."""
    parts = []
    for key in keys:
        value = finding.get(key)
        if value in (None, "", [], {}):
            continue
        if isinstance(value, list):
            for item in value:
                s = str(item).strip()
                if s:
                    parts.append(f"- {s}")
        elif isinstance(value, str):
            s = value.strip()
            if s:
                if markdown_code:
                    parts.append(f"```\n{s}\n```")
                else:
                    parts.append(s)
    return "\n\n".join(parts)


def generate_recipe_markdown(finding, base_dir, generated_on):
    """Return the full recipe Markdown string for a finding record."""
    out = []
    out.append("# Verification Recipe")
    out.append("")
    out.append(BANNER)
    out.append("")
    out.append("## 0. Status banner")
    out.append("Status: **Instruction sheet only — NOT proof. Requires human manual verification.**")
    out.append("")

    out.append("## 1. Recipe identification")
    out.extend([
        f"- Recipe ID: {finding.get('recipe_id', 'UNSPECIFIED')}",
        f"- Source finding: {finding.get('source_finding', 'Not recorded')}",
        f"- Confirmation status: {finding.get('confirmation_status', 'Not recorded')}",
        f"- Generated on: {generated_on}",
        f"- Generator version: {VERSION}",
    ])
    out.append("")

    # Resolve + validate evidence file references up-front (fail fast, offline).
    evidence_files = finding.get("evidence_files", []) or []
    missing = []
    for rel in evidence_files:
        full = _rules(base_dir, rel)
        if not full:
            raise ValueError(f"Evidence path escapes repo root: {rel}")
        if not os.path.isfile(full):
            missing.append(rel)
    if missing:
        raise FileNotFoundError(
            "Referenced raw evidence file(s) missing: " + ", ".join(missing))

    for header, keys, need in SECTIONS:
        out.append(f"## {header}")
        if header.startswith("9."):
            captured = _render_value(finding, ["evidence_to_capture"])
            if captured:
                out.append("What to capture:")
                out.append(captured)
            if evidence_files:
                out.append("Referenced raw evidence (existing, preserved separately):")
                for rel in evidence_files:
                    out.append(f"- `{rel}`")
        else:
            is_request = header.startswith("6.")
            rendered = _render_value(finding, keys, markdown_code=is_request)
            if rendered:
                out.append(rendered)
            else:
                out.append("*Not recorded / not applicable.*")
        out.append("")

    return "\n".join(out)


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__,
                                     formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--input", required=True, help="Finding record JSON path.")
    parser.add_argument("--output", required=True, help="Recipe Markdown output path.")
    parser.add_argument("--date", default=None, help="Generation date (YYYY-MM-DD).")
    args = parser.parse_args(argv)

    here = os.path.dirname(os.path.abspath(__file__))
    base_dir = os.path.dirname(here)  # repo root (work/ -> root)
    with open(args.input, "r", encoding="utf-8") as fh:
        finding = json.load(fh)
    generated_on = args.date or os.environ.get("WG_DATE", "").strip()
    if not generated_on:
        from datetime import date
        generated_on = date.today().isoformat()

    recipe = generate_recipe_markdown(finding, base_dir, generated_on)
    out_path = args.output if os.path.isabs(args.output) else os.path.join(base_dir, args.output)
    os.makedirs(os.path.dirname(os.path.abspath(out_path)), exist_ok=True)
    with open(out_path, "w", encoding="utf-8") as fh:
        fh.write(recipe)
    print(f"Wrote {os.path.relpath(out_path, base_dir)} ({len(recipe)} chars)")
    return 0


if __name__ == "__main__":
    sys.exit(main())

