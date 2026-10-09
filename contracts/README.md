# Structured contracts

Contracts make scope and completion evidence reviewable and machine-validated. They do not grant execution permissions or enforce sandbox boundaries by themselves.

| Contract | Schema | Example |
| --- | --- | --- |
| Task scope and acceptance | [Task](task.schema.json) | [Feature task](examples/feature-task.json) |
| Check outcomes | [Validation](validation.schema.json) | [Validation report](examples/validation-report.json) |
| Completion evidence | [Completion](completion.schema.json) | [Completion report](examples/completion-report.json) |

## Validate locally

```sh
python3 -m pip install -r requirements-dev.txt
python3 scripts/validate_contracts.py
python3 -m unittest discover -s tests -v
```

Status values are deliberately explicit. A `not_run` check must never be presented as passed. A completion report is an evidence record, not authorization to merge or deploy.
