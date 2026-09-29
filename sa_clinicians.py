"""South African clinician and provider types for diagnosis attribution."""

from __future__ import annotations

# HPCSA-aligned and common SA certificate wording — specialty/role, not individual names.
SA_CLINICIANS: list[dict[str, str]] = [
    {"name": "General Practitioner (GP)", "category": "Medical doctor", "description": "Primary care doctor — first point for sick notes, referrals, and ongoing treatment."},
    {"name": "Family Physician", "category": "Medical doctor", "description": "GP with additional family-medicine training — common on employer and insurer forms."},
    {"name": "Physician (specialist)", "category": "Medical doctor", "description": "Internal medicine specialist — often manages complex or multi-system conditions."},
    {"name": "Psychiatrist", "category": "Mental health", "description": "Medical doctor specialising in mental illness — can diagnose, prescribe, and admit."},
    {"name": "Clinical Psychologist", "category": "Mental health", "description": "HPCSA-registered psychologist — assessment, therapy, and reports (cannot prescribe scheduled medicine)."},
    {"name": "Registered Counsellor", "category": "Mental health", "description": "HPCSA-registered counsellor — supportive therapy and wellness reports."},
    {"name": "Educational Psychologist", "category": "Mental health", "description": "Assesses learning, cognitive, and developmental functioning — often in workplace capacity disputes."},
    {"name": "Industrial / Organisational Psychologist", "category": "Mental health", "description": "Workplace stress, burnout, and occupational functioning assessments."},
    {"name": "Neuropsychologist", "category": "Mental health", "description": "Tests memory, attention, and executive function — useful for cognitive injury claims."},
    {"name": "Social Worker", "category": "Allied health", "description": "Psychosocial assessment and support — sometimes cited on hospital discharge summaries."},
    {"name": "Occupational Therapist", "category": "Allied health", "description": "Assesses daily and work functioning — ADLs and return-to-work capacity."},
    {"name": "Physiotherapist", "category": "Allied health", "description": "Physical rehabilitation, pain management, and mobility — common for MSK claims."},
    {"name": "Biokineticist", "category": "Allied health", "description": "Exercise-based rehabilitation and conditioning programmes."},
    {"name": "Speech Therapist / Audiologist", "category": "Allied health", "description": "Communication, swallowing, and hearing-related functional limits."},
    {"name": "Dietitian", "category": "Allied health", "description": "Nutrition-related conditions and metabolic management."},
    {"name": "Chiropractor", "category": "Allied health", "description": "Musculoskeletal manipulation — sometimes documented on back/neck injury claims."},
    {"name": "Podiatrist", "category": "Allied health", "description": "Foot and lower-limb conditions affecting standing and mobility duties."},
    {"name": "Neurologist", "category": "Specialist", "description": "Brain, spine, nerve, and seizure disorders — migraine, MS, neuropathy."},
    {"name": "Neurosurgeon", "category": "Specialist", "description": "Surgical treatment of brain and spine conditions."},
    {"name": "Orthopaedic Surgeon", "category": "Specialist", "description": "Bones, joints, spine surgery — fractures, disc disease, joint replacement."},
    {"name": "Rheumatologist", "category": "Specialist", "description": "Autoimmune and inflammatory joint conditions — RA, lupus, fibromyalgia work-up."},
    {"name": "Pain Specialist", "category": "Specialist", "description": "Chronic pain management — multidisciplinary pain programmes."},
    {"name": "Rehabilitation Physician", "category": "Specialist", "description": "Physical medicine and rehab — return-to-work and impairment assessments."},
    {"name": "Occupational Medicine Physician", "category": "Specialist", "description": "Work-related illness and fitness-for-work opinions — often employer-appointed."},
    {"name": "Sports Medicine Physician", "category": "Specialist", "description": "Athletic and musculoskeletal injuries — soft-tissue and overuse conditions."},
    {"name": "Cardiologist", "category": "Specialist", "description": "Heart and blood-vessel conditions — hypertension, arrhythmia, heart failure."},
    {"name": "Cardiothoracic Surgeon", "category": "Specialist", "description": "Heart and chest surgery."},
    {"name": "Vascular Surgeon", "category": "Specialist", "description": "Arteries, veins, and circulatory surgery."},
    {"name": "Pulmonologist", "category": "Specialist", "description": "Lung disease — asthma, COPD, post-COVID respiratory sequelae."},
    {"name": "Gastroenterologist", "category": "Specialist", "description": "Digestive tract and liver disease — IBD, reflux, functional gut disorders."},
    {"name": "Endocrinologist", "category": "Specialist", "description": "Hormone and metabolic disorders — diabetes, thyroid, adrenal conditions."},
    {"name": "Nephrologist", "category": "Specialist", "description": "Kidney disease and dialysis-related care."},
    {"name": "Urologist", "category": "Specialist", "description": "Urinary tract and male reproductive conditions."},
    {"name": "Gynaecologist", "category": "Specialist", "description": "Female reproductive health — endometriosis, PCOS, pregnancy-related conditions."},
    {"name": "Obstetrician", "category": "Specialist", "description": "Pregnancy and childbirth — maternity leave and postpartum claims."},
    {"name": "Dermatologist", "category": "Specialist", "description": "Skin conditions — chronic dermatitis, psoriasis, work-related skin disease."},
    {"name": "Ophthalmologist", "category": "Specialist", "description": "Eye disease and surgery — vision loss affecting safety-critical duties."},
    {"name": "ENT Specialist (Otolaryngologist)", "category": "Specialist", "description": "Ear, nose, throat — balance disorders, hearing loss."},
    {"name": "Haematologist", "category": "Specialist", "description": "Blood disorders — anaemia, clotting, leukaemia."},
    {"name": "Oncologist", "category": "Specialist", "description": "Cancer diagnosis and treatment — chemotherapy, radiation planning."},
    {"name": "Radiation Oncologist", "category": "Specialist", "description": "Radiotherapy for cancer — treatment side effects and work limits."},
    {"name": "Infectious Disease Specialist", "category": "Specialist", "description": "Complex infections — TB, HIV management, post-infectious syndromes."},
    {"name": "Geriatrician", "category": "Specialist", "description": "Older adults — frailty, dementia, polypharmacy."},
    {"name": "Paediatrician", "category": "Specialist", "description": "Children's medicine — rarely on adult IP claims unless noted historically."},
    {"name": "Emergency Medicine Physician", "category": "Hospital", "description": "Casualty / ER doctor — acute presentations and admission decisions."},
    {"name": "Anaesthesiologist", "category": "Specialist", "description": "Anaesthesia and peri-operative care — pain blocks and ICU."},
    {"name": "Intensivist / ICU Specialist", "category": "Hospital", "description": "Critical care physician — severe illness and ventilation."},
    {"name": "Radiologist", "category": "Diagnostics", "description": "Interprets X-rays, CT, MRI — reports often support MSK and neuro claims."},
    {"name": "Pathologist", "category": "Diagnostics", "description": "Laboratory and tissue diagnosis — biopsy and blood-test interpretation."},
    {"name": "Clinical Pathologist", "category": "Diagnostics", "description": "Lab medicine specialist — blood results on certificates."},
    {"name": "Nuclear Medicine Physician", "category": "Diagnostics", "description": "Specialised imaging — bone scans, PET."},
    {"name": "General Surgeon", "category": "Specialist", "description": "Abdominal and general surgical procedures."},
    {"name": "Plastic & Reconstructive Surgeon", "category": "Specialist", "description": "Soft-tissue repair, burns, and reconstructive surgery."},
    {"name": "Maxillofacial & Oral Surgeon", "category": "Specialist", "description": "Jaw, face, and dental surgery."},
    {"name": "Dentist", "category": "Dental", "description": "Oral health — TMJ, dental infection, facial pain."},
    {"name": "Optometrist", "category": "Allied health", "description": "Vision testing and glasses — not a medical doctor but common on forms."},
    {"name": "Pharmacist (clinical)", "category": "Pharmacy", "description": "Medication review and chronic medicine management."},
    {"name": "Registered Nurse (specialist)", "category": "Nursing", "description": "Advanced practice nurse — chronic disease and wound care."},
    {"name": "Psychiatric Nurse", "category": "Nursing", "description": "Mental health nursing — inpatient and community psych care."},
    {"name": "Midwife", "category": "Nursing", "description": "Maternity care provider."},
    {"name": "Clinical Technologist", "category": "Diagnostics", "description": "Cardiology or renal technology — ECG, dialysis support."},
    {"name": "Radiographer", "category": "Diagnostics", "description": "Performs imaging — not the reporting doctor."},
    {"name": "Homeopath (registered)", "category": "Complementary", "description": "AHPCSA-registered homeopath — some chronic illness certificates."},
    {"name": "Traditional Health Practitioner", "category": "Complementary", "description": "Traditional medicine practitioner — note exact wording on certificates."},
    {"name": "Trauma Counsellor", "category": "Mental health", "description": "Crisis and trauma debriefing — PTSD and assault-related claims."},
    {"name": "Employee Health / Wellness Nurse", "category": "Occupational", "description": "On-site occupational health — employer sick-note gatekeeper."},
    {"name": "Company Doctor / Occupational Health Doctor", "category": "Occupational", "description": "Employer-appointed doctor — fitness-for-work and return-to-work opinions."},
    {"name": "Independent Medical Examiner (IME)", "category": "Assessor", "description": "Insurer- or employer-appointed assessor — not treating doctor."},
    {"name": "Medico-Legal Assessor", "category": "Assessor", "description": "RAF or compensation fund assessor — impairment ratings."},
    {"name": "Hospital Doctor (unnamed)", "category": "Hospital", "description": "Admitting or ward doctor when specialist name not recorded."},
    {"name": "Medical Officer", "category": "Hospital", "description": "Hospital medical officer — common on state hospital records."},
    {"name": "Registrar", "category": "Hospital", "description": "Specialist trainee — may sign notes under supervision."},
    {"name": "Professor / Academic Specialist", "category": "Specialist", "description": "University-affiliated specialist — teaching hospital reports."},
    {"name": "Discovery Health GP Network", "category": "Medical scheme", "description": "Scheme-network GP — note if certificate from designated service provider."},
    {"name": "Pathcare / Ampath / Lancet Lab", "category": "Diagnostics", "description": "Private pathology laboratory — results supporting diagnosis."},
    {"name": "Netcare / Mediclinic / Life Healthcare", "category": "Hospital", "description": "Private hospital group — admission and procedure records."},
    {"name": "State Hospital / District Hospital", "category": "Hospital", "description": "Public sector facility — discharge summaries and sick notes."},
    {"name": "Clinic Sister / Primary Care Nurse", "category": "Nursing", "description": "Primary clinic nurse — may issue limited sick notes in some settings."},
    {"name": "Psychiatric Hospital", "category": "Hospital", "description": "Inpatient mental health facility — admission certificates."},
    {"name": "Rehabilitation Centre", "category": "Hospital", "description": "Substance use or physical rehab inpatient programme."},
    {"name": "Sleep Laboratory", "category": "Diagnostics", "description": "Sleep study centre — insomnia, sleep apnoea evidence."},
    {"name": "Pain Clinic", "category": "Specialist", "description": "Multidisciplinary chronic pain programme."},
    {"name": "Psychiatric Day Hospital", "category": "Mental health", "description": "Day-patient mental health programme."},
]


def search_clinicians(query: str, limit: int = 20) -> list[dict]:
    q = (query or "").strip().lower()
    if not q:
        return SA_CLINICIANS
    scored: list[tuple[int, dict]] = []
    for item in SA_CLINICIANS:
        hay = " ".join((item.get("name", ""), item.get("category", ""))).lower()
        if q not in hay:
            continue
        scored.append((hay.find(q), item))
    scored.sort(key=lambda x: (x[0], x[1]["name"]))
    return [item for _, item in scored[:limit]]