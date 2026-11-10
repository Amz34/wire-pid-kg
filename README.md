# Wire-PID-KG: Wire-Native P&ID to Process Knowledge Graph

[![Engine: Wire--Native](https://img.shields.io/badge/Engine-Wire--Native-00e5ff.svg)](https://github.com/Amz34)
[![Standard: ISA--5.1](https://img.shields.io/badge/Standard-ISA--5.1-f59e0b.svg)](https://github.com/Amz34)
[![Storage: DuckDB](https://img.shields.io/badge/Store-DuckDB-FFF000.svg)](https://github.com/Amz34)
[![License: MIT](https://img.shields.io/badge/License-MIT-purple.svg)](LICENSE)

An enterprise-grade, wire-native intelligence engine and agentic skill that turns Piping & Instrumentation Diagrams (P&IDs) and Process Flow Diagrams (PFDs)—both digital vector CAD and scanned drawings—into a structured, queryable process knowledge graph.

The graph captures:
- **Process Flow:** Upstream and downstream connectivity across tanks, pumps, reactors, heat exchangers, distillation columns, and pipe segments.
- **Measurement:** Transmitters, indicators, and sensors positioned accurately within process streams.
- **Control Loops:** Complete loops traced from sensor element through controller to final actuator or drive, adhering to ISA-5.1 standards.

---

## Architecture Overview

```
wire-pid-kg/
├── .claude-plugin/
│   └── plugin.json
├── docs/
│   └── how-it-works.svg
├── skills/
│   └── wire-pid-kg/
│       ├── SKILL.md
│       ├── references/
│       │   ├── extraction_procedure.md
│       │   ├── isa_5_1.md
│       │   ├── ontology.md
│       │   ├── symbol_guide.md
│       │   └── schema/
│       │       ├── extraction.schema.json
│       │       └── graph.schema.json
│       └── scripts/
│           ├── requirements.txt
│           ├── probe_pdf.py
│           ├── render_pages.py
│           ├── make_hints.py
│           ├── build_kg.py
│           ├── kg_query.py
│           ├── export.py
│           ├── eval_kg.py
│           ├── crop.py
│           └── pidkg/
│               ├── build.py
│               ├── isa.py
│               ├── loops.py
│               ├── models.py
│               ├── ocr.py
│               ├── ontology.py
│               ├── pdf.py
│               ├── qa.py
│               ├── store.py
│               └── summary.py
└── tests/
    ├── conftest.py
    └── fixtures/
```

---

## Workflow Pipeline

1. **Page Classification (`probe_pdf.py`)**: Identifies CAD vector text vs. raster scans and establishes extraction paths.
2. **Page Rendering (`render_pages.py`)**: Generates high-resolution coordinate tiles for agent inspection.
3. **Orientation & Hints (`make_hints.py`)**: Gathers OCR bounding box hints for tag validation.
4. **Agent Inspection (`SKILL.md`)**: Inspects drawings and writes structured JSON extractions per sheet.
5. **Graph Assembly (`build_kg.py`)**: Stitches line segments, connects off-page links, and assembles control loops.
6. **QA Audit (`qa.py`)**: Validates against floating equipment, open loops, and unverified tags.
7. **Analytical Querying (`kg_query.py`)**: Queries the embedded DuckDB store for upstream and downstream process tracing.

---

## Outputs

- `graph.json`: Full validated JSON graph conforming to `graph.schema.json`.
- `graph.duckdb`: Analytical SQL database for recursive graph searches.
- `summary.md`: Clean Markdown context layer for LLM reasoning.
- `qa_report.md`: Discrepancy report detailing unresolved tags or unlinked connectors.

---

## Automated Verification

```bash
pytest
```

---

## License

MIT © [Amz34](https://github.com/Amz34).
