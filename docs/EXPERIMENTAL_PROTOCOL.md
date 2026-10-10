# Baseline versus playbook experimental protocol

**Status:** preregistered proposal for a personal experimental side project. No productivity claims or measured outcomes are asserted.

## Research question

For the same agent and realistic, synthetic software-engineering tasks, does the AI Coding Playbook change correctness, review effort, completion time, or scope compliance relative to ordinary agent use?

## Conditions

- **Baseline:** the selected agent receives a task objective, repository, and identical acceptance criteria, without playbook-specific contracts or workflows.
- **Playbook:** the same agent receives the same task and acceptance criteria using AICP's task contract, instructions, and verification workflow.
- **Evaluation:** an independent harness uses held-out checks that the agent cannot read or modify during execution. The same checks score both conditions.
- **No cherry-picking:** report all runs, including launch failures, timeouts, and incomplete work.

## Controls and reproducibility

1. Freeze task fixture revision, agent version, model identifier, configuration, prompt budget, tool permissions, timeout, and compute resources.
2. Start every run from a fresh, clean checkout of the same fixture commit. Use separate disposable environments per run; never reuse agent-modified state.
3. Randomize or counterbalance baseline/playbook order. Run at least three independent repetitions per condition for the pilot; label small-sample results exploratory.
4. Capture exact commands, hashes of task/fixture and checks, environment metadata, wall time, agent exit, human interventions, and costs **only when observed**.
5. Keep evaluator tests inaccessible to the agent until execution ends. Audit modified files and score from a fresh verification environment.
6. Define task completion and review criteria before examining results. Do not infer productivity improvements from lines of code or agent-reported success.
7. Store only synthetic content. Never publish secrets, private repositories, credentials, or proprietary engineering material.

## Primary and secondary outcomes

**Primary:** fraction of attempts passing all independent acceptance tests, with timeouts/failures counted as unsuccessful.

**Secondary:** elapsed wall-clock time; number of human interventions; human review minutes; regressions; out-of-scope file changes; cost or token consumption when reliably available. Missing telemetry is `null`, not zero.

Report task-level results and paired differences. Include distributions, confidence intervals when sample sizes permit, raw run counts, and limitations. Do not aggregate different agent models into a single vendor ranking.

## Pilot and expansion

Pilot with five small, deterministic synthetic tasks: bug fix, test addition, refactoring, documentation, and feature implementation. Expand to 20–30 tasks only after fixture and scoring validity are demonstrated. Publish negative and inconclusive results as well as positive results.

## Threats to validity

Agent nondeterminism, prompt leakage, model updates, order effects, task selection, imperfect cost reporting, unblinded reviewers, and unequal context budgets can bias outcomes. AICP's current `aicp run` host checks and Git audit are **not** a substitute for an independent held-out evaluator. Live agent integrations remain opt-in and are not run by CI.
