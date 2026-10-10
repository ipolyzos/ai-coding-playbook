# Synthetic pilot task suite

This is an **experimental personal side project**, not a validated productivity study.

The suite provides five small Python tasks: bug fixing, test addition, refactoring, documentation, and feature development. Each task has a starter workspace and a separate acceptance script.

## Create a fixture

```sh
python3 -m aicp.synthetic_fixtures --task bug-fix \
  --workspace /tmp/aicp-pilot/workspace \
  --evaluator /tmp/aicp-pilot/evaluator
```

The two output paths must be distinct and must not exist already. Provide only the `workspace` directory to the agent; **never mount the evaluator directory**. After agent execution, run `acceptance.py` from the workspace using a trusted process that has access to the evaluator script. This is a manual pilot workflow, not yet a fully isolated automated harness.

For example, in a disposable synthetic environment:

```sh
cd /tmp/aicp-pilot/workspace
python3 ../evaluator/acceptance.py
```

The tasks are deliberately small and the acceptance tests are minimal. In particular, the test-addition and documentation checks are structural smoke tests, not strong measures of engineering quality. They should be improved and independently reviewed before making productivity claims. The task definitions and evaluator source live in the same public repository for transparency; the evaluation environment must keep them out of the agent's runtime context. Follow the [experimental protocol](../../docs/EXPERIMENTAL_PROTOCOL.md) and report all failures and limitations.
