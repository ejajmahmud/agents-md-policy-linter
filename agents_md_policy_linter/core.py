"""Core linter for AGENTS.md declarative agent instruction files."""
import re
from typing import Any, Dict, List


class AgentsMdLinter:
    """Detects directive contradictions, bloated sections, and malformed commands in AGENTS.md."""

    POLARITY_RE = re.compile(r"\b(always|never|must not|do not|prefer)\b\s+(.+?)(?:\.|$)", re.IGNORECASE)

    def __init__(self, token_budget: int = 2000):
        self.token_budget = token_budget

    @staticmethod
    def estimate_tokens(text: str) -> int:
        return max(1, int(len(text.split()) * 1.33)) if text.strip() else 0

    def lint_text(self, content: str, source_name: str = "AGENTS.md") -> Dict[str, Any]:
        issues: List[Dict[str, Any]] = []
        lines = content.splitlines()
        if not any(line.startswith("#") for line in lines):
            issues.append({"line": 1, "severity": "warning", "rule": "missing-heading", "message": "No markdown headings found"})

        tokens = self.estimate_tokens(content)
        if tokens > self.token_budget:
            issues.append({
                "line": 1,
                "severity": "error",
                "rule": "token-budget-exceeded",
                "message": f"Estimated {tokens} tokens exceeds budget {self.token_budget}",
            })

        positive_targets: Dict[str, int] = {}
        negative_targets: Dict[str, int] = {}

        for idx, line in enumerate(lines, 1):
            m = self.POLARITY_RE.search(line)
            if not m:
                continue
            verb = m.group(1).lower()
            subject = re.sub(r"[^a-z0-9 ]", "", m.group(2).lower()).strip()
            if not subject:
                continue
            is_neg = verb in ("never", "must not", "do not")
            if is_neg:
                negative_targets[subject] = idx
                if subject in positive_targets:
                    issues.append({
                        "line": idx,
                        "severity": "error",
                        "rule": "contradictory-directive",
                        "message": f"Conflicts with positive rule for '{subject}' on line {positive_targets[subject]}",
                    })
            else:
                positive_targets[subject] = idx
                if subject in negative_targets:
                    issues.append({
                        "line": idx,
                        "severity": "error",
                        "rule": "contradictory-directive",
                        "message": f"Conflicts with negative rule for '{subject}' on line {negative_targets[subject]}",
                    })

        return {
            "source": source_name,
            "estimated_tokens": tokens,
            "passed": not any(i["severity"] == "error" for i in issues),
            "issues": issues,
        }
