"""Compiler helpers — document-type guessing and File view."""

from compiler import doa_conflict, guess_doc_type


def test_guess_doc_type():
    assert guess_doc_type("OldMutual-policy-wording.pdf") == "policy"
    assert guess_doc_type("rejection-letter.pdf") == "rejection"
    assert guess_doc_type("March-payslip.pdf") == "payslip"
    assert guess_doc_type("hospital-discharge.pdf") == "hospital"
    assert guess_doc_type("random-scan.jpg") == "other"
    assert guess_doc_type("note.eml") == "correspondence"
    assert guess_doc_type("AIA-PDS.pdf") == "pds"
    assert guess_doc_type("AustralianSuper-member-statement.pdf") == "super"
    assert guess_doc_type("WorkCover-file.pdf") == "workers_comp"


def test_doa_conflict():
    za = doa_conflict({"date_of_absence": "2025-03-15", "insurer_doa": "2025-05-20", "jurisdiction": "za"})
    assert za and "Date of Absence" in za["label"]
    au = doa_conflict({"date_of_absence": "2025-03-15", "insurer_doa": "2025-05-20", "jurisdiction": "au"})
    assert au and "Date of disablement" in au["label"]
    assert doa_conflict({"date_of_absence": "2025-03-15", "insurer_doa": "2025-03-15"}) is None
    assert doa_conflict({}) is None
