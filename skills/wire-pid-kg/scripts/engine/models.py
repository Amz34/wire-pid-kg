"""Data Models for Wire-Native Process Knowledge Graph."""
from typing import List, Dict, Any, Optional
from pydantic import BaseModel, Field

class EquipmentNode(BaseModel):
    id: str = Field(..., description="Unique equipment tag, e.g., P-101A")
    name: str = Field(..., description="Equipment name, e.g., Centrifugal Slurry Pump")
    equipment_type: str = Field(..., description="E.g., pump, tank, heat_exchanger, column")
    dexpi_class: Optional[str] = None
    sheet_ref: str = Field(default="Sheet-01")
    confidence: float = Field(default=1.0)

class InstrumentNode(BaseModel):
    tag: str = Field(..., description="ISA-5.1 tag, e.g., FT-101, PT-204")
    measured_variable: str = Field(..., description="Flow, Pressure, Temperature, Level")
    function: str = Field(..., description="Transmitter, Controller, Indicator, Switch")
    loop_id: Optional[str] = None
    sheet_ref: str = Field(default="Sheet-01")
    confidence: float = Field(default=1.0)

class ValveNode(BaseModel):
    id: str = Field(..., description="Valve identifier, e.g., XV-101, FCV-202")
    valve_type: str = Field(default="control_valve", description="control_valve, check_valve, gate_valve")
    fail_state: Optional[str] = "FC" # FC (Fail Closed), FO (Fail Open)
    sheet_ref: str = Field(default="Sheet-01")

class ProcessEdge(BaseModel):
    source: str
    target: str
    edge_type: str = Field(default="process_pipe", description="process_pipe, instrument_line, electrical_signal")
    line_spec: Optional[str] = None
    flow_direction: str = Field(default="forward")
    sheet_ref: str = Field(default="Sheet-01")

class ProcessKnowledgeGraph(BaseModel):
    plant_name: str
    version: str = "1.0.0"
    equipment: List[EquipmentNode] = []
    instruments: List[InstrumentNode] = []
    valves: List[ValveNode] = []
    connections: List[ProcessEdge] = []
