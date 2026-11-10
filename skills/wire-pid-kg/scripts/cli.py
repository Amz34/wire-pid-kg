#!/usr/bin/env python3
"""Wire-Native PID to Knowledge Graph CLI."""
import sys
import os
import argparse
import sqlite3

base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
if base_dir not in sys.path:
    sys.path.insert(0, base_dir)

from skills.wire_pid_kg.scripts.engine.builder import GraphBuilder
from skills.wire_pid_kg.scripts.engine.qa_auditor import PIDGoldfishReviewer

def main():
    parser = argparse.ArgumentParser(description="Wire-Native P&ID to Knowledge Graph CLI")
    subparsers = parser.add_subparsers(dest="command")

    build_parser = subparsers.add_parser("build", help="Build knowledge graph from process description or data")
    build_parser.add_argument("--plant", default="Chemical-Refinery-Unit-01", help="Plant identifier")
    build_parser.add_argument("--outdir", default="work/sample_plant", help="Output directory")

    query_parser = subparsers.add_parser("query", help="Query knowledge graph via SQL")
    query_parser.add_argument("--db", default="work/sample_plant/graph.db", help="SQL database file")
    query_parser.add_argument("--sql", required=True, help="SQL query to execute")

    args = parser.parse_args()
    if not args.command:
        parser.print_help()
        sys.exit(1)

    if args.command == "build":
        os.makedirs(args.outdir, exist_ok=True)
        print(f"\n⚙️ [Wire-PID-KG] Building Process Knowledge Graph for '{args.plant}'...")
        builder = GraphBuilder(plant_name=args.plant)

        # Standard Process Demonstration Flow: Feed Tank -> Pump -> Reactor -> Stripper
        builder.add_equipment("TK-101", "Feed Surge Tank", "tank", "DEXPI.Vessel")
        builder.add_equipment("P-101A", "Centrifugal Feed Pump", "pump", "DEXPI.CentrifugalPump")
        builder.add_equipment("R-201", "Continuous Stirred-Tank Reactor", "reactor", "DEXPI.Reactor")
        builder.add_equipment("C-301", "Depropanizer Stripping Column", "column", "DEXPI.DistillationColumn")

        builder.add_instrument("FT-101") # Flow Transmitter
        builder.add_instrument("FIC-101") # Flow Indicating Controller
        builder.add_instrument("PT-201") # Pressure Transmitter
        builder.add_instrument("TC-201") # Temperature Controller

        builder.add_valve("FCV-101", "control_valve", "FC")
        builder.add_valve("XV-201", "isolation_valve", "FO")

        builder.add_connection("TK-101", "P-101A", "suction_line", "6-inch-CS")
        builder.add_connection("P-101A", "FCV-101", "discharge_line", "4-inch-CS")
        builder.add_connection("FCV-101", "R-201", "reactor_feed", "4-inch-CS")
        builder.add_connection("R-201", "C-301", "stripper_feed", "4-inch-SS")

        # Zero-Context Goldfish Review
        print("🐟 [Goldfish QA Swarm] Executing zero-context graph integrity audit...")
        auditor = PIDGoldfishReviewer()
        qa_res = auditor.audit(builder.pkg)
        status = "PASSED" if qa_res["passed"] else "REVIEW NEEDED"
        print(f"   [{qa_res['auditor']}] Status: {status} (Score: {qa_res['score']}/100)")
        for w in qa_res["warnings"]:
            print(f"      • {w}")

        json_path = os.path.join(args.outdir, "graph.json")
        db_path = os.path.join(args.outdir, "graph.db")
        summary_path = os.path.join(args.outdir, "summary.md")

        builder.export_json(json_path)
        builder.export_sql_db(db_path)
        with open(summary_path, "w", encoding="utf-8") as f:
            f.write(builder.generate_markdown_summary())

        print(f"\n✅ [Build Complete]")
        print(f"   • Graph JSON:    {json_path}")
        print(f"   • SQL Store:     {db_path}")
        print(f"   • LLM Context:   {summary_path}\n")

    elif args.command == "query":
        print(f"\n🔍 [SQL Query] Executing: {args.sql}")
        con = sqlite3.connect(args.db)
        cur = con.cursor()
        cur.execute(args.sql)
        cols = [d[0] for d in cur.description] if cur.description else []
        rows = cur.fetchall()
        print(f"Columns: {cols}")
        for r in rows:
            print(f"  {r}")
        con.close()

if __name__ == "__main__":
    main()
