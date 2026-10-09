# Restricted container benchmark execution

The runner [run_container_fixture.py](../../scripts/run_container_fixture.py) creates a disposable fixture copy and runs a reviewed command in Docker with no network, all Linux capabilities dropped, no-new-privileges, a read-only root filesystem, an unprivileged user, and bounded memory, CPU, and process count. It independently checks expected artifact digests afterward.

## Example

```sh
python3 scripts/run_container_fixture.py evaluations/benchmarks/container-copy-task.json --fixture evaluations/benchmarks/fixtures/copy-task --output /tmp/playbook-container-evidence.json
```

Docker must be installed and running; the container image may need to be pulled in advance because networking is disabled **inside** the container, not during image resolution. Pin image digests for reproducible production benchmarks.

## Threat model and limitations

- **Not a hardened sandbox:** Docker daemon privileges, kernel vulnerabilities, bind mounts, and container escape remain risks. Never mount Docker socket, home directories, SSH agents, cloud credentials, or secrets.
- The fixture is mounted read/write so the benchmark can generate artifacts. The disposable workspace is chmod-accessible to the unprivileged container user; keep it free of secrets.
- Host network isolation and daemon policies depend on the Docker installation. The container has no direct network access under the requested network mode, but Docker may still contact registries to fetch images.
- The benchmark command is passed as argv, not through a shell; it can still run arbitrary code **inside** the container.
- Evidence includes command arguments and host workspace paths. Review before sharing.
- The runner assigns a unique container name and attempts `docker rm --force` in a finally block after every run. A failed cleanup marks the benchmark failed. Abrupt host termination, daemon outages, or orphaned Docker processes can still leave containers behind; inspect the daemon after interruptions.
- Unit tests verify command construction; the optional Docker smoke test requires an available daemon. Do not claim isolation has been tested end-to-end unless that test was executed.

Use a dedicated disposable runner with rootless Docker or stronger VM isolation for untrusted agent code. Require external authorization and artifact verification before accepting a result.
