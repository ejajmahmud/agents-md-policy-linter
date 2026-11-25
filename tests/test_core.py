"""Tests for AGENTS.md Policy Linter."""
import unittest
from agents_md_policy_linter.core import AgentsMdLinter


class TestAgentsMdLinter(unittest.TestCase):
    def test_clean_policy_passes(self):
        linter = AgentsMdLinter(token_budget=500)
        res = linter.lint_text("# Repo Guide\nAlways run unit tests.\nNever commit secrets.\n")
        self.assertTrue(res["passed"])
        self.assertEqual(res["issues"], [])

    def test_detects_contradiction(self):
        linter = AgentsMdLinter()
        res = linter.lint_text("# Rules\nAlways use poetry.\nNever use poetry.\n")
        self.assertFalse(res["passed"])
        self.assertEqual(res["issues"][0]["rule"], "contradictory-directive")

    def test_enforces_token_budget(self):
        linter = AgentsMdLinter(token_budget=5)
        res = linter.lint_text("# Title\nThis text clearly has way more than five estimated tokens.")
        self.assertFalse(res["passed"])
        self.assertEqual(res["issues"][0]["rule"], "token-budget-exceeded")
