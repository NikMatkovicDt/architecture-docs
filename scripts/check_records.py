#!/usr/bin/env python3
"""Check ADRs, RFCs and research notes against docs/FORMAT.md.

    python3 check_records.py PATH...    (files or folders)

Folders are searched for records (title `# ADR-`, `# RFC-` or `# Research:`);
TEMPLATE.md files and other Markdown are skipped. A file named directly must be a
record. Prints `file:line: problem` and exits 1 on any problem. Standard library only.
"""

from __future__ import annotations

import re
import sys
from datetime import date
from pathlib import Path

ID = r"ADR-\d{4}(, ADR-\d{4})*"
KINDS = {
    "ADR": {
        "title": re.compile(r"# ADR-(\d{4}): \S"),
        "file": re.compile(r"(\d{4})-[a-z0-9]+(-[a-z0-9]+)*\.md"),
        # key -> (required, allowed value pattern)
        "meta": {
            "Status": (True, r"Proposed|Accepted|Rejected|Deprecated|Superseded"),
            "Date": (True, None),
            "Author": (True, r".+"),
            "Scope": (True, r"org|repo"),
            "Supersedes": (False, ID),
            "Superseded by": (False, ID),
        },
        # section -> required
        "sections": {
            "Context": True,
            "Decision": True,
            "Alternatives considered": True,
            "Consequences": True,
            "Related": True,
        },
    },
    "RFC": {
        "title": re.compile(r"# RFC-(\d{4}): \S"),
        "file": re.compile(r"(\d{4})-[a-z0-9]+(-[a-z0-9]+)*\.md"),
        "meta": {
            "Status": (True, r"Draft|Proposed|Accepted|Rejected|Withdrawn"),
            "Date": (True, None),
            "Author": (True, r".+"),
        },
        "sections": {
            "Summary": True,
            "Motivation": True,
            "Proposed rules": True,
            "Alternatives considered": True,
            "Related": True,
        },
    },
    "Research": {
        "title": re.compile(r"# Research: \S"),
        "file": re.compile(r"[a-z0-9]+(-[a-z0-9]+)*\.md"),
        "meta": {
            "Status": (True, r"Open|In progress|Answered|Time-boxed out"),
            "Date": (True, None),
            "Author": (True, r".+"),
            "Type": (True, r"question|spike"),
            "Requested by": (False, r".+"),
            "Time-box": (False, r".+"),
        },
        "sections": {
            "Question": True,
            "Answer": True,
            "Criteria": True,
            "Options": True,
            "Prototype": False,
            "Risks and unknowns": True,
            "Recommendation": True,
            "Sources": True,
        },
    },
}
META = re.compile(r"- \*\*([^*]+):\*\* (.*)")
# Template placeholders: NNNN, YYYY-MM-DD and <...> outside `code` (autolinks allowed).
PLACEHOLDER = re.compile(r"NNNN|YYYY-MM-DD|<(?!https?:)[A-Za-z][^<>\n]*>")
CODE_SPAN = re.compile(r"`[^`]*`")


def kind_of(text: str) -> str | None:
    first = text.split("\n", 1)[0]
    for kind in KINDS:
        if first.startswith(f"# {kind}-" if kind != "Research" else "# Research:"):
            return kind
    return None


def check(path: Path, text: str, kind: str) -> list[str]:
    spec = KINDS[kind]
    lines = text.split("\n")
    errs: list[str] = []

    def err(n: int, msg: str) -> None:
        errs.append(f"{path}:{n}: {msg}")

    title = spec["title"].match(lines[0])
    if not title:
        err(1, f"title must look like {spec['title'].pattern!r}")
    fname = spec["file"].fullmatch(path.name)
    if not fname:
        err(1, f"file name must match {spec['file'].pattern!r}")
    elif title and kind != "Research" and fname.group(1) != title.group(1):
        err(1, f"title number {title.group(1)} differs from file number {fname.group(1)}")

    # Metadata: a list right after the title (one blank line allowed before it).
    i = 2 if len(lines) > 1 and lines[1] == "" else 1
    meta: dict[str, tuple[int, str]] = {}
    order: list[str] = []
    while i < len(lines) and lines[i].startswith("- **"):
        m = META.fullmatch(lines[i].rstrip())
        if not m:
            err(i + 1, "metadata line must be '- **Key:** value'")
        elif m.group(1) not in spec["meta"]:
            err(i + 1, f"unknown metadata key {m.group(1)!r}")
        else:
            meta[m.group(1)] = (i + 1, m.group(2).strip())
            order.append(m.group(1))
        i += 1
    keys = list(spec["meta"])
    if order != sorted(order, key=keys.index):
        err(3, f"metadata out of order; order is {', '.join(keys)}")
    for key, (required, pattern) in spec["meta"].items():
        if key not in meta:
            if required:
                err(3, f"missing metadata '{key}'")
            continue
        n, value = meta[key]
        if key == "Date":
            try:
                date.fromisoformat(value)
            except ValueError:
                err(n, "Date must be YYYY-MM-DD")
        elif pattern and not re.fullmatch(pattern, value):
            err(n, f"{key} must match {pattern!r}, got {value!r}")
    if kind == "ADR" and meta.get("Status", (0, ""))[1] == "Superseded" and "Superseded by" not in meta:
        err(meta["Status"][0], "a Superseded ADR needs 'Superseded by'")

    # Sections: `##` headings outside code fences, exactly the allowed ones, in order.
    found: list[tuple[int, str]] = []
    fenced = False
    for n, line in enumerate(lines, 1):
        if line.startswith("```"):
            fenced = not fenced
        elif not fenced and line.startswith("## "):
            found.append((n, line[3:].strip()))
        elif not fenced and n > 1 and re.match(r"# ", line):
            err(n, "only one '#' title per file")
        hole = None if fenced else PLACEHOLDER.search(CODE_SPAN.sub("", line))
        if hole:
            err(n, f"template placeholder left in: {hole.group(0)!r}")
    names = list(spec["sections"])
    for n, name in found:
        if name not in spec["sections"]:
            err(n, f"unexpected section '## {name}'; allowed: {', '.join(names)}")
    present = [name for _, name in found if name in spec["sections"]]
    if present != sorted(present, key=names.index) or len(set(present)) != len(present):
        err(found[0][0] if found else 1, f"sections out of order or repeated; order is {', '.join(names)}")
    for name, required in spec["sections"].items():
        if required and name not in present:
            err(1, f"missing section '## {name}'")
    # Each section has some text before the next one.
    bounds = [n for n, _ in found] + [len(lines) + 1]
    # A research note still being worked on may have empty sections.
    drafting = kind == "Research" and meta.get("Status", (0, ""))[1] in ("Open", "In progress")
    for (n, name), end in zip(found, bounds[1:]):
        if not drafting and not any(line.strip() for line in lines[n : end - 1]):
            err(n, f"section '## {name}' is empty")
    return errs


def main(args: list[str]) -> int:
    if not args:
        print(__doc__.strip(), file=sys.stderr)
        return 2
    errs: list[str] = []
    records: list[tuple[Path, str]] = []
    for arg in args:
        p = Path(arg)
        if p.is_dir():
            files = [(f, False) for f in sorted(p.rglob("*.md")) if f.name != "TEMPLATE.md"]
        elif p.is_file():
            files = [(p, True)]
        else:
            errs.append(f"{arg}: no such file or folder")
            continue
        for f, explicit in files:
            kind = kind_of(f.read_text(encoding="utf-8"))
            if kind:
                records.append((f, kind))
            elif explicit:
                errs.append(f"{f}:1: not a record (title must start '# ADR-', '# RFC-' or '# Research:')")
    for f, kind in records:
        errs += check(f, f.read_text(encoding="utf-8"), kind)
        # A number is unique per folder and kind, against every record there.
        if kind != "Research" and re.match(r"\d{4}-", f.name):
            for other in sorted(f.parent.glob(f"{f.name[:4]}-*.md")):
                if other != f and kind_of(other.read_text(encoding="utf-8")) == kind:
                    errs.append(f"{f}:1: {kind}-{f.name[:4]} is also used by {other.name}")
    for e in errs:
        print(e)
    print(f"{len(records)} record(s) checked, {len(errs)} problem(s)", file=sys.stderr)
    return 1 if errs else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
