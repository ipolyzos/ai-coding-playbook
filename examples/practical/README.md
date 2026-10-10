# Runnable practical example

This fictional Python service demonstrates AICP onboarding, scoped tasks, and independent verification without vendor credentials, Docker, a network connection, or real personal data.

From the **playbook repository root**, copy the fixture to a disposable directory:

```sh
PROJECT="$(mktemp -d)"
cp -R examples/practical/. "$PROJECT/"
python3 -m aicp init --tool codex --path "$PROJECT" --dry-run
python3 -m aicp init --tool codex --path "$PROJECT"
python3 -m aicp validate --path "$PROJECT"
python3 -m aicp task create \
  --path "$PROJECT" \
  --name improve-retry \
  --objective "Review retry behavior and add a regression test for a newly identified edge case" \
  --allow sample_service.py \
  --allow tests/ \
  --accept "A regression test covers the chosen edge case" \
  --accept "All tests pass"
python3 -m aicp verify \
  --path "$PROJECT" \
  --checks "$PROJECT/checks.json" \
  --output "$PROJECT/verification.json"
```

Inspect `$PROJECT/tasks/improve-retry.json` and `$PROJECT/verification.json`. The sample implementation already passes its existing tests; the task is a **practice exercise**, not a known failing defect. Ask your coding assistant to propose an additional edge case and wait for approval before changing code. To try the documentation-only workflow, edit this fixture's README on a feature branch and review its diff.

**Security:** `aicp verify` executes the reviewed commands with your host permissions, not in a sandbox. Use only the supplied trusted fixture and inspect any changes before running checks. `mktemp -d` creates a fresh temporary directory; remove it yourself when finished. The output path must not already exist, so use a new directory for each run. No agent is launched or PR created automatically.

For the complete narrative see [usage guide](../../docs/USAGE_GUIDE.md) and [practical walkthrough](../../docs/PRACTICAL_WALKTHROUGH.md).
