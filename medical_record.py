"""ICD-10 diagnoses and medication reference data for medical record intake.

Canonical master registry: clinical_atlas.py (Clinical Atlas resources UI).
SA monographs, footnotes, and sources: clinical_atlas_references.py.
"""

from __future__ import annotations

DIAGNOSIS_CATEGORY_INFO: dict[str, str] = {
    "Mental health": "Conditions affecting mood, anxiety, thinking, or behaviour — insurers still need duty-impact evidence, not diagnosis alone.",
    "Sleep": "Disorders of sleep quality, timing, or breathing — often linked to fatigue and cognitive work limits.",
    "Pain & MSK": "Musculoskeletal and chronic pain — common in desk, manual, and travel-heavy roles.",
    "Injury": "Event-based harm — document when, where, and how; distinguish from gradual illness.",
    "Neurological": "Brain, nerve, and coordination conditions — may affect concentration, safety, or stamina.",
    "Cardiovascular": "Heart and circulation — stamina, shift work, and stress tolerance may be affected.",
    "Metabolic": "Hormone, blood sugar, and weight-related conditions — fatigue and attendance are common themes.",
    "Haematology": "Blood disorders — anaemia commonly causes fatigue and reduced endurance.",
    "GI": "Digestive conditions — nausea, urgency, and pain can limit travel and client-facing work.",
    "Respiratory": "Lung conditions — breathlessness affects physical and sometimes cognitive endurance.",
    "Infectious": "Infection and post-infectious illness — include dates and continuity for waiting-period arguments.",
    "Oncology": "Cancer and related conditions — treatment side effects often drive work incapacity.",
    "Renal": "Kidney disease — fatigue, fluid restrictions, and dialysis schedules affect duties.",
    "Gynaecology": "Female reproductive health — may affect attendance, pain, and hormone-related symptoms.",
    "Substance": "Alcohol or drug use disorders — policy exclusions and rehab cooperation may apply.",
    "Ophthalmology": "Eye conditions — visual field and acuity limits may affect driving, screen work, and safety-critical roles.",
    "Other": "Symptom-based or non-specific codes — pair with functional impact in your story.",
}

MEDICATION_CATEGORY_INFO: dict[str, str] = {
    "SSRI antidepressant": "Selective serotonin reuptake inhibitor — treats depression/anxiety; common side effects: nausea, sleep change, sexual dysfunction.",
    "SNRI antidepressant": "Serotonin-noradrenaline reuptake inhibitor — depression, anxiety, and some pain; may raise blood pressure.",
    "Tricyclic antidepressant": "Older antidepressant class — also used for nerve pain and sleep at low doses; sedation common.",
    "Atypical antidepressant": "Non-SSRI antidepressants — e.g. mirtazapine (sedating), bupropion (activating).",
    "Mood stabiliser": "Controls bipolar mood swings — lithium requires blood monitoring.",
    "Benzodiazepine": "Short-term anxiety/sleep drug — dependence risk; insurers may query long-term use.",
    "Sleep aid": "Medication to induce sleep — morning sedation can affect duty performance.",
    "Antipsychotic": "Treats psychosis and sometimes bipolar depression — sedation and metabolic effects.",
    "Neuropathic pain / anxiety": "Nerve-pain and anxiety drug — pregabalin causes dizziness and sedation.",
    "Neuropathic pain": "Calms overactive nerves — dizziness and fatigue are common.",
    "Opioid analgesic": "Strong pain relief — dependence, sedation, and safety-critical work limits.",
    "Analgesic": "Pain and fever relief — paracetamol is generally non-sedating.",
    "NSAID": "Anti-inflammatory pain relief — stomach and kidney precautions with long use.",
    "Combination analgesic": "Multi-ingredient pain tablet — often includes codeine (sedating, restricted).",
    "Pain / sleep adjunct": "Low-dose antidepressant used for pain or sleep rather than mood.",
    "Migraine prophylaxis": "Preventive migraine treatment — taken daily, not for acute attacks.",
    "Migraine acute": "Stops migraine attack — limited monthly use; cardiovascular cautions.",
    "Beta-blocker / anxiety": "Slows heart rate — used for anxiety physical symptoms and migraine prevention.",
    "ADHD": "Stimulant or non-stimulant focus medication — appetite and sleep effects.",
    "Thyroid": "Replaces or suppresses thyroid hormone — requires blood test monitoring.",
    "Diabetes": "Lowers blood sugar — hypoglycaemia risk if dosing or meals are irregular.",
    "Antihypertensive": "Blood pressure treatment — dizziness on standing may affect duties.",
    "ACE inhibitor": "Blood pressure and heart failure drug — dry cough is a common side effect.",
    "ARB": "Blood pressure drug alternative to ACE inhibitors.",
    "Statin": "Cholesterol lowering — muscle pain reported by some patients.",
    "Antiplatelet": "Reduces clot risk — bleeding precautions with surgery/injury.",
    "Anticoagulant": "Blood thinner — bruising and bleeding risk; interacts with many drugs.",
    "Corticosteroid": "Reduces inflammation — insomnia, mood changes, and blood sugar effects.",
    "Bronchodilator": "Opens airways in asthma/COPD — tremor and fast heartbeat possible.",
    "Asthma / COPD": "Inhaled steroid/long-acting bronchodilator — rinse mouth after use.",
    "Substance use": "Supports alcohol or opioid recovery — part of structured treatment plans.",
    "Supplement": "Vitamins/minerals — document if prescribed for diagnosed deficiency.",
    "Non-drug treatment": "Therapy or rehabilitation — still evidence for functional capacity.",
    "Other": "Other prescribed or complementary treatment — note prescriber and work impact.",
}

ICD10_DIAGNOSES: list[dict[str, str]] = [
    {"name": "Major depressive disorder, single episode", "code": "F32.9", "category": "Mental health"},
    {"name": "Major depressive disorder, recurrent", "code": "F33.9", "category": "Mental health"},
    {"name": "Major depressive disorder, moderate", "code": "F32.1", "category": "Mental health"},
    {"name": "Major depressive disorder, severe", "code": "F32.2", "category": "Mental health"},
    {"name": "Dysthymic disorder / persistent depressive disorder", "code": "F34.1", "category": "Mental health"},
    {"name": "Generalised anxiety disorder", "code": "F41.1", "category": "Mental health"},
    {"name": "Panic disorder", "code": "F41.0", "category": "Mental health"},
    {"name": "Mixed anxiety and depressive disorder", "code": "F41.2", "category": "Mental health"},
    {"name": "Adjustment disorder with anxiety", "code": "F43.22", "category": "Mental health"},
    {"name": "Adjustment disorder with depressed mood", "code": "F43.21", "category": "Mental health"},
    {"name": "Post-traumatic stress disorder (PTSD)", "code": "F43.10", "category": "Mental health"},
    {"name": "Acute stress reaction", "code": "F43.0", "category": "Mental health"},
    {"name": "Burnout / exhaustion disorder (working diagnosis)", "code": "Z73.0", "category": "Mental health"},
    {"name": "Schizophrenia", "code": "F20.9", "category": "Mental health"},
    {"name": "Bipolar affective disorder", "code": "F31.9", "category": "Mental health"},
    {"name": "Bipolar disorder, current episode depressed", "code": "F31.3", "category": "Mental health"},
    {"name": "Obsessive-compulsive disorder", "code": "F42.9", "category": "Mental health"},
    {"name": "Social phobia / social anxiety disorder", "code": "F40.1", "category": "Mental health"},
    {"name": "Agoraphobia", "code": "F40.0", "category": "Mental health"},
    {"name": "Insomnia", "code": "G47.0", "category": "Sleep"},
    {"name": "Sleep disorder, unspecified", "code": "G47.9", "category": "Sleep"},
    {"name": "Chronic fatigue syndrome / ME", "code": "G93.3", "category": "Other"},
    {"name": "Fibromyalgia", "code": "M79.7", "category": "Pain & MSK"},
    {"name": "Chronic pain syndrome", "code": "G89.4", "category": "Pain & MSK"},
    {"name": "Low back pain", "code": "M54.5", "category": "Pain & MSK"},
    {"name": "Dorsalgia, unspecified", "code": "M54.9", "category": "Pain & MSK"},
    {"name": "Cervicalgia (neck pain)", "code": "M54.2", "category": "Pain & MSK"},
    {"name": "Thoracic back pain", "code": "M54.6", "category": "Pain & MSK"},
    {"name": "Sciatica", "code": "M54.3", "category": "Pain & MSK"},
    {"name": "Lumbar disc disorder with radiculopathy", "code": "M51.1", "category": "Pain & MSK"},
    {"name": "Intervertebral disc degeneration, lumbar", "code": "M51.36", "category": "Pain & MSK"},
    {"name": "Cervical disc disorder with radiculopathy", "code": "M50.1", "category": "Pain & MSK"},
    {"name": "Spinal stenosis, lumbar region", "code": "M48.06", "category": "Pain & MSK"},
    {"name": "Spondylosis, lumbar", "code": "M47.816", "category": "Pain & MSK"},
    {"name": "Rotator cuff syndrome", "code": "M75.1", "category": "Pain & MSK"},
    {"name": "Shoulder impingement syndrome", "code": "M75.4", "category": "Pain & MSK"},
    {"name": "Tennis elbow / lateral epicondylitis", "code": "M77.1", "category": "Pain & MSK"},
    {"name": "Carpal tunnel syndrome", "code": "G56.0", "category": "Pain & MSK"},
    {"name": "Osteoarthritis, knee", "code": "M17.9", "category": "Pain & MSK"},
    {"name": "Osteoarthritis, hip", "code": "M16.9", "category": "Pain & MSK"},
    {"name": "Rheumatoid arthritis", "code": "M06.9", "category": "Pain & MSK"},
    {"name": "Systemic lupus erythematosus", "code": "M32.9", "category": "Pain & MSK"},
    {"name": "Ankylosing spondylitis", "code": "M45", "category": "Pain & MSK"},
    {"name": "Fracture, unspecified", "code": "T14.2", "category": "Injury"},
    {"name": "Sprain of lumbar spine", "code": "S33.5", "category": "Injury"},
    {"name": "Concussion", "code": "S06.0", "category": "Injury"},
    {"name": "Whiplash injury", "code": "S13.4", "category": "Injury"},
    {"name": "Migraine, unspecified", "code": "G43.9", "category": "Neurological"},
    {"name": "Migraine without aura", "code": "G43.0", "category": "Neurological"},
    {"name": "Migraine with aura", "code": "G43.1", "category": "Neurological"},
    {"name": "Epilepsy, unspecified", "code": "G40.9", "category": "Neurological"},
    {"name": "Multiple sclerosis", "code": "G35", "category": "Neurological"},
    {"name": "Parkinson disease", "code": "G20", "category": "Neurological"},
    {"name": "Stroke / cerebrovascular accident", "code": "I63.9", "category": "Cardiovascular"},
    {"name": "Hypertension", "code": "I10", "category": "Cardiovascular"},
    {"name": "Atrial fibrillation", "code": "I48.9", "category": "Cardiovascular"},
    {"name": "Coronary artery disease", "code": "I25.10", "category": "Cardiovascular"},
    {"name": "Heart failure", "code": "I50.9", "category": "Cardiovascular"},
    {"name": "Cardiomyopathy", "code": "I42.9", "category": "Cardiovascular"},
    {"name": "Type 2 diabetes mellitus", "code": "E11.9", "category": "Metabolic"},
    {"name": "Type 1 diabetes mellitus", "code": "E10.9", "category": "Metabolic"},
    {"name": "Addison disease", "code": "E27.1", "category": "Metabolic"},
    {"name": "Diabetes insipidus", "code": "E23.2", "category": "Metabolic"},
    {"name": "Hyperlipidaemia", "code": "E78.5", "category": "Metabolic"},
    {"name": "Hypothyroidism", "code": "E03.9", "category": "Metabolic"},
    {"name": "Hyperthyroidism", "code": "E05.9", "category": "Metabolic"},
    {"name": "Obesity", "code": "E66.9", "category": "Metabolic"},
    {"name": "Anaemia, unspecified", "code": "D64.9", "category": "Haematology"},
    {"name": "Iron deficiency anaemia", "code": "D50.9", "category": "Haematology"},
    {"name": "Haemophilia", "code": "D66", "category": "Haematology"},
    {"name": "Vitamin B12 deficiency", "code": "E53.8", "category": "Metabolic"},
    {"name": "Gastro-oesophageal reflux disease (GORD)", "code": "K21.9", "category": "GI"},
    {"name": "Irritable bowel syndrome", "code": "K58.9", "category": "GI"},
    {"name": "Inflammatory bowel disease, unspecified", "code": "K52.9", "category": "GI"},
    {"name": "Crohn disease", "code": "K50.90", "category": "GI"},
    {"name": "Ulcerative colitis", "code": "K51.90", "category": "GI"},
    {"name": "Asthma", "code": "J45.9", "category": "Respiratory"},
    {"name": "Bronchiectasis", "code": "J47", "category": "Respiratory"},
    {"name": "COPD", "code": "J44.9", "category": "Respiratory"},
    {"name": "Pneumonia", "code": "J18.9", "category": "Respiratory"},
    {"name": "COVID-19, unspecified", "code": "U07.1", "category": "Infectious"},
    {"name": "Long COVID / post-COVID condition", "code": "U09.9", "category": "Infectious"},
    {"name": "HIV disease", "code": "B24", "category": "Infectious"},
    {"name": "Tuberculosis", "code": "A15.9", "category": "Infectious"},
    {"name": "Malignant neoplasm, unspecified", "code": "C80.1", "category": "Oncology"},
    {"name": "Breast cancer", "code": "C50.9", "category": "Oncology"},
    {"name": "Prostate cancer", "code": "C61", "category": "Oncology"},
    {"name": "Skin cancer (melanoma)", "code": "C43.9", "category": "Oncology"},
    {"name": "Benign neoplasm, unspecified", "code": "D36.9", "category": "Oncology"},
    {"name": "Chronic kidney disease", "code": "N18.9", "category": "Renal"},
    {"name": "Urinary tract infection", "code": "N39.0", "category": "Renal"},
    {"name": "Endometriosis", "code": "N80.9", "category": "Gynaecology"},
    {"name": "Polycystic ovarian syndrome", "code": "E28.2", "category": "Gynaecology"},
    {"name": "Pregnancy-related condition, unspecified", "code": "O26.9", "category": "Gynaecology"},
    {"name": "Substance use disorder, unspecified", "code": "F19.10", "category": "Substance"},
    {"name": "Alcohol use disorder", "code": "F10.20", "category": "Substance"},
    {"name": "Attention-deficit hyperactivity disorder (ADHD)", "code": "F90.9", "category": "Mental health"},
    {"name": "Autism spectrum disorder", "code": "F84.0", "category": "Mental health"},
    {"name": "Personality disorder, unspecified", "code": "F60.9", "category": "Mental health"},
    {"name": "Eating disorder, unspecified", "code": "F50.9", "category": "Mental health"},
    {"name": "Glaucoma", "code": "H40.9", "category": "Ophthalmology"},
    {"name": "Vertigo", "code": "R42", "category": "Other"},
    {"name": "Syncope and collapse", "code": "R55", "category": "Other"},
    {"name": "Malaise and fatigue", "code": "R53", "category": "Other"},
    {"name": "Illness, unspecified", "code": "R69", "category": "Other"},
    {"name": "Injury, unspecified", "code": "T14.9", "category": "Injury"},
]

MEDICATIONS: list[dict[str, str]] = [
    {"name": "Cipralex (escitalopram)", "generic": "escitalopram", "category": "SSRI antidepressant"},
    {"name": "Lexamil (escitalopram)", "generic": "escitalopram", "category": "SSRI antidepressant"},
    {"name": "Zoloft (sertraline)", "generic": "sertraline", "category": "SSRI antidepressant"},
    {"name": "Serlife (sertraline)", "generic": "sertraline", "category": "SSRI antidepressant"},
    {"name": "Prozac (fluoxetine)", "generic": "fluoxetine", "category": "SSRI antidepressant"},
    {"name": "Lovan (fluoxetine)", "generic": "fluoxetine", "category": "SSRI antidepressant"},
    {"name": "Paxil (paroxetine)", "generic": "paroxetine", "category": "SSRI antidepressant"},
    {"name": "Cilift (citalopram)", "generic": "citalopram", "category": "SSRI antidepressant"},
    {"name": "Efexor (venlafaxine)", "generic": "venlafaxine", "category": "SNRI antidepressant"},
    {"name": "Venlor (venlafaxine)", "generic": "venlafaxine", "category": "SNRI antidepressant"},
    {"name": "Cymbalta (duloxetine)", "generic": "duloxetine", "category": "SNRI antidepressant"},
    {"name": "Amitriptyline", "generic": "amitriptyline", "category": "Tricyclic antidepressant"},
    {"name": "Trepiline (amitriptyline)", "generic": "amitriptyline", "category": "Tricyclic antidepressant"},
    {"name": "Nuzak (fluoxetine)", "generic": "fluoxetine", "category": "SSRI antidepressant"},
    {"name": "Wellbutrin (bupropion)", "generic": "bupropion", "category": "Atypical antidepressant"},
    {"name": "Mirtaz (mirtazapine)", "generic": "mirtazapine", "category": "Atypical antidepressant"},
    {"name": "Remeron (mirtazapine)", "generic": "mirtazapine", "category": "Atypical antidepressant"},
    {"name": "Lithium carbonate", "generic": "lithium", "category": "Mood stabiliser"},
    {"name": "Epilim (sodium valproate)", "generic": "valproate", "category": "Mood stabiliser"},
    {"name": "Lamictin (lamotrigine)", "generic": "lamotrigine", "category": "Mood stabiliser"},
    {"name": "Xanor (alprazolam)", "generic": "alprazolam", "category": "Benzodiazepine"},
    {"name": "Rivotril (clonazepam)", "generic": "clonazepam", "category": "Benzodiazepine"},
    {"name": "Ativan (lorazepam)", "generic": "lorazepam", "category": "Benzodiazepine"},
    {"name": "Valium (diazepam)", "generic": "diazepam", "category": "Benzodiazepine"},
    {"name": "Stilnox (zolpidem)", "generic": "zolpidem", "category": "Sleep aid"},
    {"name": "Imovane (zopiclone)", "generic": "zopiclone", "category": "Sleep aid"},
    {"name": "Seroquel (quetiapine)", "generic": "quetiapine", "category": "Antipsychotic"},
    {"name": "Risperdal (risperidone)", "generic": "risperidone", "category": "Antipsychotic"},
    {"name": "Abilify (aripiprazole)", "generic": "aripiprazole", "category": "Antipsychotic"},
    {"name": "Lyrica (pregabalin)", "generic": "pregabalin", "category": "Neuropathic pain / anxiety"},
    {"name": "Pregabalin (generic)", "generic": "pregabalin", "category": "Neuropathic pain / anxiety"},
    {"name": "Neurontin (gabapentin)", "generic": "gabapentin", "category": "Neuropathic pain"},
    {"name": "Gabapentin (generic)", "generic": "gabapentin", "category": "Neuropathic pain"},
    {"name": "Tramadol", "generic": "tramadol", "category": "Opioid analgesic"},
    {"name": "Tramal (tramadol)", "generic": "tramadol", "category": "Opioid analgesic"},
    {"name": "Codeine phosphate", "generic": "codeine", "category": "Opioid analgesic"},
    {"name": "Panado (paracetamol)", "generic": "paracetamol", "category": "Analgesic"},
    {"name": "Brufen (ibuprofen)", "generic": "ibuprofen", "category": "NSAID"},
    {"name": "Voltaren (diclofenac)", "generic": "diclofenac", "category": "NSAID"},
    {"name": "Celebrex (celecoxib)", "generic": "celecoxib", "category": "NSAID"},
    {"name": "Arcoxia (etoricoxib)", "generic": "etoricoxib", "category": "NSAID"},
    {"name": "Myprodol", "generic": "paracetamol + ibuprofen + codeine", "category": "Combination analgesic"},
    {"name": "Stilpane", "generic": "paracetamol + codeine", "category": "Combination analgesic"},
    {"name": "Trepiline (low-dose amitriptyline)", "generic": "amitriptyline", "category": "Pain / sleep adjunct"},
    {"name": "Elavil (amitriptyline)", "generic": "amitriptyline", "category": "Tricyclic antidepressant"},
    {"name": "Topamax (topiramate)", "generic": "topiramate", "category": "Migraine prophylaxis"},
    {"name": "Imigran (sumatriptan)", "generic": "sumatriptan", "category": "Migraine acute"},
    {"name": "Propranolol", "generic": "propranolol", "category": "Beta-blocker / anxiety"},
    {"name": "Inderal (propranolol)", "generic": "propranolol", "category": "Beta-blocker / anxiety"},
    {"name": "Ritalin (methylphenidate)", "generic": "methylphenidate", "category": "ADHD"},
    {"name": "Ritalin LA (methylphenidate LA)", "generic": "methylphenidate", "category": "ADHD"},
    {"name": "Concerta (methylphenidate ER)", "generic": "methylphenidate", "category": "ADHD"},
    {"name": "Medikinet LA (methylphenidate LA)", "generic": "methylphenidate", "category": "ADHD"},
    {"name": "Rubifen (methylphenidate)", "generic": "methylphenidate", "category": "ADHD"},
    {"name": "Attenta (methylphenidate)", "generic": "methylphenidate", "category": "ADHD"},
    {"name": "Strattera (atomoxetine)", "generic": "atomoxetine", "category": "ADHD"},
    {"name": "Eltroxin (levothyroxine)", "generic": "levothyroxine", "category": "Thyroid"},
    {"name": "Euthyrox (levothyroxine)", "generic": "levothyroxine", "category": "Thyroid"},
    {"name": "Metformin", "generic": "metformin", "category": "Diabetes"},
    {"name": "Glucophage (metformin)", "generic": "metformin", "category": "Diabetes"},
    {"name": "Amlodipine", "generic": "amlodipine", "category": "Antihypertensive"},
    {"name": "Enalapril", "generic": "enalapril", "category": "ACE inhibitor"},
    {"name": "Losartan", "generic": "losartan", "category": "ARB"},
    {"name": "Atorvastatin", "generic": "atorvastatin", "category": "Statin"},
    {"name": "Aspirin", "generic": "aspirin", "category": "Antiplatelet"},
    {"name": "Warfarin", "generic": "warfarin", "category": "Anticoagulant"},
    {"name": "Xarelto (rivaroxaban)", "generic": "rivaroxaban", "category": "Anticoagulant"},
    {"name": "Eliquis (apixaban)", "generic": "apixaban", "category": "Anticoagulant"},
    {"name": "Prednisone", "generic": "prednisone", "category": "Corticosteroid"},
    {"name": "Medrol (methylprednisolone)", "generic": "methylprednisolone", "category": "Corticosteroid"},
    {"name": "Salbutamol inhaler", "generic": "salbutamol", "category": "Bronchodilator"},
    {"name": "Seretide inhaler", "generic": "fluticasone + salmeterol", "category": "Asthma / COPD"},
    {"name": "Antabuse (disulfiram)", "generic": "disulfiram", "category": "Substance use"},
    {"name": "Campral (acamprosate)", "generic": "acamprosate", "category": "Substance use"},
    {"name": "Naltrexone", "generic": "naltrexone", "category": "Substance use"},
    {"name": "Suboxone (buprenorphine + naloxone)", "generic": "buprenorphine", "category": "Substance use"},
    {"name": "Methadone", "generic": "methadone", "category": "Substance use"},
    {"name": "Vitamin B12 injection", "generic": "cyanocobalamin", "category": "Supplement"},
    {"name": "Ferrous sulphate (iron)", "generic": "iron", "category": "Supplement"},
    {"name": "Vitamin D", "generic": "cholecalciferol", "category": "Supplement"},
    {"name": "Magnesium supplement", "generic": "magnesium", "category": "Supplement"},
    {"name": "Melatonin", "generic": "melatonin", "category": "Sleep aid"},
    {"name": "CBD oil (prescribed)", "generic": "cannabidiol", "category": "Other"},
    {"name": "Medical cannabis (prescribed)", "generic": "cannabis", "category": "Other"},
    {"name": "Physiotherapy (prescribed)", "generic": "physiotherapy", "category": "Non-drug treatment"},
    {"name": "Psychotherapy / CBT", "generic": "psychotherapy", "category": "Non-drug treatment"},
    {"name": "Occupational therapy", "generic": "occupational therapy", "category": "Non-drug treatment"},
]

# SA market strengths by active ingredient — pick from list; manual entry is secondary.
STRENGTHS_BY_GENERIC: dict[str, list[str]] = {
    "escitalopram": ["5 mg tablet", "10 mg tablet", "20 mg tablet"],
    "sertraline": ["50 mg tablet", "100 mg tablet"],
    "fluoxetine": ["20 mg capsule"],
    "paroxetine": ["20 mg tablet"],
    "citalopram": ["20 mg tablet", "40 mg tablet"],
    "venlafaxine": ["37.5 mg tablet", "75 mg tablet", "150 mg XR capsule"],
    "duloxetine": ["30 mg capsule", "60 mg capsule"],
    "amitriptyline": ["10 mg tablet", "25 mg tablet", "50 mg tablet"],
    "bupropion": ["150 mg SR tablet", "300 mg XL tablet"],
    "mirtazapine": ["15 mg tablet", "30 mg tablet", "45 mg tablet"],
    "lithium": ["250 mg tablet", "400 mg tablet"],
    "valproate": ["200 mg tablet", "500 mg tablet"],
    "lamotrigine": ["25 mg tablet", "50 mg tablet", "100 mg tablet", "200 mg tablet"],
    "alprazolam": ["0.25 mg tablet", "0.5 mg tablet", "1 mg tablet"],
    "clonazepam": ["0.5 mg tablet", "2 mg tablet"],
    "lorazepam": ["1 mg tablet", "2 mg tablet"],
    "diazepam": ["5 mg tablet", "10 mg tablet"],
    "zolpidem": ["10 mg tablet"],
    "zopiclone": ["7.5 mg tablet"],
    "quetiapine": ["25 mg tablet", "100 mg tablet", "200 mg tablet", "300 mg tablet"],
    "risperidone": ["1 mg tablet", "2 mg tablet", "3 mg tablet"],
    "aripiprazole": ["10 mg tablet", "15 mg tablet", "30 mg tablet"],
    "pregabalin": ["25 mg capsule", "75 mg capsule", "150 mg capsule", "300 mg capsule"],
    "gabapentin": ["100 mg capsule", "300 mg capsule", "400 mg capsule"],
    "tramadol": ["50 mg capsule", "100 mg SR tablet"],
    "codeine": ["30 mg tablet", "60 mg tablet"],
    "paracetamol": ["500 mg tablet", "1 g tablet"],
    "ibuprofen": ["200 mg tablet", "400 mg tablet", "600 mg tablet"],
    "diclofenac": ["25 mg tablet", "50 mg tablet", "50 mg enteric-coated tablet"],
    "celecoxib": ["100 mg capsule", "200 mg capsule"],
    "etoricoxib": ["60 mg tablet", "90 mg tablet", "120 mg tablet"],
    "paracetamol + ibuprofen + codeine": ["Myprodol tablet (combo)"],
    "paracetamol + codeine": ["Stilpane tablet (combo)", "15 mg codeine / 500 mg paracetamol"],
    "topiramate": ["25 mg tablet", "50 mg tablet", "100 mg tablet"],
    "sumatriptan": ["50 mg tablet", "100 mg tablet"],
    "propranolol": ["10 mg tablet", "40 mg tablet", "80 mg tablet"],
    "methylphenidate": [
        "5 mg tablet",
        "10 mg tablet",
        "20 mg tablet",
        "10 mg LA capsule",
        "20 mg LA capsule",
        "30 mg LA capsule",
        "40 mg LA capsule",
        "18 mg ER tablet",
        "27 mg ER tablet",
        "36 mg ER tablet",
        "54 mg ER tablet",
    ],
    "atomoxetine": ["10 mg capsule", "18 mg capsule", "25 mg capsule", "40 mg capsule", "60 mg capsule", "80 mg capsule", "100 mg capsule"],
    "levothyroxine": ["25 mcg tablet", "50 mcg tablet", "75 mcg tablet", "100 mcg tablet", "125 mcg tablet"],
    "metformin": ["500 mg tablet", "850 mg tablet", "1 000 mg tablet"],
    "amlodipine": ["5 mg tablet", "10 mg tablet"],
    "enalapril": ["5 mg tablet", "10 mg tablet", "20 mg tablet"],
    "losartan": ["50 mg tablet", "100 mg tablet"],
    "atorvastatin": ["10 mg tablet", "20 mg tablet", "40 mg tablet", "80 mg tablet"],
    "aspirin": ["81 mg tablet", "300 mg tablet"],
    "warfarin": ["1 mg tablet", "2 mg tablet", "5 mg tablet"],
    "rivaroxaban": ["10 mg tablet", "15 mg tablet", "20 mg tablet"],
    "apixaban": ["2.5 mg tablet", "5 mg tablet"],
    "prednisone": ["5 mg tablet", "20 mg tablet"],
    "methylprednisolone": ["4 mg tablet"],
    "salbutamol": ["100 mcg/actuation inhaler", "200 mcg/actuation inhaler"],
    "fluticasone + salmeterol": ["50/100 mcg inhaler", "125/250 mcg inhaler", "250/50 mcg inhaler"],
    "disulfiram": ["200 mg tablet"],
    "acamprosate": ["333 mg tablet"],
    "naltrexone": ["50 mg tablet"],
    "buprenorphine": ["2 mg/0.5 mg sublingual film", "8 mg/2 mg sublingual film"],
    "methadone": ["5 mg tablet", "10 mg tablet"],
    "cyanocobalamin": ["1 mg/mL injection ampoule"],
    "iron": ["200 mg ferrous sulphate tablet"],
    "cholecalciferol": ["1 000 IU capsule", "2 000 IU capsule", "50 000 IU capsule"],
    "magnesium": ["250 mg tablet", "500 mg tablet"],
    "melatonin": ["3 mg tablet", "5 mg tablet", "10 mg tablet"],
    "cannabidiol": ["10 mg/mL oil", "20 mg/mL oil"],
    "cannabis": ["Dried flower (prescribed)", "Oil extract (prescribed)"],
    "physiotherapy": ["30 min session", "45 min session", "60 min session"],
    "psychotherapy": ["50 min session", "60 min session"],
    "occupational therapy": ["45 min session", "60 min session"],
}

# Brand-specific overrides where strengths differ from generic defaults.
STRENGTHS_BY_NAME: dict[str, list[str]] = {
    "Ritalin (methylphenidate)": ["5 mg tablet", "10 mg tablet", "20 mg tablet"],
    "Ritalin LA (methylphenidate LA)": ["10 mg LA capsule", "20 mg LA capsule", "30 mg LA capsule", "40 mg LA capsule"],
    "Concerta (methylphenidate ER)": ["18 mg ER tablet", "27 mg ER tablet", "36 mg ER tablet", "54 mg ER tablet"],
    "Medikinet LA (methylphenidate LA)": ["10 mg LA capsule", "20 mg LA capsule", "30 mg LA capsule", "40 mg LA capsule"],
    "Rubifen (methylphenidate)": ["5 mg tablet", "10 mg tablet", "20 mg tablet"],
    "Attenta (methylphenidate)": ["5 mg tablet", "10 mg tablet", "20 mg tablet"],
    "Trepiline (low-dose amitriptyline)": ["10 mg tablet", "25 mg tablet"],
    "Salbutamol inhaler": ["100 mcg/actuation", "200 mcg/actuation"],
    "Seretide inhaler": ["50/100 mcg", "125/250 mcg", "250/50 mcg"],
    "Suboxone (buprenorphine + naloxone)": ["2 mg/0.5 mg film", "8 mg/2 mg film"],
}

DOSE_FREQUENCIES: list[dict[str, str]] = [
    {"id": "daily", "label": "Once daily"},
    {"id": "bd", "label": "Twice daily (BD)"},
    {"id": "tds", "label": "Three times daily (TDS)"},
    {"id": "qid", "label": "Four times daily"},
    {"id": "mane", "label": "Each morning (mane)"},
    {"id": "nocte", "label": "At night (nocte)"},
    {"id": "prn", "label": "As needed (PRN)"},
    {"id": "weekly", "label": "Once weekly"},
    {"id": "fortnightly", "label": "Fortnightly"},
    {"id": "monthly", "label": "Monthly"},
    {"id": "session", "label": "Per session / appointment"},
    {"id": "other", "label": "Other schedule"},
]

MEDICAL_AID_HELP_BY_JURISDICTION = {
    "za": {
        "title": "Medical aid claims history",
        "how_to": (
            "Request a claims history / chronic medicine register from your medical aid (Discovery, "
            "Bonitas, GEMS, etc.) — usually via the app under Claims or Documents, or email member services. "
            "Upload the PDF or export showing diagnoses, procedures, hospital admissions, and chronic "
            "medication authorisations for the last 2–3 years."
        ),
        "helps_with": [
            "Builds a medical chronology before your formal claim — useful for pre-existing debates",
            "Cross-checks diagnosis dates against symptom onset and cover start",
            "Lists medications already on chronic authorisation — saves re-typing below",
            "Shows hospital admissions and specialist visits insurers may request anyway",
            "Supports CAMAF / employer medical aid offset arguments on payslips",
        ],
    },
    "au": {
        "title": "Medicare / private health insurance history",
        "how_to": (
            "Request a claims/benefits statement from Medicare (via myGov → Medicare → Claims history) "
            "and, if you hold private hospital or extras cover, from your health fund (usually under "
            "Claims or Statements in their app or member portal, or by calling member services). Upload "
            "the export showing diagnoses, procedures, hospital admissions, and chronic medication for "
            "the last 2–3 years."
        ),
        "helps_with": [
            "Builds a medical chronology before your formal claim — useful for pre-existing debates",
            "Cross-checks diagnosis dates against symptom onset and cover start",
            "Lists medications already on prescription — saves re-typing below",
            "Shows hospital admissions and specialist visits insurers may request anyway",
            "Supports Medicare Safety Net / private health rebate arguments alongside payslips",
        ],
    },
}

# Kept as the default (ZA) for any caller that hasn't been updated to pass a
# jurisdiction — prefer medical_aid_help(code) for new call sites.
MEDICAL_AID_HELP = MEDICAL_AID_HELP_BY_JURISDICTION["za"]


def medical_aid_help(code: str | None) -> dict:
    return MEDICAL_AID_HELP_BY_JURISDICTION.get((code or "").lower(), MEDICAL_AID_HELP_BY_JURISDICTION["za"])


def _search_reference(items: list[dict], query: str, keys: tuple[str, ...], limit: int = 12) -> list[dict]:
    q = (query or "").strip().lower()
    if not q:
        return items[:limit]
    scored: list[tuple[int, dict]] = []
    for item in items:
        hay = " ".join(item.get(k, "") for k in keys).lower()
        if q not in hay:
            continue
        pos = hay.find(q)
        scored.append((pos, item))
    scored.sort(key=lambda x: (x[0], x[1].get("name", "")))
    return [item for _, item in scored[:limit]]


def diagnosis_description(item: dict) -> str:
    cat = item.get("category", "")
    base = DIAGNOSIS_CATEGORY_INFO.get(cat, "")
    code = item.get("code", "")
    name = item.get("name", "")
    parts = [f"{name}."]
    if code:
        parts.append(f"ICD-10: {code}.")
    if base:
        parts.append(base)
    return " ".join(parts)


def medication_description(item: dict) -> str:
    cat = item.get("category", "")
    generic = item.get("generic", "")
    info = MEDICATION_CATEGORY_INFO.get(cat, "")
    parts = []
    if generic:
        parts.append(f"Active ingredient: {generic}.")
    if info:
        parts.append(info)
    return " ".join(parts) if parts else item.get("name", "")


def enrich_diagnosis(item: dict) -> dict:
    return {**item, "description": diagnosis_description(item)}


def medication_strengths(item: dict) -> list[str]:
    name = item.get("name", "")
    if name in STRENGTHS_BY_NAME:
        return list(STRENGTHS_BY_NAME[name])
    generic = item.get("generic", "")
    if generic in STRENGTHS_BY_GENERIC:
        return list(STRENGTHS_BY_GENERIC[generic])
    return []


def enrich_medication(item: dict) -> dict:
    cat = item.get("category", "")
    strengths = medication_strengths(item)
    return {
        **item,
        "description": medication_description(item),
        "category_description": MEDICATION_CATEGORY_INFO.get(cat, ""),
        "strengths": strengths,
        "has_strengths": bool(strengths),
    }


def search_diagnoses(query: str, limit: int = 12) -> list[dict]:
    items = _search_reference(ICD10_DIAGNOSES, query, ("name", "code", "category"), limit)
    return [enrich_diagnosis(i) for i in items]


def search_medications(query: str, limit: int = 16) -> list[dict]:
    q = (query or "").strip().lower()
    if not q:
        items = MEDICATIONS[:limit] if limit else MEDICATIONS
    else:
        items = _search_reference(MEDICATIONS, query, ("name", "generic", "category"), limit)
    return [enrich_medication(i) for i in items]


def match_diagnosis_by_name(name: str) -> dict | None:
    n = (name or "").strip().lower()
    if not n:
        return None
    for item in ICD10_DIAGNOSES:
        if item["name"].lower() == n:
            return item
    for item in ICD10_DIAGNOSES:
        if n in item["name"].lower():
            return item
    return None