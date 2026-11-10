"""Knowledge Graph Builder and SQLite/DuckDB/JSON Exporter."""
import json
import sqlite3
from typing import Dict, Any, List
from skills.wire_pid_kg.scripts.engine.models import (
    ProcessKnowledgeGraph, EquipmentNode, InstrumentNode, ValveNode, ProcessEdge
)
from skills.wire_pid_kg.scripts.engine.isa import ISAParser

class GraphBuilder:
    def __init__(self, plant_name: str = "Enterprise-Plant-1"):
        self.plant_name = plant_name
        self.pkg = ProcessKnowledgeGraph(plant_name=plant_name)

    def add_equipment(self, eq_id: str, name: str, eq_type: str, dexpi_class: str = "", sheet_ref: str = "Sheet-01"):
        node = EquipmentNode(
            id=eq_id,
            name=name,
            equipment_type=eq_type,
            dexpi_class=dexpi_class or f"DEXPI.{eq_type.title()}",
            sheet_ref=sheet_ref
        )
        self.pkg.equipment.append(node)

    def add_instrument(self, tag: str, sheet_ref: str = "Sheet-01"):
        parsed = ISAParser.parse_tag(tag)
        inst = InstrumentNode(
            tag=tag,
            measured_variable=parsed["measured_variable"],
            function=parsed["function"],
            loop_id=f"Loop-{parsed['loop_number']}",
            sheet_ref=sheet_ref
        )
        self.pkg.instruments.append(inst)

    def add_valve(self, valve_id: str, valve_type: str = "control_valve", fail_state: str = "FC", sheet_ref: str = "Sheet-01"):
        valve = ValveNode(
            id=valve_id,
            valve_type=valve_type,
            fail_state=fail_state,
            sheet_ref=sheet_ref
        )
        self.pkg.valves.append(valve)

    def add_connection(self, source: str, target: str, edge_type: str = "process_pipe", line_spec: str = "4-inch-CS"):
        edge = ProcessEdge(
            source=source,
            target=target,
            edge_type=edge_type,
            line_spec=line_spec
        )
        self.pkg.connections.append(edge)

    def export_json(self, filepath: str):
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(self.pkg.model_dump_json(indent=2))

    def export_sql_db(self, db_filepath: str):
        """Exports relational tables to SQLite (compatible with DuckDB and standard SQL engines)."""
        con = sqlite3.connect(db_filepath)
        cur = con.cursor()
        
        cur.execute("DROP TABLE IF EXISTS equipment")
        cur.execute("CREATE TABLE equipment (id TEXT, name TEXT, equipment_type TEXT, dexpi_class TEXT, sheet_ref TEXT)")
        
        cur.execute("DROP TABLE IF EXISTS instruments")
        cur.execute("CREATE TABLE instruments (tag TEXT, measured_variable TEXT, function TEXT, loop_id TEXT, sheet_ref TEXT)")
        
        cur.execute("DROP TABLE IF EXISTS valves")
        cur.execute("CREATE TABLE valves (id TEXT, valve_type TEXT, fail_state TEXT, sheet_ref TEXT)")
        
        cur.execute("DROP TABLE IF EXISTS connections")
        cur.execute("CREATE TABLE connections (source TEXT, target TEXT, edge_type TEXT, line_spec TEXT, flow_direction TEXT)")

        for eq in self.pkg.equipment:
            cur.execute("INSERT INTO equipment VALUES (?, ?, ?, ?, ?)", (eq.id, eq.name, eq.equipment_type, eq.dexpi_class, eq.sheet_ref))

        for inst in self.pkg.instruments:
            cur.execute("INSERT INTO instruments VALUES (?, ?, ?, ?, ?)", (inst.tag, inst.measured_variable, inst.function, inst.loop_id, inst.sheet_ref))

        for v in self.pkg.valves:
            cur.execute("INSERT INTO valves VALUES (?, ?, ?, ?)", (v.id, v.valve_type, v.fail_state, v.sheet_ref))

        for conn in self.pkg.connections:
            cur.execute("INSERT INTO connections VALUES (?, ?, ?, ?, ?)", (conn.source, conn.target, conn.edge_type, conn.line_spec, conn.flow_direction))

        con.commit()
        con.close()

    def generate_markdown_summary(self) -> str:
        lines = [
            f"# Process Knowledge Graph Summary: {self.plant_name}",
            "",
            "## Equipment Inventory",
            "| Tag | Equipment Name | Type | DEXPI Class |",
            "| :--- | :--- | :--- | :--- |"
        ]
        for eq in self.pkg.equipment:
            lines.append(f"| `{eq.id}` | {eq.name} | {eq.equipment_type} | {eq.dexpi_class} |")

        lines.extend([
            "",
            "## Instrumentation & Control Loops",
            "| Tag | Variable | Function | Control Loop |",
            "| :--- | :--- | :--- | :--- |"
        ])
        for inst in self.pkg.instruments:
            lines.append(f"| `{inst.tag}` | {inst.measured_variable} | {inst.function} | `{inst.loop_id}` |")

        lines.extend([
            "",
            "## Flow Paths & Interconnects",
            "| From | To | Edge Type | Spec |",
            "| :--- | :--- | :--- | :--- |"
        ])
        for conn in self.pkg.connections:
            lines.append(f"| `{conn.source}` | `{conn.target}` | {conn.edge_type} | {conn.line_spec} |")

        return "\n".join(lines)
