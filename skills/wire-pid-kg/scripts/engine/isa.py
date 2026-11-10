"""ISA-5.1 Instrument Tag Parser."""
import re
from typing import Dict, Any, Optional

# Standard ISA-5.1 First Letters (Measured Variables)
FIRST_LETTERS = {
    "F": "Flow Rate",
    "P": "Pressure",
    "T": "Temperature",
    "L": "Level",
    "A": "Analysis",
    "C": "Conductivity",
    "D": "Density",
    "E": "Voltage",
    "H": "Hand / Manual",
    "I": "Current",
    "J": "Power",
    "K": "Time",
    "M": "Moisture",
    "S": "Speed / Frequency",
    "V": "Vibration",
    "W": "Weight / Force",
    "Y": "Event / State",
    "Z": "Position"
}

# Standard ISA-5.1 Succeeding Letters (Readout / Output Functions)
SUCCEEDING_LETTERS = {
    "A": "Alarm",
    "C": "Controller",
    "E": "Sensor / Element",
    "I": "Indicator",
    "R": "Recorder",
    "S": "Switch",
    "T": "Transmitter",
    "V": "Valve / Actuator",
    "Y": "Relay / Compute",
    "Z": "Final Drive"
}

class ISAParser:
    """Parses standard ISA-5.1 tags into variable and function taxonomy."""
    
    @staticmethod
    def parse_tag(tag: str) -> Dict[str, Any]:
        tag = tag.strip().upper()
        match = re.match(r"^([A-Z]+)[-_ ]*(\d+[A-Z0-9]*)$", tag)
        if not match:
            return {
                "tag": tag,
                "measured_variable": "Unknown",
                "function": "Unknown",
                "loop_number": "N/A"
            }
        
        letters, loop_no = match.groups()
        first_letter = letters[0]
        succeeding = letters[1:]

        variable = FIRST_LETTERS.get(first_letter, "Special")
        functions = [SUCCEEDING_LETTERS.get(char, "Modifier") for char in succeeding]
        function_desc = " ".join(functions) if functions else "Sensor"

        return {
            "tag": tag,
            "measured_variable": variable,
            "function": function_desc,
            "loop_number": loop_no
        }
