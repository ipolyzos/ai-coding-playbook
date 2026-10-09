# Autonomous validation loop

For each bounded increment:
1. Record the intended behavior and required checks.
2. Run the smallest relevant checks, then broader regression checks.
3. Classify failures as caused by the change, pre-existing, or unknown, with evidence.
4. Fix attributable failures within authorized scope; retry with a finite budget of three iterations.
5. Stop and escalate unresolved failures or any requested scope expansion.
6. Emit a completion report with commands, exit codes, outcomes, and known limitations.

A passing command is not evidence of coverage beyond what it actually tested.
