import pandas as pd

# Define severity levels and their temperature ranges
severity_levels = {
    "Normal": ("36.6", "37.2"),
    "Mild": ("37.3", "38.0"),
    "Severe": ("38.1", "39.0"),
    "Very Severe": ("39.1", "41.0")
}

#advice for different level
severity_advice = {
    "Normal": "Continue monitoring your symptoms. No immediate action is required.",
    "Mild": "Rest and stay hydrated. Over-the-counter medications may help.",
    "Moderate": "Consult a general physician if symptoms persist beyond 2-3 days.",
    "Severe": "Immediate medical consultation is recommended.",
    "Very Severe": "Seek emergency medical attention immediately."
}

# Sample disease definitions (expand as needed)
base_diseases = [
    # Allergies
    ("Skin Allergy", ["Itchy Skin", "Rash", "Redness"]),
    ("Dust Allergy", ["Sneezing", "Runny Nose", "Cough", "Watery Eyes"]),
    ("Food Allergy", ["Hives", "Vomiting", "Stomach Pain", "Anaphylaxis"]),
    ("Pollen Allergy", ["Sneezing", "Itchy Eyes", "Nasal Congestion"]),
    ("Pet Allergy", ["Wheezing", "Red Eyes", "Sneezing", "Itchy Eyes"]),

    # Asthma Types
    ("Allergic Asthma", ["Wheezing", "Coughing", "Tight Chest"]),
    ("Exercise-Induced Asthma", ["Shortness of Breath", "Fatigue after Exercise", "Cough"]),
    ("Occupational Asthma", ["Cough at Work", "Breathlessness", "Chest Tightness"]),

    # Fever Types
    ("Viral Fever", ["Body Ache", "Fever", "Sore Throat"]),
    ("Typhoid Fever", ["High Fever", "Abdominal Pain", "Weakness"]),
    ("Dengue Fever", ["Rash", "Joint Pain", "High Fever"]),
    ("Malaria Fever", ["Chills", "Sweating", "Headache"]),

    # Diabetes Types
    ("Type 1 Diabetes", ["Frequent Urination", "Weight Loss", "Fatigue"]),
    ("Type 2 Diabetes", ["Slow Healing Wounds", "Thirst", "Fatigue"]),
    ("Gestational Diabetes", ["Thirst", "Frequent Urination", "Blurred Vision (Pregnancy)"]),

    # Hepatitis Types
    ("Hepatitis A", ["Jaundice", "Loss of Appetite", "Fatigue"]),
    ("Hepatitis B", ["Dark Urine", "Joint Pain", "Abdominal Discomfort"]),
    ("Hepatitis C", ["Muscle Pain", "Yellow Skin", "Fatigue"]),

    # Heart Diseases
    ("Heart Attack", ["Chest Pain", "Arm Pain", "Sweating"]),
    ("Arrhythmia", ["Irregular Heartbeat", "Dizziness", "Fainting"]),
    ("Heart Failure", ["Swelling", "Fatigue", "Shortness of Breath"]),
    ("Angina", ["Chest Pain", "Dizziness", "Sweating"]),
    ("Cardiomyopathy", ["Swelling", "Breathlessness", "Fainting"]),

    # Cancers
    ("Lung Cancer", ["Chronic Cough", "Chest Pain", "Weight Loss"]),
    ("Breast Cancer", ["Lump in Breast", "Nipple Discharge", "Pain"]),
    ("Colon Cancer", ["Abdominal Pain", "Blood in Stool", "Weight Loss"]),
    ("Skin Cancer", ["New Mole", "Changes in Skin", "Itching"]),
    ("Prostate Cancer", ["Urinary Difficulty", "Pelvic Pain", "Back Pain"]),
    ("Leukemia - AML", ["Frequent Infections", "Bleeding", "Fatigue"]),
    ("Glioblastoma", ["Headache", "Blurred Vision", "Nausea"]),
    ("Meningioma", ["Seizures", "Hearing Loss", "Memory Problems"]),

    # Skin Conditions
    ("Eczema", ["Red Itchy Skin", "Dryness", "Scaly Patches"]),
    ("Psoriasis", ["Thick Skin Patches", "Flaking", "Itching"]),
    ("Rosacea", ["Facial Redness", "Swollen Skin", "Visible Blood Vessels"]),
    ("Fungal Infection", ["Itchy Skin", "Red Patches", "Peeling"]),
    ("Vitiligo", ["White Patches", "Loss of Pigment", "Skin Sensitivity"]),
    ("Ringworm", ["Circular Rash", "Itching", "Scaling"]),
    ("Acne Vulgaris", ["Pimples", "Oily Skin", "Scars"]),

    # Headaches
    ("Migraine", ["Throbbing Headache", "Nausea", "Sensitivity to Light"]),
    ("Tension Headache", ["Mild Pressure", "Forehead Pain", "Neck Pain"]),
    ("Cluster Headache", ["Severe Pain near Eye", "Watery Eye", "Restlessness"]),

    # Infections & Others
    ("Tuberculosis", ["Chronic Cough", "Night Sweats", "Weight Loss"]),
    ("HIV/AIDS", ["Fatigue", "Swollen Lymph Nodes", "Frequent Infections"]),
    ("Cholera", ["Severe Diarrhea", "Dehydration", "Vomiting"]),
    ("Measles", ["Rash", "Fever", "Cough"]),
    ("Mumps", ["Swollen Cheeks", "Fever", "Headache"]),
    ("Chickenpox", ["Itchy Blisters", "Fever", "Fatigue"]),
    ("Swine Flu", ["Fever", "Body Aches", "Sore Throat"]),

    # Respiratory Disorders
    ("Chronic Bronchitis", ["Productive Cough", "Chest Tightness", "Shortness of Breath"]),
    ("COPD", ["Wheezing", "Cough with Mucus", "Breathlessness"]),
    ("Sleep Apnea", ["Snoring", "Daytime Fatigue", "Gasping During Sleep"]),

    # Neurological Disorders
    ("Epilepsy", ["Seizures", "Loss of Consciousness", "Confusion"]),
    ("Parkinson’s Disease", ["Tremor", "Muscle Stiffness", "Slow Movement"]),
    ("Alzheimer’s Disease", ["Memory Loss", "Confusion", "Difficulty Speaking"]),
    ("Multiple Sclerosis", ["Tingling", "Vision Problems", "Weakness"]),
    ("Stroke", ["Sudden Numbness", "Slurred Speech", "Dizziness"]),

    # Digestive Issues
    ("IBS", ["Bloating", "Cramping", "Constipation or Diarrhea"]),
    ("GERD", ["Heartburn", "Regurgitation", "Chest Discomfort"]),
    ("Lactose Intolerance", ["Bloating", "Gas", "Stomach Pain after Dairy"]),
    ("Crohn’s Disease", ["Abdominal Cramps", "Diarrhea", "Weight Loss"]),
    ("Ulcerative Colitis", ["Bloody Diarrhea", "Fatigue", "Fever"]),

    # Endocrine Disorders
    ("Hyperthyroidism", ["Weight Loss", "Rapid Heartbeat", "Anxiety"]),
    ("Hypothyroidism", ["Weight Gain", "Fatigue", "Dry Skin"]),
    ("Cushing's Syndrome", ["Round Face", "Weight Gain", "High BP"]),
    ("Addison's Disease", ["Dark Skin", "Low BP", "Fatigue"]),

    # Nutritional
    ("Scurvy", ["Bleeding Gums", "Weakness", "Joint Pain"]),
    ("Rickets", ["Bone Pain", "Delayed Growth", "Muscle Weakness"]),
    ("Pellagra", ["Diarrhea", "Dermatitis", "Dementia"]),

    # Autoimmune Diseases
    ("Lupus", ["Butterfly Rash", "Joint Pain", "Photosensitivity"]),
    ("Rheumatoid Arthritis", ["Joint Pain", "Morning Stiffness", "Swelling"]),
    ("Celiac Disease", ["Bloating", "Weight Loss", "Diarrhea"]),
    ("Sjögren's Syndrome", ["Dry Eyes", "Dry Mouth", "Joint Pain"]),
    ("Graves' Disease", ["Heat Intolerance", "Weight Loss", "Rapid Heartbeat"]),

    # Musculoskeletal Conditions
    ("Osteoarthritis", ["Joint Stiffness", "Pain", "Decreased Range of Motion"]),
    ("Gout", ["Joint Swelling", "Redness", "Sudden Intense Pain"]),
    ("Tendonitis", ["Localized Pain", "Swelling", "Tenderness"]),
    ("Scoliosis", ["Uneven Shoulders", "Back Pain", "Curve in Spine"]),
    ("Fibromyalgia", ["Widespread Pain", "Fatigue", "Memory Issues"]),

    # Psychiatric & Behavioral Disorders
    ("Depression", ["Persistent Sadness", "Sleep Problems", "Loss of Interest"]),
    ("Anxiety", ["Nervousness", "Rapid Breathing", "Restlessness"]),
    ("PTSD", ["Nightmares", "Flashbacks", "Avoidance"]),
    ("Bipolar Disorder", ["Mood Swings", "Irritability", "Euphoria or Depression"]),
    ("Schizophrenia", ["Hallucinations", "Delusions", "Disorganized Speech"]),

    # Blood Disorders
    ("Anemia", ["Fatigue", "Pale Skin", "Shortness of Breath"]),
    ("Thalassemia", ["Fatigue", "Jaundice", "Bone Deformities"]),
    ("Sickle Cell Anemia", ["Pain Crises", "Swelling", "Anemia"]),
    ("Hemophilia", ["Excessive Bleeding", "Joint Pain", "Bruising"]),
    ("Iron Deficiency Anemia", ["Dizziness", "Cold Hands/Feet", "Weakness"]),

    # Pediatric Infections
    ("Rotavirus", ["Watery Diarrhea", "Fever", "Vomiting"]),
    ("Hand, Foot, and Mouth Disease", ["Rash", "Fever", "Mouth Sores"]),
    ("Tonsillitis", ["Sore Throat", "Swollen Tonsils", "Fever"]),
    ("Whooping Cough", ["Severe Coughing", "Vomiting", "Fatigue"]),
    ("Scarlet Fever", ["Red Rash", "Fever", "Sore Throat"]),

    # Ear/Nose/Throat
    ("Otitis Media", ["Ear Pain", "Fever", "Hearing Loss"]),
    ("Sinusitis", ["Facial Pressure", "Nasal Congestion", "Headache"]),
    ("Tonsillitis", ["Painful Swallowing", "Swollen Tonsils", "Fever"]),
    ("Meniere’s Disease", ["Vertigo", "Hearing Loss", "Tinnitus"]),
    ("Labyrinthitis", ["Vertigo", "Nausea", "Balance Issues"]),

    # Eye Disorders
    ("Cataract", ["Blurred Vision", "Faded Colors", "Halos Around Lights"]),
    ("Glaucoma", ["Eye Pain", "Tunnel Vision", "Headache"]),
    ("Macular Degeneration", ["Central Vision Loss", "Blurry Spots", "Distorted Lines"]),
    ("Conjunctivitis", ["Red Eye", "Discharge", "Itching"]),
    ("Retinal Detachment", ["Flashes of Light", "Floaters", "Shadow over Vision"]),

    # Reproductive Health
    ("Polycystic Ovary Syndrome", ["Irregular Periods", "Facial Hair", "Acne"]),
    ("Endometriosis", ["Pelvic Pain", "Painful Periods", "Infertility"]),
    ("Menopause", ["Hot Flashes", "Mood Swings", "Vaginal Dryness"]),
    ("Ectopic Pregnancy", ["Abdominal Pain", "Vaginal Bleeding", "Dizziness"]),
    ("Ovarian Cyst", ["Pelvic Pressure", "Bloating", "Pain During Intercourse"]),

    # Emergency Cases
    ("Heat Stroke", ["Body Temperature >104°F", "Confusion", "No Sweating"]),
    ("Sepsis", ["Rapid Breathing", "Low BP", "Altered Mental State"]),
    ("Anaphylaxis", ["Breathing Difficulty", "Swelling", "Hives"]),
    ("Poisoning", ["Nausea", "Confusion", "Convulsions"]),
    ("Snake Bite", ["Puncture Marks", "Swelling", "Paralysis"]),

    # Rare Conditions
    ("Marfan Syndrome", ["Tall Stature", "Flexible Joints", "Heart Problems"]),
    ("Ehlers-Danlos Syndrome", ["Hypermobile Joints", "Fragile Skin", "Chronic Pain"]),
    ("Wilson's Disease", ["Liver Dysfunction", "Neurological Symptoms", "Copper Rings in Eyes"]),
    ("ALS (Lou Gehrig’s)", ["Muscle Weakness", "Slurred Speech", "Twitching"]),
    ("Tourette Syndrome", ["Motor Tics", "Vocal Tics", "Uncontrollable Movements"]),
]

# Medication mapping for specified diseases
medication_mapping = {
    # Allergies
    "Skin Allergy": "Antihistamines (e.g., Cetirizine, Loratadine), Hydrocortisone cream",
    "Dust Allergy": "Loratadine, Nasal corticosteroids, Air purifiers",
    "Food Allergy": "Epinephrine (auto-injector for anaphylaxis), Antihistamines",
    "Pollen Allergy": "Nasal corticosteroids, Antihistamines, Leukotriene modifiers",
    "Pet Allergy": "Antihistamines, Nasal sprays, Allergen immunotherapy",

    # Asthma Types
    "Allergic Asthma": "Inhaled corticosteroids (Fluticasone), Leukotriene inhibitors (Montelukast), Albuterol",
    "Exercise-Induced Asthma": "Short-acting beta agonists (Albuterol) before activity, Warm-up exercises",
    "Occupational Asthma": "Inhaled corticosteroids, Bronchodilators, Avoidance of workplace triggers",

    # Fever Types
    "Viral Fever": "Paracetamol (Acetaminophen), Ibuprofen, Hydration, Rest",
    "Typhoid Fever": "Ciprofloxacin, Azithromycin (for resistant strains), Adequate fluid intake",
    "Dengue Fever": "Acetaminophen (Avoid NSAIDs like Ibuprofen), Oral rehydration, Hospital monitoring if severe",
    "Malaria Fever": "Artemether-lumefantrine, Chloroquine (if sensitive), Quinine for severe cases",

    # Diabetes Types
    "Type 1 Diabetes": "Insulin therapy (short-acting, long-acting), Blood sugar monitoring, Diet management",
    "Type 2 Diabetes": "Metformin, Sulfonylureas, Lifestyle changes, Blood glucose monitoring",
    "Gestational Diabetes": "Insulin (if needed), Diet control, Regular glucose checks",

    # Hepatitis Types
    "Hepatitis A": "Rest, Hydration, Avoid alcohol, Symptom relief",
    "Hepatitis B": "Antiviral medications (Tenofovir, Entecavir), Liver monitoring",
    "Hepatitis C": "Direct-acting antivirals (Sofosbuvir, Ledipasvir), Liver function monitoring",

    # Heart Diseases
    "Heart Attack": "Aspirin, Nitroglycerin, Beta-blockers, Emergency PCI",
    "Arrhythmia": "Antiarrhythmics (Amiodarone), Beta-blockers, Pacemaker (if required)",
    "Heart Failure": "ACE inhibitors, Diuretics, Beta-blockers, Lifestyle changes",
    "Angina": "Nitrates, Beta-blockers, Calcium channel blockers, Aspirin",
    "Cardiomyopathy": "ACE inhibitors, Diuretics, Implantable devices (if needed)",

    # Cancers (General)
    "Lung Cancer": "Chemotherapy, Targeted therapy, Surgery, Radiation",
    "Breast Cancer": "Surgery, Chemotherapy, Radiation, Hormonal therapy",
    "Colon Cancer": "Surgery, Chemotherapy, Targeted therapy",
    "Skin Cancer": "Surgical excision, Cryotherapy, Topical treatments",
    "Prostate Cancer": "Hormone therapy, Surgery, Radiation, Active surveillance",
    "Leukemia - AML": "Chemotherapy, Bone marrow transplant, Supportive care",
    "Glioblastoma": "Surgical resection, Radiation therapy, Temozolomide",
    "Meningioma": "Surgery, Radiation (if large or recurrent), Monitoring small tumors",

    # Skin Conditions
    "Eczema": "Topical corticosteroids, Moisturizers, Antihistamines for itching",
    "Psoriasis": "Topical corticosteroids, Vitamin D analogues, Biologic injections (e.g., Adalimumab)",
    "Rosacea": "Topical metronidazole, Oral doxycycline, Avoidance of triggers",
    "Fungal Infection": "Antifungal creams (Clotrimazole, Miconazole), Oral antifungals if widespread",
    "Vitiligo": "Topical corticosteroids, Calcineurin inhibitors, Phototherapy (UVB)",
    "Ringworm": "Topical antifungal creams (Terbinafine, Clotrimazole), Keep area dry",
    "Acne Vulgaris": "Topical retinoids, Benzoyl peroxide, Oral antibiotics (Doxycycline)",

    # Headaches
    "Migraine": "Triptans (Sumatriptan), NSAIDs, Anti-nausea meds, Preventives like propranolol",
    "Tension Headache": "Acetaminophen, Ibuprofen, Stress management, Regular sleep",
    "Cluster Headache": "Oxygen therapy, Sumatriptan injections, Preventive meds (Verapamil)",

    # Infections & Others
    "Tuberculosis": "Isoniazid, Rifampicin, Ethambutol, Pyrazinamide (6-month regimen)",
    "HIV/AIDS": "Antiretroviral therapy (ART) - Tenofovir, Efavirenz, Lamivudine",
    "Cholera": "Oral rehydration salts (ORS), Doxycycline or Azithromycin (severe cases)",
    "Measles": "Supportive care (Vitamin A, fluids), Isolation to prevent spread",
    "Mumps": "Pain relievers (Ibuprofen), Cold compress, Supportive care",
    "Chickenpox": "Antihistamines, Calamine lotion, Acyclovir (for high-risk cases)",
    "Swine Flu": "Oseltamivir (Tamiflu), Rest, Fluids, Paracetamol for fever",

    # Respiratory Disorders
    "Chronic Bronchitis": "Bronchodilators (Albuterol), Inhaled steroids, Smoking cessation",
    "COPD": "Bronchodilators, Inhaled corticosteroids, Oxygen therapy, Pulmonary rehab",
    "Sleep Apnea": "CPAP machine, Weight loss, Avoid alcohol/sedatives, Surgery in some cases",

    # Neurological Disorders
    "Epilepsy": "Antiepileptic drugs (Carbamazepine, Valproate), Lifestyle modification",
    "Parkinson’s Disease": "Levodopa, Carbidopa, MAO-B inhibitors, Physical therapy",
    "Alzheimer’s Disease": "Donepezil, Rivastigmine, Memory training, Supportive care",
    "Multiple Sclerosis": "Interferon beta, Corticosteroids, Physical therapy, Disease-modifying drugs",
    "Stroke": "Aspirin, Thrombolytics (if early), Blood pressure control, Physical rehab",

    # Digestive Issues
    "IBS": "Antispasmodics (Dicyclomine), Fiber supplements, Stress management",
    "GERD": "Proton pump inhibitors (Omeprazole), Antacids, Lifestyle changes",
    "Lactose Intolerance": "Lactase enzyme supplements, Dairy-free diet",
    "Crohn’s Disease": "Corticosteroids, Immunosuppressants (Azathioprine), Biologics (Infliximab)",
    "Ulcerative Colitis": "Mesalamine, Corticosteroids, Immune modulators",

    # Endocrine Disorders
    "Hyperthyroidism": "Methimazole, Beta-blockers (Propranolol), Radioactive iodine therapy",
    "Hypothyroidism": "Levothyroxine (T4), Regular TSH monitoring",
    "Cushing's Syndrome": "Surgical removal of tumor, Ketoconazole (if surgery not feasible)",
    "Addison's Disease": "Hydrocortisone, Fludrocortisone, Increased salt intake",

    # Nutritional
    "Scurvy": "Vitamin C supplements, Citrus fruits, Leafy greens",
    "Rickets": "Vitamin D and calcium supplements, Sunlight exposure",
    "Pellagra": "Niacin (Vitamin B3) supplementation, Balanced diet with protein",

    # Autoimmune Diseases
    "Lupus": "Hydroxychloroquine, Corticosteroids, Immunosuppressants",
    "Rheumatoid Arthritis": "NSAIDs, Methotrexate, Biologic agents (Etanercept, Adalimumab)",
    "Celiac Disease": "Strict gluten-free diet, Vitamin supplements",
    "Sjögren's Syndrome": "Artificial tears, Saliva stimulants, Hydroxychloroquine",
    "Graves' Disease": "Methimazole, Beta-blockers, Radioactive iodine therapy",

    # Musculoskeletal Conditions
    "Osteoarthritis": "NSAIDs, Physical therapy, Joint replacement (in severe cases)",
    "Gout": "Colchicine, Allopurinol, Low-purine diet",
    "Tendonitis": "Rest, Ice, NSAIDs, Physiotherapy",
    "Scoliosis": "Back brace (in children), Physical therapy, Surgery (in severe cases)",
    "Fibromyalgia": "Pain relievers, Antidepressants (Duloxetine), Exercise therapy",

    # Psychiatric & Behavioral Disorders
    "Depression": "SSRIs (Fluoxetine, Sertraline), CBT, Lifestyle changes",
    "Anxiety": "Benzodiazepines (short-term), SSRIs, Exposure therapy",
    "PTSD": "CBT, EMDR therapy, SSRIs (Paroxetine, Sertraline)",
    "Bipolar Disorder": "Mood stabilizers (Lithium), Antipsychotics, Psychotherapy",
    "Schizophrenia": "Antipsychotic medications (Olanzapine, Risperidone), Therapy",

    # Blood Disorders
    "Anemia": "Iron supplements, Folate, Vitamin B12, Treat underlying cause",
    "Thalassemia": "Regular blood transfusions, Iron chelation therapy, Folic acid",
    "Sickle Cell Anemia": "Hydroxyurea, Pain relievers, Blood transfusions",
    "Hemophilia": "Clotting factor replacement therapy, Desmopressin (mild cases)",
    "Iron Deficiency Anemia": "Iron-rich diet, Ferrous sulfate tablets, Vitamin C",

    # Pediatric Infections
    "Rotavirus": "Oral rehydration therapy, Zinc supplementation, Rotavirus vaccine (prevention)",
    "Hand, Foot, and Mouth Disease": "Topical mouth pain relievers, Fever reducers, Hydration",
    "Tonsillitis": "Amoxicillin or Penicillin (if bacterial), Salt water gargle, Pain relievers",
    "Whooping Cough": "Azithromycin or Erythromycin (early stages), Cough suppressants",
    "Scarlet Fever": "Penicillin, Paracetamol or Ibuprofen for fever and sore throat",

    # Ear/Nose/Throat
    "Otitis Media": "Amoxicillin, Ibuprofen or Paracetamol for pain, Warm compress",
    "Sinusitis": "Nasal decongestants, Saline nasal spray, Amoxicillin (if bacterial)",
    "Meniere’s Disease": "Diuretics, Betahistine, Antiemetics",
    "Labyrinthitis": "Meclizine, Antiemetics, Corticosteroids (if viral origin)",

    # Eye Disorders
    "Cataract": "Surgical removal and lens replacement (no medication to reverse)",
    "Glaucoma": "Timolol, Latanoprost, Surgery for intraocular pressure control",
    "Macular Degeneration": "Anti-VEGF injections (e.g., Ranibizumab), Zinc and antioxidant vitamins",
    "Conjunctivitis": "Antibiotic/antiviral/antihistamine drops depending on cause",
    "Retinal Detachment": "Emergency surgery (no medication can reverse detachment)",

     # ✅ Reproductive Health
    "Polycystic Ovary Syndrome": "Metformin, Hormonal birth control, Spironolactone for acne",
    "Endometriosis": "NSAIDs (Ibuprofen), Hormonal therapy (GnRH agonists), Surgery (laparoscopy)",
    "Menopause": "Hormone Replacement Therapy (HRT), Vaginal estrogen, SSRIs for mood swings",
    "Ectopic Pregnancy": "Methotrexate (early stages), Emergency surgery (if ruptured)",
    "Ovarian Cyst": "Pain relievers (Ibuprofen), Hormonal contraceptives, Surgery if large/persistent",

    # 🚨 Emergency Cases
    "Heat Stroke": "Immediate cooling, IV fluids, Hospitalization (emergency care)",
    "Sepsis": "IV antibiotics, Vasopressors, ICU support (lifesaving emergency)",
    "Anaphylaxis": "Intramuscular Epinephrine (Adrenaline), Antihistamines, Oxygen therapy",
    "Poisoning": "Activated charcoal, Antidote (if known), Hospital emergency treatment",
    "Snake Bite": "Antivenom, Supportive care, Tetanus prophylaxis",

    # 🧬 Rare Conditions
    "Marfan Syndrome": "Beta-blockers, Losartan, Regular heart monitoring, Surgery (if needed)",
    "Ehlers-Danlos Syndrome": "Pain management, Physical therapy, Protective braces/supports",
    "Wilson's Disease": "Penicillamine, Trientine (copper chelators), Zinc supplements",
    "ALS (Lou Gehrig’s)": "Riluzole, Edaravone, Supportive care (physiotherapy, speech therapy)",
    "Tourette Syndrome": "Haloperidol, Clonidine, Behavioral therapy (CBIT)",
}

# Definition of diseases
disease_definitions = {
    "Skin Allergy": "An immune response that causes skin irritation, itching, redness, and rashes due to contact with allergens.",
    "Dust Allergy": "An allergic reaction triggered by inhaling dust particles, including mites and debris, leading to sneezing and nasal issues.",
    "Food Allergy": "A potentially serious immune response to certain foods causing symptoms like swelling, hives, vomiting, or anaphylaxis.",
    "Pollen Allergy": "Also called hay fever, it occurs when the immune system reacts to pollen, causing sneezing, nasal congestion, and itchy eyes.",
    "Pet Allergy": "A hypersensitivity to proteins found in pet dander, saliva, or urine, causing respiratory and skin symptoms.",

    "Allergic Asthma": "A type of asthma triggered by exposure to allergens like pollen, dust, or pet dander, leading to airway inflammation.",
    "Exercise-Induced Asthma": "A form of asthma triggered during or after physical activity, causing coughing, wheezing, and breathlessness.",
    "Occupational Asthma": "Asthma caused by exposure to irritants or allergens in the workplace such as fumes, chemicals, or dust.",

    "Viral Fever": "Fever caused by a viral infection, often accompanied by body aches, fatigue, sore throat, and general discomfort.",
    "Typhoid Fever": "A bacterial infection caused by Salmonella typhi, resulting in high fever, abdominal pain, and weakness.",
    "Dengue Fever": "A mosquito-borne viral illness causing high fever, rash, joint pain, and in severe cases, bleeding and organ damage.",
    "Malaria Fever": "A mosquito-transmitted disease caused by Plasmodium parasites, leading to chills, fever, and flu-like symptoms.",

    "Type 1 Diabetes": "A chronic condition where the pancreas produces little or no insulin, requiring insulin therapy from an early age.",
    "Type 2 Diabetes": "A metabolic disorder where the body resists insulin or doesn’t produce enough, often managed with lifestyle and medication.",
    "Gestational Diabetes": "High blood sugar that develops during pregnancy and usually resolves after delivery but requires monitoring and management.",

    "Hepatitis A": "A viral infection that inflames the liver, spread through contaminated food or water; usually self-limiting.",
    "Hepatitis B": "A serious liver infection caused by the hepatitis B virus, spread through bodily fluids, which can become chronic.",
    "Hepatitis C": "A liver infection caused by the hepatitis C virus, often transmitted through blood and can lead to long-term liver damage.",

    "Heart Attack": "A medical emergency where blood flow to the heart is blocked, causing damage to heart muscle tissue.",
    "Arrhythmia": "A condition characterized by irregular heartbeat rhythms that may be too fast, too slow, or erratic.",
    "Heart Failure": "A chronic condition where the heart cannot pump enough blood to meet the body's needs.",
    "Angina": "Chest pain or discomfort caused by reduced blood flow to the heart muscles, often triggered by stress or activity.",
    "Cardiomyopathy": "A disease of the heart muscle that affects its size, shape, and structure, leading to reduced function.",

    "Lung Cancer": "A type of cancer that begins in the lungs, often linked to smoking, and may spread quickly if untreated.",
    "Breast Cancer": "A malignant tumor that develops in the cells of the breast, commonly found in women but also occurs in men.",
    "Colon Cancer": "Cancer of the large intestine (colon), usually beginning with benign polyps that can become cancerous over time.",
    "Skin Cancer": "A growth of abnormal skin cells caused by DNA damage, often due to sun exposure or tanning beds.",
    "Prostate Cancer": "A slow-growing cancer in the prostate gland found in men, sometimes detected through PSA blood tests.",
    "Leukemia - AML": "A rapid-forming cancer of the blood and bone marrow characterized by the overproduction of immature white cells.",
    "Glioblastoma": "An aggressive and fast-growing brain tumor that arises from glial cells and is difficult to treat.",
    "Meningioma": "A usually benign tumor that arises from the membranes surrounding the brain and spinal cord, potentially causing pressure symptoms.",

    "Eczema": "A chronic skin condition causing red, itchy, and inflamed patches, often triggered by allergens or irritants.",
    "Psoriasis": "An autoimmune skin disorder that speeds up skin cell production, causing scaling and inflammation.",
    "Rosacea": "A chronic skin condition that causes facial redness, swelling, and visible blood vessels, especially on the cheeks and nose.",
    "Fungal Infection": "A skin condition caused by fungi that typically results in redness, itching, and peeling in moist body areas.",
    "Vitiligo": "A condition in which the skin loses its pigment cells, leading to white patches on various parts of the body.",
    "Ringworm": "A contagious fungal skin infection characterized by a red, ring-shaped rash that itches and may scale.",
    "Acne Vulgaris": "A common skin condition that occurs when hair follicles become clogged with oil and dead skin cells, causing pimples and cysts.",

    "Migraine": "A neurological disorder marked by intense headaches, often on one side, with nausea and sensitivity to light or sound.",
    "Tension Headache": "The most common type of headache characterized by mild to moderate pressure across the forehead or back of the neck.",
    "Cluster Headache": "A rare type of headache involving severe, recurring pain usually around one eye, often accompanied by watery eyes and nasal congestion.",

    "Tuberculosis": "A contagious bacterial infection primarily affecting the lungs, spread through air droplets.",
    "HIV/AIDS": "A chronic immune system condition caused by the HIV virus, leading to vulnerability to infections and cancers.",
    "Cholera": "A bacterial infection causing severe diarrhea and dehydration, usually spread through contaminated water.",
    "Measles": "A highly contagious viral disease that causes fever, rash, and cough, often preventable through vaccination.",
    "Mumps": "A viral infection of the salivary glands causing painful swelling in the cheeks and jaw.",
    "Chickenpox": "A viral infection causing an itchy skin rash with small, fluid-filled blisters, mostly in children.",
    "Swine Flu": "A flu virus strain (H1N1) initially found in pigs, causing respiratory illness in humans.",

    "Chronic Bronchitis": "A long-term inflammation of the bronchial tubes, often caused by smoking, leading to coughing and mucus production.",
    "COPD": "A progressive lung disease that obstructs airflow and makes breathing difficult, commonly due to smoking.",
    "Sleep Apnea": "A sleep disorder characterized by repeated pauses in breathing during sleep, leading to daytime fatigue.",

    "Epilepsy": "A neurological disorder involving recurrent seizures due to abnormal brain activity.",
    "Parkinson’s Disease": "A progressive nervous system disorder affecting movement, often including tremors and stiffness.",
    "Alzheimer’s Disease": "A degenerative brain disorder that gradually destroys memory, thinking skills, and the ability to carry out tasks.",
    "Multiple Sclerosis": "An autoimmune disease where the immune system attacks the protective covering of nerves, causing communication problems between brain and body.",
    "Stroke": "A medical emergency where blood flow to a part of the brain is interrupted or reduced, depriving it of oxygen.",

    "IBS": "A chronic gastrointestinal disorder causing abdominal discomfort, bloating, and changes in bowel habits.",
    "GERD": "A digestive disorder where stomach acid frequently flows back into the esophagus, irritating its lining.",
    "Lactose Intolerance": "A condition in which the body cannot digest lactose, a sugar found in milk and dairy products.",
    "Crohn’s Disease": "A type of inflammatory bowel disease that can affect any part of the gastrointestinal tract, causing severe inflammation.",
    "Ulcerative Colitis": "An inflammatory bowel disease causing long-lasting inflammation and ulcers in the colon and rectum.",

    "Hyperthyroidism": "A condition where the thyroid gland produces excessive thyroid hormones, leading to a fast metabolism and symptoms like anxiety, weight loss, and palpitations.",
    "Hypothyroidism": "A condition where the thyroid gland produces insufficient thyroid hormones, causing fatigue, weight gain, and cold intolerance.",
    "Cushing's Syndrome": "A hormonal disorder caused by high levels of cortisol, often due to steroid use or adrenal tumors.",
    "Addison's Disease": "A rare disorder where the adrenal glands fail to produce enough hormones, particularly cortisol and aldosterone.",

    "Scurvy": "A disease caused by vitamin C deficiency, leading to gum bleeding, weakness, and joint pain.",
    "Rickets": "A childhood condition caused by vitamin D deficiency, resulting in soft and weak bones.",
    "Pellagra": "A disease resulting from niacin (vitamin B3) deficiency, characterized by diarrhea, dermatitis, and dementia.",

    "Lupus": "A chronic autoimmune condition in which the immune system attacks healthy tissues, affecting skin, joints, and organs.",
    "Rheumatoid Arthritis": "An autoimmune disorder that causes chronic inflammation in the joints, leading to pain and stiffness.",
    "Celiac Disease": "An autoimmune disorder triggered by gluten intake, damaging the lining of the small intestine.",
    "Sjögren's Syndrome": "An autoimmune condition that targets moisture-producing glands, causing dry eyes and mouth.",
    "Graves' Disease": "An autoimmune disorder leading to overproduction of thyroid hormones (hyperthyroidism).",

    "Osteoarthritis": "A degenerative joint disease caused by the breakdown of cartilage and underlying bone, leading to joint pain and stiffness.",
    "Gout": "A type of arthritis caused by excess uric acid crystals in the joints, resulting in intense pain and inflammation.",
    "Tendonitis": "Inflammation of a tendon due to overuse or injury, commonly seen in the shoulder, elbow, or knee.",
    "Scoliosis": "A condition where the spine curves sideways, often developing in adolescence.",
    "Fibromyalgia": "A disorder characterized by widespread musculoskeletal pain, fatigue, and memory issues.",

    "Depression": "A mental health disorder marked by persistent sadness, lack of interest, and emotional disturbances.",
    "Anxiety": "A mental health condition characterized by excessive worry, restlessness, and fear.",
    "PTSD": "A psychiatric disorder triggered by experiencing or witnessing a traumatic event, leading to flashbacks and anxiety.",
    "Bipolar Disorder": "A mental condition involving episodes of mood swings from depressive lows to manic highs.",
    "Schizophrenia": "A severe mental disorder involving delusions, hallucinations, disorganized thinking, and impaired functioning.",

    "Anemia": "A condition where the body lacks enough healthy red blood cells to carry adequate oxygen to tissues.",
    "Thalassemia": "A genetic blood disorder that causes the body to make abnormal hemoglobin, leading to anemia.",
    "Sickle Cell Anemia": "An inherited red blood cell disorder causing cells to become misshapen, leading to pain and complications.",
    "Hemophilia": "A rare bleeding disorder in which the blood doesn’t clot properly due to missing clotting factors.",
    "Iron Deficiency Anemia": "A common type of anemia caused by insufficient iron, resulting in fatigue and weakness.",

    "Rotavirus": "A contagious virus that causes diarrhea and vomiting in infants and young children.",
    "Hand, Foot, and Mouth Disease": "A viral illness causing mouth sores, skin rash, and fever, mostly affecting young children.",
    "Tonsillitis": "Inflammation of the tonsils due to viral or bacterial infection, causing sore throat and fever.",
    "Whooping Cough": "A bacterial respiratory infection marked by uncontrollable, violent coughing, especially dangerous in infants.",
    "Scarlet Fever": "A bacterial illness that develops in some people with strep throat, featuring a red rash and sore throat.",

    "Otitis Media": "A middle ear infection that causes ear pain, fever, and hearing problems, common in children.",
    "Sinusitis": "Inflammation or swelling of the sinuses often due to infection, allergies, or cold.",
    "Meniere’s Disease": "A disorder of the inner ear causing vertigo, hearing loss, and ringing in the ears.",
    "Labyrinthitis": "An inner ear infection leading to dizziness, balance issues, and sometimes hearing loss.",

    "Cataract": "A clouding of the eye's natural lens, leading to blurred vision, often treated with surgery.",
    "Glaucoma": "A group of eye conditions that damage the optic nerve, usually due to high eye pressure.",
    "Macular Degeneration": "An age-related disease that blurs central vision, affecting reading and facial recognition.",
    "Conjunctivitis": "Also called pink eye, it's inflammation of the conjunctiva, often due to infection or allergy.",
    "Retinal Detachment": "An emergency eye condition where the retina pulls away from supportive tissue, causing vision loss.",

    "Polycystic Ovary Syndrome": "A hormonal imbalance in women causing irregular periods, cysts in ovaries, and infertility.",
    "Endometriosis": "A condition where tissue similar to the uterine lining grows outside the uterus, causing pain and fertility issues.",
    "Menopause": "The natural end of menstrual cycles in women, marked by hot flashes, mood changes, and hormonal shifts.",
    "Ectopic Pregnancy": "A pregnancy where the fertilized egg implants outside the uterus, often in a fallopian tube, which is life-threatening.",
    "Ovarian Cyst": "A fluid-filled sac on or in an ovary, often harmless but sometimes causing pain or complications.",

    "Heat Stroke": "A life-threatening condition caused by prolonged heat exposure, resulting in high body temperature and confusion.",
    "Sepsis": "A dangerous response to infection causing widespread inflammation and organ failure, requiring immediate medical care.",
    "Anaphylaxis": "A severe allergic reaction leading to breathing difficulty, drop in blood pressure, and potential death if untreated.",
    "Poisoning": "The harmful effects of substances swallowed, inhaled, or absorbed, potentially life-threatening without prompt care.",
    "Snake Bite": "Injury from a snake’s fangs that can inject venom and cause swelling, paralysis, or organ damage depending on species.",

    "Marfan Syndrome": "A genetic disorder affecting connective tissue, leading to tall stature, heart problems, and flexible joints.",
    "Ehlers-Danlos Syndrome": "A group of connective tissue disorders causing hypermobile joints, fragile skin, and chronic pain.",
    "Wilson's Disease": "A rare inherited disorder where copper builds up in the body, affecting liver and brain functions.",
    "ALS (Lou Gehrig’s)": "A neurodegenerative disease that weakens muscles and impacts physical function over time.",
    "Tourette Syndrome": "A neurological condition characterized by repetitive, involuntary movements and vocalizations called tics." 
}

# Expand base list to generate 300 diseases
diseases = []
for i in range(1, 21):  # Multiply to reach 300
    for name, symptoms in base_diseases:
        diseases.append((f"{name}_{i}", symptoms))

# Create a complete list with severity levels for each disease
complete_data = []

for disease_id, symptoms in diseases:
    base_name = disease_id.split("_")[0]  # Extract base name from disease ID if needed

    for severity_level, temp_range in severity_levels.items():
        complete_data.append({
            "disease": disease_id,
            "definition": disease_definitions.get(base_name, "Definition not available"),
            "symptoms": ", ".join(symptoms),
            "severity": severity_level,
            "temperature_range": f"{temp_range[0]}°C to {temp_range[1]}°C",
            "medications": medication_mapping.get(base_name, "Consult a healthcare provider"),
            "advice": severity_advice.get(severity_level, "Follow medical guidance")
        })
        
# Convert to DataFrame
df = pd.DataFrame(complete_data)

# Save to CSV if needed
df.to_csv("disease_dataset.csv", index=False)

# Display sample
print(df.head(10))

# Create DataFrame and save
df = pd.DataFrame(complete_data)
df.to_csv("structured_healthcare_dataset.csv", index=False)
df.to_excel("structured_healthcare_dataset.xlsx", index=False)

print("✅ Structured dataset with 300 diseases saved successfully.")
