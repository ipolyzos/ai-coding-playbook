# Compatibility and integration testing

The GitHub Actions [Validate workflow](../.github/workflows/validate.yml) runs the standard validation job and a compatibility matrix for Python 3.10, 3.12, and 3.13 on Linux, plus Python 3.12 on macOS. Each matrix job installs the package, exercises the installed CLI, and runs unit tests. This matrix is a compatibility sample, not a guarantee for every Python version and operating system.

## Agent integration tests

Unit tests for `aicp run` mock the agent executable. They do **not** validate real Codex, Claude, or Gemini CLI behavior. Real agent integration testing is intentionally **manual and opt-in**, because it requires vendor installations, authentication, a disposable host, and potentially network access.

Before attempting a real run:

1. Provision an isolated, disposable machine with no personal or organization credentials beyond the minimum vendor-specific test account.
2. Review the agent command and the task and checks files; use synthetic data only.
3. Explicitly approve host execution and run `aicp run` as documented in [CLI](CLI.md).
4. Review modified files, command hashes, exit statuses, and test evidence; do not treat the JSON report as scope enforcement or proof of isolation.
5. Delete the disposable environment and revoke temporary credentials.

The project does not execute live vendor agents in standard CI. Do not add real API keys or private project data to workflow fixtures.
