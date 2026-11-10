# Process Knowledge Graph Summary: AONE-BioChemical-Unit-01

## Equipment Inventory
| Tag | Equipment Name | Type | DEXPI Class |
| :--- | :--- | :--- | :--- |
| `TK-101` | Feed Surge Tank | tank | DEXPI.Vessel |
| `P-101A` | Centrifugal Feed Pump | pump | DEXPI.CentrifugalPump |
| `R-201` | Continuous Stirred-Tank Reactor | reactor | DEXPI.Reactor |
| `C-301` | Depropanizer Stripping Column | column | DEXPI.DistillationColumn |

## Instrumentation & Control Loops
| Tag | Variable | Function | Control Loop |
| :--- | :--- | :--- | :--- |
| `FT-101` | Flow Rate | Transmitter | `Loop-101` |
| `FIC-101` | Flow Rate | Indicator Controller | `Loop-101` |
| `PT-201` | Pressure | Transmitter | `Loop-201` |
| `TC-201` | Temperature | Controller | `Loop-201` |

## Flow Paths & Interconnects
| From | To | Edge Type | Spec |
| :--- | :--- | :--- | :--- |
| `TK-101` | `P-101A` | suction_line | 6-inch-CS |
| `P-101A` | `FCV-101` | discharge_line | 4-inch-CS |
| `FCV-101` | `R-201` | reactor_feed | 4-inch-CS |
| `R-201` | `C-301` | stripper_feed | 4-inch-SS |