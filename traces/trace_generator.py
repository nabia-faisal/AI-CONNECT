"""
Trace Generator — wraps CSPSolver to log feature vectors at each decision.
"""
import json
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))
from solver.csp_solver import CSPSolver


class TraceGenerator(CSPSolver):
    def __init__(self):
        super().__init__()
        self.trace = []

    def solve(self, variables, domains, constraints):
        self.trace = []
        return super().solve(variables, domains, constraints)

    def _backtrack(self, assignment, variables, domains, constraints):
        if len(assignment) == len(variables):
            return assignment
        var = self._select_unassigned_variable(assignment, variables, domains)
        for value in list(domains[var]):
            self.steps += 1
            self.trace.append({
                "step": self.steps,
                "variable": var,
                "value": value,
                "assignment_size": len(assignment),
                "remaining_domain_sizes": {v: len(d) for v, d in domains.items() if v not in assignment},
            })
            if self._is_consistent(var, value, assignment, constraints):
                assignment[var] = value
                saved = {v: list(d) for v, d in domains.items()}
                if self._forward_check(var, value, assignment, domains, constraints):
                    result = self._backtrack(assignment, variables, domains, constraints)
                    if result is not None:
                        return result
                del assignment[var]
                domains.update(saved)
        return None

    def save_trace(self, puzzle_id: str, output_dir: str = "traces/output"):
        Path(output_dir).mkdir(parents=True, exist_ok=True)
        path = Path(output_dir) / f"trace_{puzzle_id}.json"
        with open(path, "w") as f:
            json.dump({"puzzle_id": puzzle_id, "steps": self.steps, "trace": self.trace}, f, indent=2)
        return str(path)
