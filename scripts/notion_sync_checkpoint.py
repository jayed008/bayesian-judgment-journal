"""Select changed journal files and persist the cutoff of a verified Notion sync."""

import argparse
import fcntl
import json
import os
import tempfile
import time
from pathlib import Path
from uuid import UUID


def read_cutoff(state_path):
    try:
        cutoff = json.loads(state_path.read_text(encoding="utf-8"))["cutoff_ns"]
    except FileNotFoundError:
        return 0
    if type(cutoff) is not int or cutoff <= 0:
        raise ValueError("Invalid saved sync cutoff")
    return cutoff


def scan(records, state_path):
    started_at_ns = time.time_ns()
    previous_cutoff_ns = read_cutoff(state_path)
    if previous_cutoff_ns >= started_at_ns:
        raise ValueError("The local clock has not passed the saved sync cutoff")

    paths = [records / "journal.md"]
    for folder, prefix in (("judgments", "J"), ("events", "E")):
        paths.extend(sorted((records / folder).glob(f"{prefix}-*.md")))

    files = []
    for path in paths:
        mtime_ns = path.stat().st_mtime_ns
        files.append({
            "path": path.relative_to(records).as_posix(),
            "mtime_ns": str(mtime_ns),
            "changed": mtime_ns > previous_cutoff_ns,
        })
    print(json.dumps({
        "started_at_ns": str(started_at_ns),
        "previous_cutoff_ns": str(previous_cutoff_ns),
        "baseline_required": previous_cutoff_ns == 0,
        "files": files,
    }, ensure_ascii=False))


def commit(state_path, started_at_ns, previous_cutoff_ns):
    if not 0 <= previous_cutoff_ns < started_at_ns <= time.time_ns():
        raise ValueError("Invalid sync cutoff")

    lock_path = state_path.with_suffix(".lock")
    with lock_path.open("a") as lock_file:
        fcntl.flock(lock_file, fcntl.LOCK_EX)
        if read_cutoff(state_path) != previous_cutoff_ns:
            raise ValueError("Another sync updated the cutoff. Scan again before committing.")
        with tempfile.NamedTemporaryFile(
            mode="w", encoding="utf-8", dir=state_path.parent, delete=False
        ) as temp_file:
            temp_path = Path(temp_file.name)
            try:
                json.dump({"cutoff_ns": started_at_ns}, temp_file)
                temp_file.write("\n")
                temp_file.flush()
                os.fsync(temp_file.fileno())
                os.replace(temp_path, state_path)
            finally:
                temp_path.unlink(missing_ok=True)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("records", type=Path)
    parser.add_argument("notion_root_id", type=UUID)
    commands = parser.add_subparsers(dest="command", required=True)
    commands.add_parser("scan")
    commit_parser = commands.add_parser("commit")
    commit_parser.add_argument("started_at_ns", type=int)
    commit_parser.add_argument("previous_cutoff_ns", type=int)
    args = parser.parse_args()

    state_path = args.records / f".notion-sync-{args.notion_root_id.hex}.json"
    try:
        if args.command == "scan":
            scan(args.records, state_path)
        else:
            commit(state_path, args.started_at_ns, args.previous_cutoff_ns)
    except (OSError, ValueError, KeyError, TypeError) as error:
        parser.exit(1, f"{error}\n")


if __name__ == "__main__":
    main()
