"""
Hybrid CSP Solver for ZebraLogicBench
Implements: Backtracking + MRV heuristic + Forward Checking + AC-3
"""
from collections import deque


class CSPSolver:
    """Symbolic CSP Solver with MRV, Forward Checking, and Arc Consistency (AC-3)."""

    def __init__(self):
        self.steps = 0

    def solve(self, variables: list, domains: dict, constraints: list):
        """
        Solve a CSP.
        Args:
            variables: list of variable names
            domains: dict mapping variable -> list of possible values
            constraints: list of (var1, var2, check_fn) tuples
        Returns:
            assignment dict or None
        """
        self.steps = 0
        domains_copy = {v: list(d) for v, d in domains.items()}
        return self._backtrack({}, variables, domains_copy, constraints)

    def _backtrack(self, assignment, variables, domains, constraints):
        if len(assignment) == len(variables):
            return assignment
        var = self._select_unassigned_variable(assignment, variables, domains)
        for value in list(domains[var]):
            self.steps += 1
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

    def _select_unassigned_variable(self, assignment, variables, domains):
        """MRV heuristic."""
        return min(
            (v for v in variables if v not in assignment),
            key=lambda v: len(domains[v])
        )

    def _is_consistent(self, var, value, assignment, constraints):
        for (v1, v2, check) in constraints:
            if v1 == var and v2 in assignment:
                if not check(value, assignment[v2]):
                    return False
            if v2 == var and v1 in assignment:
                if not check(assignment[v1], value):
                    return False
        return True

    def _forward_check(self, var, value, assignment, domains, constraints):
        for (v1, v2, check) in constraints:
            if v1 == var and v2 not in assignment:
                domains[v2] = [val for val in domains[v2] if check(value, val)]
                if not domains[v2]:
                    return False
            if v2 == var and v1 not in assignment:
                domains[v1] = [val for val in domains[v1] if check(val, value)]
                if not domains[v1]:
                    return False
        return True

    def arc_consistency(self, domains, constraints):
        """AC-3 preprocessing to reduce domains before search."""
        queue = deque([(v1, v2) for (v1, v2, _) in constraints])
        while queue:
            xi, xj = queue.popleft()
            if self._revise(xi, xj, domains, constraints):
                if not domains[xi]:
                    return False
                for (v1, v2, _) in constraints:
                    if v2 == xi and v1 != xj:
                        queue.append((v1, xi))
        return True

    def _revise(self, xi, xj, domains, constraints):
        revised = False
        checks = [chk for (v1, v2, chk) in constraints if v1 == xi and v2 == xj]
        for x in list(domains[xi]):
            if checks and not any(chk(x, y) for chk in checks for y in domains[xj]):
                domains[xi].remove(x)
                revised = True
        return revised


if __name__ == "__main__":
    variables = ["h1_color", "h2_color", "h3_color"]
    domains = {v: ["red", "blue", "green"] for v in variables}
    constraints = [
        (v1, v2, lambda a, b: a != b)
        for i, v1 in enumerate(variables) for v2 in variables[i+1:]
    ]
    solver = CSPSolver()
    print("Solution:", solver.solve(variables, domains, constraints))
    print("Steps:", solver.steps)
