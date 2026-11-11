#!/usr/bin/env python3
"""Static security gate for AI agent skills (SKILL.md, references, and scripts)."""

from __future__ import annotations

import json
import re
import sys
from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class SecurityRule:
    rule_id: str
    severity: str
    pattern: re.Pattern[str]
    reason: str


RULES: tuple[SecurityRule, ...] = (
    SecurityRule(
        "SEC001",
        "CRITICAL",
        re.compile(r"ignore\s+(all\s+)?(previous|prior|system)\s+instructions", re.I),
        "Indirect prompt injection override directive",
    ),
    SecurityRule(
        "SEC002",
        "CRITICAL",
        re.compile(r"(curl|wget)\s+[^\n|]+\|\s*(ba)?sh|invoke-expression|\biex\s*\(", re.I),
        "Remote script pipe-to-shell execution",
    ),
    SecurityRule(
        "SEC003",
        "CRITICAL",
        re.compile(r"(\.ssh/id_|authorized_keys|\.aws/credentials|keychain|seed\s*phrase)", re.I),
        "Sensitive credential or key store targeting",
    ),
    SecurityRule(
        "SEC004",
        "HIGH",
        re.compile(r"(silently\s+send|without\s+telling\s+the\s+user|do\s+not\s+inform\s+the\s+user)", re.I),
        "Covert exfiltration or concealment instruction",
    ),
    SecurityRule(
        "SEC005",
        "HIGH",
        re.compile(r"(base64\s+-d|base64\.b64decode|eval\s*\(|exec\s*\().{0,80}(http|curl|socket|subprocess|os\.system)", re.I | re.S),
        "Obfuscated payload execution",
    ),
    SecurityRule(
        "SEC007",
        "MEDIUM",
        re.compile(r"(~/\.|/etc/passwd|/etc/shadow|\.\./\.\./\.\./)", re.I),
        "Out-of-workspace host path access",
    ),
)

CODE_EXTENSIONS = {".py", ".sh", ".ps1", ".js", ".ts"}
SCAN_EXTENSIONS = {".md", ".json", ".yaml", ".yml", *CODE_EXTENSIONS}
ENV_READ_RE = re.compile(r"\b(os\.environ|os\.getenv|process\.env)\b", re.I)
NET_CALL_RE = re.compile(r"\b(requests\.(post|put|get)|urllib\.request|http\.client|socket\.|fetch\(|axios\.)", re.I)


def scan_skill_dir(skill_dir: Path) -> list[dict]:
    """Scan a single skill directory and return structured security findings."""
    findings: list[dict] = []
    for fpath in sorted(skill_dir.rglob("*")):
        if not fpath.is_file() or fpath.suffix.lower() not in SCAN_EXTENSIONS:
            continue
        text = fpath.read_text(encoding="utf-8", errors="replace")
        rel = fpath.relative_to(skill_dir).as_posix()
        is_code = fpath.suffix.lower() in CODE_EXTENSIONS
        for rule in RULES:
            if rule.rule_id == "SEC005" and not is_code:
                continue
            if m := rule.pattern.search(text):
                line_no = text[: m.start()].count("\n") + 1
                findings.append(
                    {
                        "skill": skill_dir.name,
                        "file": rel,
                        "line": line_no,
                        "rule_id": rule.rule_id,
                        "severity": rule.severity,
                        "reason": rule.reason,
                    }
                )
        if is_code and ENV_READ_RE.search(text) and (m_net := NET_CALL_RE.search(text)):
            findings.append(
                {
                    "skill": skill_dir.name,
                    "file": rel,
                    "line": text[: m_net.start()].count("\n") + 1,
                    "rule_id": "SEC006",
                    "severity": "HIGH",
                    "reason": "Environment secret read combined with outbound network call",
                }
            )
    return findings


def scan_skills_root(skills_root: Path) -> dict:
    """Scan every skill under .agents/skills/ and summarize pass/fail status."""
    findings: list[dict] = []
    scanned = 0
    if skills_root.is_dir():
        for entry in sorted(skills_root.iterdir()):
            if entry.is_dir():
                scanned += 1
                findings.extend(scan_skill_dir(entry))
    blocking = [f for f in findings if f["severity"] in {"CRITICAL", "HIGH"}]
    return {
        "scanned_skills": scanned,
        "findings": findings,
        "blocking_count": len(blocking),
        "passed": len(blocking) == 0,
    }


def main() -> int:
    root = Path(__file__).resolve().parent.parent
    skills_root = Path(sys.argv[1]) if len(sys.argv) > 1 else root / ".agents" / "skills"
    report = scan_skills_root(skills_root)
    print(json.dumps(report, ensure_ascii=False, indent=2))
    return 0 if report["passed"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
