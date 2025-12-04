import argparse
import logging
import sys
from pathlib import Path
from typing import List

#!/usr/bin/env python3
"""
Basic Python script template.

Features:
- Simple CLI with argparse
- Logging setup
- Example functions: greet, add_numbers, read_file
"""



def setup_logging(level: int = logging.INFO) -> None:
    logging.basicConfig(
        level=level,
        format="%(asctime)s - %(levelname)s - %(message)s",
    )


def greet(name: str, repeat: int = 1) -> None:
    """Print a greeting message repeat times."""
    for _ in range(max(1, repeat)):
        print(f"Hello, {name}!")


def add_numbers(numbers: List[float]) -> float:
    """Return the sum of a list of numbers."""
    return sum(numbers)


def read_file(path: str, max_lines: int = 10) -> None:
    """Print up to max_lines from file at path."""
    p = Path(path)
    if not p.exists():
        logging.error("File not found: %s", path)
        return
    try:
        with p.open("r", encoding="utf-8") as f:
            for i, line in enumerate(f):
                if i >= max_lines:
                    break
                print(line.rstrip("\n"))
    except Exception as e:
        logging.exception("Failed reading file: %s", e)


def parse_args(argv: List[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Basic example Python script.")
    parser.add_argument("--name", "-n", default="World", help="Name to greet")
    parser.add_argument("--repeat", "-r", type=int, default=1, help="How many times to repeat the greeting")
    parser.add_argument("--numbers", "-s", nargs="*", type=float, help="Numbers to sum (space separated)")
    parser.add_argument("--file", "-f", help="Path to a text file to print partial contents")
    parser.add_argument("--verbose", "-v", action="store_true", help="Enable debug logging")
    return parser.parse_args(argv)


def main(argv: List[str]) -> int:
    args = parse_args(argv)
    setup_logging(logging.DEBUG if args.verbose else logging.INFO)

    greet(args.name, args.repeat)

    if args.numbers:
        total = add_numbers(args.numbers)
        print(f"Sum of numbers: {total}")

    if args.file:
        read_file(args.file)

    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))