# Recording coding-agent run provenance

The benchmark protocol accepts externally supplied workspaces. To compare tools fairly, preserve metadata and hashes alongside independent acceptance results.

## Manual run protocol

1. Select a pinned task manifest and start from an identical baseline workspace for each tool.
2. Run the chosen coding assistant with the same task text and documented permission limits. Capture its transcript securely outside the repository.
3. Record the declared tool, version, task, workspace fingerprint, and transcript digest:

```sh
python3 scripts/record_agent_run.py --agent codex --version recorded-version --task uppercase-copy --workspace /path/to/submission --transcript /path/to/private-transcript.txt --output /tmp/playbook-agent-run.json
```

4. Independently verify the submission using [verify_agent_submission.py](../../scripts/verify_agent_submission.py) in an appropriately restricted environment. Preserve both JSON records.
5. Repeat across tools using the same task baseline, resource limits, and acceptance checks. Do not rank tools from one task or mix different task versions.

## Important limitations

This recorder **does not launch an agent** and **does not authenticate the claimed tool or version**. Its hashes help detect later changes to the recorded transcript/workspace, but cannot prove how the files were produced. The transcript may contain secrets; this script records only its hash and byte count, not its contents. File names and declared metadata still appear in evidence. The workspace fingerprint reads all regular files recursively, so use small, dedicated workspaces and exclude credentials before running it.

A trustworthy automated adapter will need controlled process launch, version detection, bounded permissions, structured logs, immutable baseline snapshots, and cryptographic linkage between execution and submitted artifacts.
