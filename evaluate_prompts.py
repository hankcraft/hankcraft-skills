#!/usr/bin/env python3
"""
CLI Agent System Prompt Evaluation Harness
Evaluates system prompt performance across two key dimensions:
1. Outcome Accuracy: Functional test success rate (pytest/npm test)
2. Trajectory Quality: Tool usage efficiency, rule adherence, and diff surgicality
"""

import json
import argparse
import subprocess
from pathlib import Path
from typing import Dict, List, Any

def audit_trajectory(transcript_path: Path) -> Dict[str, Any]:
    """Audits agent JSONL transcript for tool call patterns and compliance rules."""
    if not transcript_path.exists():
        return {"step_count": 0, "violations": ["Missing transcript log"]}

    steps = []
    read_files = set()
    violations = []

    with open(transcript_path, "r", encoding="utf-8") as f:
        for line in f:
            if not line.strip():
                continue
            data = json.loads(line)
            steps.append(data)
            
            # Extract tool call actions
            tool_calls = data.get("tool_calls", [])
            for call in tool_calls:
                name = call.get("name")
                args = call.get("args", {})
                
                if name in ["view_file", "grep_search", "read_url_content"]:
                    path = args.get("AbsolutePath") or args.get("SearchPath")
                    if path:
                        read_files.add(path)
                elif name in ["replace_file_content", "multi_replace_file_content", "write_to_file"]:
                    target = args.get("TargetFile")
                    if target and target not in read_files:
                        violations.append(f"Rule Violation: Edited '{target}' without prior inspection.")

    return {
        "step_count": len(steps),
        "violations": violations,
        "read_count": len(read_files)
    }

def check_diff(workspace_dir: Path) -> int:
    """Returns number of modified/added/deleted lines in git diff."""
    res = subprocess.run(
        ["git", "diff", "--shortstat"],
        cwd=workspace_dir,
        capture_output=True,
        text=True
    )
    # Parse shortstat output e.g. "2 files changed, 10 insertions(+), 3 deletions(-)"
    output = res.stdout.strip()
    if not output:
        return 0
    total_changes = 0
    for part in output.split(","):
        part = part.strip()
        if "insertion" in part or "deletion" in part:
            num = int(part.split()[0])
            total_changes += num
    return total_changes

def evaluate_variant(task: Dict[str, Any], prompt_path: Path, variant_name: str, workspace: Path) -> Dict[str, Any]:
    """Runs a single evaluation iteration of a task with a given system prompt variant."""
    transcript_path = workspace / f"transcript_{variant_name}.jsonl"

    print(f"[{variant_name}] Evaluating Task: {task['id']}...")
    
    # Run test verification command
    test_res = subprocess.run(
        task["test_command"],
        shell=True,
        cwd=workspace,
        capture_output=True,
        text=True
    )
    passed = test_res.returncode == 0
    diff_lines = check_diff(workspace)
    trajectory_stats = audit_trajectory(transcript_path)

    return {
        "task_id": task["id"],
        "variant": variant_name,
        "passed": passed,
        "diff_lines": diff_lines,
        "step_count": trajectory_stats["step_count"],
        "violations": trajectory_stats["violations"]
    }

def main():
    parser = argparse.ArgumentParser(description="CLI Agent System Prompt Evaluator")
    parser.add_argument("--prompt-a", type=Path, help="Path to baseline system prompt")
    parser.add_argument("--prompt-b", type=Path, help="Path to candidate system prompt")
    parser.add_argument("--workspace", type=Path, default=Path("."), help="Target workspace path")
    args = parser.parse_args()

    print("System Prompt Evaluation Harness Ready.")

if __name__ == "__main__":
    main()
