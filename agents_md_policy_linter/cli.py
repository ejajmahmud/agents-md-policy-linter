"""CLI for AGENTS.md Policy Linter."""
import argparse
import json
from .core import AgentsMdLinter


def main():
    parser = argparse.ArgumentParser(description="AGENTS.md Policy Linter CLI")
    parser.add_argument("--file", help="Path to AGENTS.md file")
    parser.add_argument("--budget", type=int, default=2000, help="Token budget")
    args = parser.parse_args()

    linter = AgentsMdLinter(token_budget=args.budget)
    if args.file:
        with open(args.file, "r", encoding="utf-8") as f:
            text = f.read()
        res = linter.lint_text(text, source_name=args.file)
    else:
        res = linter.lint_text("# Project Guide\nAlways run unittest before commit.\n")
    print(json.dumps(res, indent=2))


if __name__ == "__main__":
    main()
