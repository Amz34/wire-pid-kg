"""Comprehensive Unit Tests for wire-pid-kg."""
import unittest
import os
import sys
import tempfile
import sqlite3

base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if base_dir not in sys.path:
    sys.path.insert(0, base_dir)

from skills.wire_pid_kg.scripts.engine.isa import ISAParser
from skills.wire_pid_kg.scripts.engine.builder import GraphBuilder
from skills.wire_pid_kg.scripts.engine.qa_auditor import PIDGoldfishReviewer

class TestWirePIDKnowledgeGraph(unittest.TestCase):

    def test_isa_tag_parsing(self):
        flow_tag = ISAParser.parse_tag("FT-101")
        self.assertEqual(flow_tag["measured_variable"], "Flow Rate")
        self.assertEqual(flow_tag["function"], "Transmitter")
        self.assertEqual(flow_tag["loop_number"], "101")

        temp_tag = ISAParser.parse_tag("TIC-204A")
        self.assertEqual(temp_tag["measured_variable"], "Temperature")
        self.assertIn("Controller", temp_tag["function"])

    def test_graph_builder_and_sql_export(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            builder = GraphBuilder(plant_name="Test-Refinery")
            builder.add_equipment("TK-10", "Surge Tank", "tank")
            builder.add_equipment("P-10", "Pump", "pump")
            builder.add_instrument("PT-10")
            builder.add_connection("TK-10", "P-10")

            json_path = os.path.join(tmpdir, "graph.json")
            db_path = os.path.join(tmpdir, "graph.db")

            builder.export_json(json_path)
            builder.export_sql_db(db_path)

            self.assertTrue(os.path.exists(json_path))
            self.assertTrue(os.path.exists(db_path))

            # Query SQL Store
            con = sqlite3.connect(db_path)
            cur = con.cursor()
            res = cur.execute("SELECT count(*) FROM equipment").fetchone()[0]
            self.assertEqual(res, 2)
            con.close()

    def test_goldfish_qa_auditor(self):
        builder = GraphBuilder("Unconnected-Plant")
        builder.add_equipment("TK-1", "Tank 1", "tank")
        builder.add_equipment("TK-2", "Floating Tank", "tank")
        # No connections
        auditor = PIDGoldfishReviewer()
        qa_res = auditor.audit(builder.pkg)
        self.assertGreater(len(qa_res["warnings"]), 0)
        self.assertTrue(any("Unconnected equipment" in w for w in qa_res["warnings"]))

if __name__ == "__main__":
    unittest.main()
