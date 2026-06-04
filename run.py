#!/usr/bin/env python3
"""
run.py — AI Connect 2025 CSP Solver entry point
Usage: python run.py --data test_puzzles.jsonl --out results.json
"""
import argparse, json
from data.data_loader import load_dataset, puzzle_to_csp
from solver.csp_solver import CSPSolver


def main():
    parser = argparse.ArgumentParser(description="AI Connect 2025 – CSP Solver")
    parser.add_argument("--data", required=True, help="Test puzzles JSONL path")
    parser.add_argument("--out", default="results.json")
    parser.add_argument("--max", type=int, default=None)
    args = parser.parse_args()

    puzzles = load_dataset(args.data)
    if args.max:
        puzzles = puzzles[:args.max]

    solver = CSPSolver()
    results = {}

    for puzzle in puzzles:
        pid = puzzle.get("id", f"puzzle_{len(results)+1:03d}")
        variables, domains, constraints = puzzle_to_csp(puzzle)
        solver.arc_consistency(domains, constraints)
        results[pid] = solver.solve(variables, domains, constraints) or {}

    with open(args.out, "w") as f:
        json.dump(results, f, indent=2)
    print(f"Done. {len(results)} puzzles → {args.out}")


if __name__ == "__main__":
    main()
