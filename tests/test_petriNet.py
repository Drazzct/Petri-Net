import pytest
from src.PetriNet import PetriNet
from pathlib import Path

def test_001():
    base_dir = Path(__file__).parent / "test_1"
    
    pn = PetriNet.from_pnml(str(base_dir / "example.pnml"))
    with open(base_dir / "expected.txt", "r", encoding="utf-8", newline=None) as f:
        expected_content = f.read().strip()
        
    actual_content = str(pn).strip()
    assert actual_content == expected_content, "PetriNet.from_pnml output does not match expected"
