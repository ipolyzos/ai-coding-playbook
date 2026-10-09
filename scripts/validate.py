#!/usr/bin/env python3
"""Dependency-free validation of JSON files and relative Markdown links."""
import json
import re
from pathlib import Path

root = Path(__file__).resolve().parents[1]
errors = []
for path in root.rglob('*.json'):
    if '.git' in path.parts:
        continue
    try:
        json.loads(path.read_text(encoding='utf-8'))
    except (ValueError, UnicodeError) as exc:
        errors.append(f'{path.relative_to(root)}: {exc}')
for path in root.rglob('*.md'):
    if '.git' in path.parts:
        continue
    text = path.read_text(encoding='utf-8')
    for target in re.findall(r'(?<!!)\[[^\]]+\]\(([^)]+)\)', text):
        if target.startswith(('http:', 'https:', '#', 'mailto:')):
            continue
        destination = (path.parent / target.split('#', 1)[0]).resolve()
        if not destination.is_relative_to(root) or not destination.exists():
            errors.append(f'{path.relative_to(root)}: broken link {target}')
if errors:
    raise SystemExit('\n'.join(errors))
print('JSON and local Markdown links validated')
