from pathlib import Path

Path("result.txt").write_bytes(Path("input.txt").read_bytes().upper())
