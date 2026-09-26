#!/usr/bin/env python3
"""Regression test for the Verification Recipe Generator.

Verifies the behavior required by `.clinerules/06-verification.md` stays in
place permanently:
- every mandatory recipe section is present,
- the mandatory "NOT proof / human manual verification" status banner is present,
- referenced raw-evidence files exist (the generator fails fast otherwise),
- the generator is deterministic for a fixed input+date,
- unspecified optional fields render as "Not recorded / not applicable".

Runs offline. Usage:  python test_verification_recipe.py
"""

import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, HERE)

import verification_recipe_generator as g

REQUIRED_HEADERS = [
    "## 0. Status banner",
    "## 1. Recipe identification",
    "## 2. Finding and vulnerability class",
    "## 3. Target endpoint/surface",
    "## 4. Preconditions and required authorization",
    "## 5. Exact reproduction steps",
    "## 6. Minimal test input/request",
    "## 7. Benign control test",
    "## 8. Expected vulnerable vs. safe behavior",
    "## 9. Evidence to capture",
    "## 10. Safety limits and stop conditions",
    "## 11. Cleanup requirements",
    "## 12. Reporting notes",
]

BANNER_MARKERS = [
    "THIS RECIPE IS NOT PROOF OF A VULNERABILITY",
    "manually reproduce and validate",
    "never submits bug-bounty",  # accepts the generator phrasing "accident" note
]


def load_input(path):
    with open(path, "r", encoding="utf-8") as fh:
        return json.load(fh)


def test_all_sections_present():
    finding = load_input(os.path.join(HERE, "verification_recipe_example_input.json"))
    recipe = g.generate_recipe_markdown(finding, ROOT, "2026-01-01")
    missing = [h for h in REQUIRED_HEADERS if h not in recipe]
    assert not missing, f"Missing recipe sections: {missing}"
    print("ok: all required sections present (%d)" % len(REQUIRED_HEADERS))


def test_banner_present():
    finding = load_input(os.path.join(HERE, "verification_recipe_example_input.json"))
    recipe = g.generate_recipe_markdown(finding, ROOT, "2026-01-01")
    for marker in BANNER_MARKERS:
        assert marker in recipe, f"Banner marker missing: {marker}"
    print("ok: status banner (not-proof / manual verification) present")


def test_evidence_references_exist():
    finding = load_input(os.path.join(HERE, "verification_recipe_example_input.json"))
    # Generate must not raise for the valid example input.
    g.generate_recipe_markdown(finding, ROOT, "2026-01-01")
    for rel in finding["evidence_files"]:
        full = os.path.join(ROOT, rel)
        assert os.path.isfile(full), f"Raw evidence file missing: {rel}"
    print("ok: referenced raw-evidence files exist (%d)" % len(finding["evidence_files"]))


def test_missing_evidence_fails():
    finding = load_input(os.path.join(HERE, "verification_recipe_example_input.json"))
    bad = dict(finding)
    bad["evidence_files"] = ["evidence/reporting/raw/does_not_exist.txt"]
    try:
        g.generate_recipe_markdown(bad, ROOT, "2026-01-01")
    except FileNotFoundError:
        print("ok: missing raw-evidence reference fails fast")
        return
    raise AssertionError("expected FileNotFoundError for missing raw evidence")


def test_path_escape_rejected():
    finding = load_input(os.path.join(HERE, "verification_recipe_example_input.json"))
    bad = dict(finding)
    bad["evidence_files"] = ["../outside.txt"]
    try:
        g.generate_recipe_markdown(bad, ROOT, "2026-01-01")
    except ValueError:
        print("ok: evidence path escaping repo root rejected")
        return
    raise AssertionError("expected ValueError for escaping path")


def test_deterministic_output():
    finding = load_input(os.path.join(HERE, "verification_recipe_example_input.json"))
    a = g.generate_recipe_markdown(finding, ROOT, "2026-01-01")
    b = g.generate_recipe_markdown(finding, ROOT, "2026-01-01")
    assert a == b, "output is not deterministic for fixed input + date"
    print("ok: deterministic output for fixed input + date (%d chars)" % len(a))


def test_unknown_optional_renders_notrecorded():
    minimal = {
        "recipe_id": "T", "class": "C", "component": "E",
        "preconditions": ["P"], "reproduction_steps": ["1. go"],
    }
    recipe = g.generate_recipe_markdown(minimal, ROOT, "2026-01-01")
    assert "Not recorded / not applicable" in recipe, "expected placeholder for omitted fields"
    print("ok: omitted optional fields render as not-recorded placeholder")


def main():
    tests = [
        test_all_sections_present,
        test_banner_present,
        test_evidence_references_exist,
        test_missing_evidence_fails,
        test_path_escape_rejected,
        test_deterministic_output,
        test_unknown_optional_renders_notrecorded,
    ]
    for t in tests:
        t()
    print("\nAll verification-recipe generator tests passed (%d)." % len(tests))
    return 0


if __name__ == "__main__":
    sys.exit(main())
