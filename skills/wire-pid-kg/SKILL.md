---
name: wire-pid-kg
description: Converts piping and instrumentation diagrams (P&IDs) and process flow diagrams (PFDs) into a structured process knowledge graph with ISA-5.1 tag decomposition, upstream/downstream flow tracing, and DuckDB SQL queryability. Triggers when the user asks to digitize, extract, build a knowledge graph, or query process equipment, control loops, or sensor locations.
---

# Wire-Native P&ID to Knowledge Graph Skill

Encodes enterprise chemical process and instrumentation knowledge into a queryable graph. Built for deep LLM reasoning and zero-hallucination industrial workflows.

## Features
- **ISA-5.1 Decomposition**: Automatically separates measured variables (Flow, Pressure, Temp, Level) and output functions (Transmitters, Controllers, Alarms, Valves).
- **Process Connectivity**: Full topological graph of upstream and downstream equipment.
- **Embedded SQL Store**: Exports to DuckDB for zero-dependency analytical querying.
- **Zero-Context Goldfish Audit**: Built-in automated checks for floating nodes, missing control loops, and unverified connections.
