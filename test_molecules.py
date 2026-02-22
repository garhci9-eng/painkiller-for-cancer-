"""
tests/test_molecules.py
분자 특성 계산 및 필터링 유닛 테스트
"""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from utils.molecules import calculate_descriptors, lipinski_pass, side_effect_score


# ── 아세트아미노펜 (알려진 값으로 테스트) ──────────────────────────────────────
ACETAMINOPHEN = "CC(=O)Nc1ccc(O)cc1"

def test_descriptors_not_none():
    desc = calculate_descriptors(ACETAMINOPHEN)
    assert desc is not None

def test_descriptors_keys():
    desc = calculate_descriptors(ACETAMINOPHEN)
    for key in ["MW", "LogP", "HBD", "HBA", "TPSA", "RotBonds"]:
        assert key in desc, f"Missing key: {key}"

def test_acetaminophen_lipinski_pass():
    desc = calculate_descriptors(ACETAMINOPHEN)
    passed, violations = lipinski_pass(desc)
    assert passed, f"Acetaminophen should pass Lipinski. Violations: {violations}"

def test_invalid_smiles():
    desc = calculate_descriptors("NOT_A_SMILES_!!!!")
    # should return None or a dict (mock) — never raise
    # (None if RDKit available, mock dict if not)
    assert desc is None or isinstance(desc, dict)

def test_side_effect_score_range():
    desc = calculate_descriptors(ACETAMINOPHEN)
    se = side_effect_score(desc)
    assert 0.0 <= se <= 1.0, f"Score out of range: {se}"

def test_drug_score_acetaminophen():
    desc = calculate_descriptors(ACETAMINOPHEN)
    se = side_effect_score(desc)
    drug_sc = 1 - se
    assert drug_sc >= 0.5, f"Acetaminophen drug score too low: {drug_sc}"
