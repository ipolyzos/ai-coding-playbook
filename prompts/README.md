# Prompt catalog

Choose the smallest template matching the task. Replace bracketed placeholders with concrete context. Templates guide behavior; CI and human review verify outcomes.

## Interactive engineering

| Goal | Prompt |
| --- | --- |
| Understand a codebase | [Explore](interactive/explore.md) |
| Compare solution architectures | [Design](interactive/design.md) |
| Break down a change | [Plan](interactive/plan.md) |
| Implement a feature | [Implement](interactive/implement.md) |
| Diagnose a defect | [Debug](interactive/debug.md) |
| Design and execute tests | [Test](interactive/test.md) |
| Review changes | [Review](interactive/review.md) |
| Improve structure safely | [Refactor](interactive/refactor.md) |

## Autonomous engineering

| Goal | Prompt |
| --- | --- |
| Validate scope and authority | [Task intake](autonomous/task-intake.md) |
| Inspect a repository | [Repository discovery](autonomous/repository-discovery.md) |
| Plan bounded execution | [Execution plan](autonomous/execution-plan.md) |
| Implement in increments | [Incremental implementation](autonomous/incremental-implementation.md) |
| Verify bounded changes | [Validation loop](autonomous/validation-loop.md) |
| Review agent output | [Self-review](autonomous/self-review.md) |
| Control authorization boundaries | [Scope control](autonomous/scope-control.md) |
| Recover from failures | [Failure recovery](autonomous/failure-recovery.md) |
| Report completion evidence | [Completion report](autonomous/completion-report.md) |

## Usage

Provide relevant paths, objective, non-goals, and acceptance criteria. For autonomous work, use the [task contract](../contracts/task.schema.json) to define boundaries. Apply [verification standards](../instructions/verification.md) to all completion reports.
