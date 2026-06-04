"""
Evaluation Script
Composite Score = Accuracy(%) - alpha * (AvgSteps / MaxAvgSteps)
"""
import json
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))
from data.data_loader import load_dataset, puzzle_to_csp
from solver.csp_solver import CSPSolver

ALPHA = 10  # per competition spec


def evaluate(dataset_path=None, max_puzzles=None):
    puzzles = load_dataset(dataset_path)
    if max_puzzles:
        puzzles = puzzles[:max_puzzles]

    solver = CSPSolver()
    correct, total_steps, results = 0, 0, {}

    for puzzle in puzzles:
        pid = puzzle.get("id", f"puzzle_{len(results)+1:03d}")
        variables, domains, constraints = puzzle_to_csp(puzzle)
        solution = solver.solve(variables, domains, constraints)
        total_steps += solver.steps
        if solution and solution == puzzle.get("solution"):
            correct += 1
        results[pid] = solution or {}

    n = len(puzzles)
    return {
        "accuracy": round(correct / n * 100, 2) if n else 0,
        "avg_steps": round(total_steps / n, 2) if n else 0,
        "num_puzzles": n,
        "results": results,
    }


def composite_score(accuracy, avg_steps, max_avg_steps):
    return round(accuracy - ALPHA * (avg_steps / max_avg_steps), 4)


if __name__ == "__main__":
    import argparse
    p = argparse.ArgumentParser()
    p.add_argument("--data", default=None)
    p.add_argument("--max", type=int, default=50)
    p.add_argument("--out", default="results.json")
    args = p.parse_args()
    m = evaluate(args.data, args.max)
    print(f"Accuracy: {m['accuracy']}%  |  Avg Steps: {m['avg_steps']}")
    with open(args.out, "w") as f:
        json.dump(m["results"], f, indent=2)
    print(f"Results saved to {args.out}")
