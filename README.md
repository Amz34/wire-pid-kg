# Wire-PID-KG: Wire-Native Process & Instrumentation Knowledge Graph Engine

[![Engine: Wire--Native](https://img.shields.io/badge/Engine-Wire--Native-00e5ff.svg)](https://github.com/Amz34)
[![Architecture: EGM](https://img.shields.io/badge/Architecture-EGM--Swarm-10b981.svg)](https://github.com/Amz34)
[![License: MIT](https://img.shields.io/badge/License-MIT-purple.svg)](LICENSE)
[![ISA-5.1: Compliant](https://img.shields.io/badge/Standard-ISA--5.1-f59e0b.svg)](https://github.com/Amz34)

An enterprise-grade, wire-native intelligence engine that transforms **Piping & Instrumentation Diagrams (P&IDs)** and Process Flow Diagrams (PFDs) into a queryable, connected process knowledge graph for autonomous LLM reasoning.

Designed with **Elephant-Goldfish Multi-Agent Review**: deep-context extraction synthesized by an Elephant orchestrator, then stress-tested by zero-context Goldfish QA reviewers to eliminate hallucinations.

---

## Capabilities & Architecture

- **ISA-5.1 Decomposition**: Automatically parses tags (`FT`, `PT`, `FIC`, `TIC`, `XV`, etc.) into variables (Flow, Pressure, Temperature, Level) and functions (Transmitter, Controller, Alarm, Final Valve).
- **Process Topology**: Full upstream and downstream tracking across vessels, pumps, reactors, and distillation columns.
- **Embedded SQL & JSON Store**: Native relational tables (`equipment`, `instruments`, `valves`, `connections`) queryable with SQLite and DuckDB.
- **Zero-Context Goldfish Swarm**: Validates graphs against floating nodes, unlinked loops, and flow mismatches.
- **LLM Context Synthesis**: Generates ready-to-ingest markdown summaries for retrieval-augmented generation and reasoning.

---

## Quickstart

### 1. Build Process Knowledge Graph
```bash
./skills/wire-pid-kg/scripts/cli.py build \
  --plant "AONE-BioChemical-Unit-01" \
  --outdir work/sample_plant
```

Outputs:
- `work/sample_plant/graph.json`: Full JSON representation.
- `work/sample_plant/graph.db`: Queryable SQL database.
- `work/sample_plant/summary.md`: LLM context layer.

### 2. Analytical SQL Queries
```bash
# Query all equipment upstream or downstream
./skills/wire-pid-kg/scripts/cli.py query \
  --db work/sample_plant/graph.db \
  --sql "SELECT id, name, equipment_type FROM equipment"
```

```bash
# Query active instrumentation and control loops
./skills/wire-pid-kg/scripts/cli.py query \
  --db work/sample_plant/graph.db \
  --sql "SELECT tag, measured_variable, function, loop_id FROM instruments"
```

---

## Running Automated Tests

```bash
python3 -m unittest discover tests
```

---

## License

MIT © [Amz34](https://github.com/Amz34).
