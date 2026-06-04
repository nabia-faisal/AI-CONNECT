# AI Connect 2025 — CSP Solver Challenge

> A hybrid symbolic CSP solver for [ZebraLogicBench](https://huggingface.co/datasets/allenai/ZebraLogicBench) logic grid puzzles.  
> Built for the AI Connect 2025 international student competition (HSBI · TDU · SEECS/NUST · CST/RUB).

---

## What This Project Does

This solver tackles Zebra-style logic grid puzzles by modelling them as Constraint Satisfaction Problems (CSPs). Given a set of houses, attributes, and natural-language clues, it finds the unique assignment that satisfies all constraints.

**Key techniques implemented:**

- **Backtracking Search** — systematic depth-first exploration
- **MRV Heuristic** *(Minimum Remaining Values)* — always branches on the most constrained variable first
- **Forward Checking** — prunes domain values that can no longer lead to a solution after each assignment
- **AC-3 Arc Consistency** — propagates constraints before and during search to shrink domains early
- **Trace Generation** — logs feature vectors at every decision point (for analysis/ML training)

---

## Project Structure

```
AI-CONNECT/
├── run.py                      # Entry point — run solver on a test set
├── requirements.txt
├── .gitignore
│
├── solver/
│   ├── __init__.py
│   └── csp_solver.py           # Core CSP engine (backtracking + MRV + FC + AC-3)
│
├── data/
│   ├── __init__.py
│   └── data_loader.py          # Loads ZebraLogicBench; parses puzzles into CSP format
│
├── traces/
│   ├── __init__.py
│   ├── trace_generator.py      # Wraps solver to emit per-step feature vectors
│   └── output/                 # Saved trace JSON files (git-ignored)
│
├── evaluation/
│   ├── __init__.py
│   └── evaluate.py             # Accuracy, avg steps, composite score
│
└── report/                     # Final report and presentation materials
```

---

## Quickstart

### 1. Install dependencies

```bash
pip install -r requirements.txt
```

### 2. Run on test puzzles

```bash
python run.py --data path/to/test_puzzles.jsonl --out results.json
```

### 3. Evaluate on a validation set

```bash
python evaluation/evaluate.py --data path/to/val.jsonl --max 100 --out results.json
```

### 4. Generate solver traces

```python
from traces.trace_generator import TraceGenerator
from data.data_loader import puzzle_to_csp

gen = TraceGenerator()
variables, domains, constraints = puzzle_to_csp(my_puzzle)
gen.solve(variables, domains, constraints)
gen.save_trace("puzzle_001")
```

---

## Dataset

**ZebraLogicBench** — ~1,000 logic grid puzzles with varying sizes and clue sets.  
Source: [allenai/ZebraLogicBench on HuggingFace](https://huggingface.co/datasets/allenai/ZebraLogicBench)

Each puzzle contains:
- List of entities (people, pets, colours, etc.)
- Clues in natural language
- Ground-truth solution
- Structured JSON representation

---

## Evaluation Metric

The competition uses a **composite score** that rewards both correctness and speed:

```
Composite Score = Accuracy (%) − α × (AvgSteps / MaxAvgSteps)
```

Where `α = 10` is the efficiency penalty weight set by the competition organisers.

| Metric | Description |
|--------|-------------|
| Accuracy (%) | % of puzzles with a fully correct solution |
| AvgSteps | Average CSP search steps per puzzle |
| MaxAvgSteps | Highest AvgSteps across all competing teams |

---

## Submission Files

Per competition requirements, the submission zip must contain:

| File | Description |
|------|-------------|
| `run.py` | Script to run the solver on test puzzles |
| `solver/csp_solver.py` | Core hybrid solver |
| `results.json` | Output for the held-out test set |
| `README.md` | This file |

---

## Competition Timeline

| Week | Milestone |
|------|-----------|
| 1 | Set up CSP solver & data loader; parse puzzles into CSP format |
| 1 | Generate solver traces (search states + decisions) |
| 2 | Evaluate on validation set |
| 2 | Final evaluation on held-out test puzzles (Kaggle); report + video submission (LMS) |

---

## Team

Built as part of **AI Connect 2025** — a collaborative, student-centred project week co-hosted by universities across Germany, Türkiye, Pakistan, and Bhutan.
