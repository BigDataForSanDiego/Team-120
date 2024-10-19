
def generate_questions_and_autopopulate(profile):
    questions = {}
    missing_questions = []

    # Basic Info
    questions["Name"] = profile.get("name", "Missing")
    questions["Date of birth"] = profile.get("date_of_birth", "Missing")
    questions["Doctor"] = profile.get("doctor", "Missing")
    questions["Phone number"] = profile.get("phone_number", "Missing")
    questions["Sex"] = profile.get("sex", "Missing")
    questions["Preferred language"] = profile.get("language", "Missing")
    questions["Occupation"] = profile.get("occupation", "Missing")

    # Medical Illnesses
    illnesses = profile.get("medical_illnesses", {})
    conditions = [
        ("Do you have cancer?", "cancer"),
        ("Do you have alcoholism or drug addiction?", "alcoholism_drug_addiction"),
        ("Do you have glaucoma?", "glaucoma"),
        ("Do you have HIV?", "HIV"),
        ("Do you have seizures?", "seizures"),
        ("Do you have blood clots?", "blood_clots"),
        ("Do you have heart disease?", "heart_disease"),
        ("Do you have kidney disease?", "kidney_disease"),
        ("Have you had strokes?", "strokes"),
        ("Do you suffer from depression or anxiety?", "depression_anxiety"),
        ("Do you have hepatitis?", "hepatitis"),
        ("Do you have lung disease?", "lung_disease"),
        ("Do you have a thyroid condition?", "thyroid_condition"),
        ("Do you have diabetes?", "diabetes"),
        ("Do you have high blood pressure?", "high_blood_pressure"),
        ("Do you suffer from migraines?", "migraines")
    ]

    for question, condition in conditions:
        if condition in illnesses:
            questions[question] = "Yes" if illnesses[condition] else "No"
        else:
            questions[question] = "Missing"
            missing_questions.append(question)

    questions["Anything else about your medical history?"] = illnesses.get(
        "other_medical_conditions", "Missing")

    # Surgeries
    if profile.get("surgeries"):
        surgeries = profile["surgeries"]
        surgeries_list = [f"{surgery['type']} on {
            surgery['date']}" for surgery in surgeries]
        questions["Have you had any surgeries?"] = ", ".join(surgeries_list)
    else:
        questions["Have you had any surgeries?"] = "Missing"
        missing_questions.append("Have you had any surgeries?")

    # Other Visits
    if profile.get("hospitalizations"):
        visits = profile["hospitalizations"]
        visit_list = [f"{visit['type']} on {
            visit['date']}" for visit in visits]
        questions["Any hospitalizations, ER or urgent care visits?"] = ", ".join(
            visit_list)
    else:
        questions["Any hospitalizations, ER or urgent care visits?"] = "Missing"
        missing_questions.append(
            "Any hospitalizations, ER or urgent care visits?")

    # Medications
    if profile.get("medications"):
        medication_list = [f"{med['name']} ({med['dosage']}, {
            med['frequency']})" for med in profile["medications"]]
        questions["Are you taking any medications?"] = ", ".join(
            medication_list)
    else:
        questions["Are you taking any medications?"] = "Missing"
        missing_questions.append("Are you taking any medications?")

    # Allergies
    if profile.get("allergies"):
        allergy_list = [
            f"{allergy['allergen']} ({allergy['reaction']})" for allergy in profile["allergies"]]
        questions["Do you have any allergies?"] = ", ".join(allergy_list)
    else:
        questions["Do you have any allergies?"] = "Missing"
        missing_questions.append("Do you have any allergies?")

    # Vaccines
    vaccines = profile.get("vaccines", {})
    questions["When was your last Tetanus/Tdap vaccine?"] = vaccines.get(
        "tetanus", "Missing")
    questions["When was your last Flu shot?"] = vaccines.get("flu", "Missing")
    questions["When was your last Shingles vaccine?"] = vaccines.get(
        "shingles", "Missing")
    questions["When was your last Pneumonia vaccine?"] = vaccines.get(
        "pneumonia", "Missing")

    missing_vaccine_questions = [
        "When was your last Tetanus/Tdap vaccine?",
        "When was your last Flu shot?",
        "When was your last Shingles vaccine?",
        "When was your last Pneumonia vaccine?"
    ]

    for question in missing_vaccine_questions:
        if questions[question] == "Missing":
            missing_questions.append(question)

    # Family History
    family_history = profile.get("family_history", {})
    conditions = ["heart_disease", "diabetes", "breast_cancer",
                  "colon_cancer", "depression", "stroke", "thyroid_condition"]
    for condition in conditions:
        family = family_history.get(condition, [])
        questions[f"Does your family have a history of {condition.replace(
            '_', ' ')}?"] = ", ".join(family) if family else "Missing"
        if questions[f"Does your family have a history of {condition.replace('_', ' ')}?"] == "Missing":
            missing_questions.append(f"Does your family have a history of {
                                     condition.replace('_', ' ')}?")

    # Social History
    social_history_fields = [
        ("What is your marital status?", "marital_status"),
        ("What is your sexual orientation?", "sexual_orientation"),
        ("Do you have children?", "children"),
        ("Do you use birth control?", "birth_control"),
        ("Do you live alone?", "live_alone"),
        ("Do you have a history of domestic violence?", "domestic_violence_history")
    ]

    for question, field in social_history_fields:
        if field in profile:
            questions[question] = profile.get(field, "Missing")
        else:
            questions[question] = "Missing"
            missing_questions.append(question)

    # Smoking History
    smoking_status = profile.get("smoking_status", "Missing")
    if smoking_status == "Former smoker":
        questions["Are you a former smoker?"] = f"Yes, quit on {profile.get(
            'date_quit', 'Missing')}, smoked for {profile.get('years_smoked', 'Missing')} years"
    elif smoking_status == "Missing":
        questions["Do you smoke?"] = "Missing"
        missing_questions.append("Do you smoke?")

    # Alcohol Use
    alcohol_use = profile.get("alcohol_use", {})
    questions["Do you have a history of alcohol abuse?"] = "Yes" if alcohol_use.get(
        "history_of_abuse") else "No"
    questions["What is your current level of alcohol use?"] = alcohol_use.get(
        "current_use_level", "Missing")

    if questions["What is your current level of alcohol use?"] == "Missing":
        missing_questions.append("What is your current level of alcohol use?")

    # Drug Use
    drug_use = profile.get("drug_use", {})
    questions["Do you have a history of drug use?"] = ", ".join(
        drug_use.get("past_use", [])) if drug_use.get("past_use") else "Missing"
    questions["Do you currently use drugs?"] = ", ".join(drug_use.get(
        "current_use", [])) if drug_use.get("current_use") else "Missing"

    if questions["Do you have a history of drug use?"] == "Missing":
        missing_questions.append("Do you have a history of drug use?")
    if questions["Do you currently use drugs?"] == "Missing":
        missing_questions.append("Do you currently use drugs?")

    # Caffeine Use
    caffeine = profile.get("caffeine_use", {})
    if caffeine:
        questions["Do you use caffeine?"] = f"Yes, {caffeine.get(
            'type')} ({caffeine.get('ounces_per_day', 'Missing')} oz per day)"
    else:
        questions["Do you use caffeine?"] = "Missing"
        missing_questions.append("Do you use caffeine?")

    # Exercise
    questions["Do you exercise?"] = profile.get(
        "exercise_frequency", "Missing")
    if questions["Do you exercise?"] == "Missing":
        missing_questions.append("Do you exercise?")

    # Colon Cancer Screening
    colon_cancer_screening = profile.get("colon_cancer_screening", {})
    questions["When was your last stool card test?"] = colon_cancer_screening.get(
        "stool_cards", "Missing")
    questions["When was your last sigmoidoscopy?"] = colon_cancer_screening.get(
        "sigmoidoscopy", "Missing")
    questions["When was your last colonoscopy?"] = colon_cancer_screening.get(
        "colonoscopy", "Missing")
    questions["Have you never had a colon cancer screening?"] = "Yes" if colon_cancer_screening.get(
        "never_had_screening") else "No"

    missing_colon_screening_questions = [
        "When was your last stool card test?",
        "When was your last sigmoidoscopy?",
        "When was your last colonoscopy?"
    ]

    for question in missing_colon_screening_questions:
        if questions[question] == "Missing":
            missing_questions.append(question)

    # Pregnancy (For Females)
    questions["Have you ever been pregnant?"] = f"Yes, {profile.get('pregnancy_history', {}).get(
        'number_of_pregnancies', 'Missing')} pregnancies" if profile.get("pregnancy_history") else "Missing"
    questions["How many live births have you had?"] = profile.get(
        "pregnancy_history", {}).get("number_of_live_births", "Missing")
    questions["When was your last period?"] = profile.get(
        "last_period", "Missing")
    questions["When was your last Pap smear?"] = profile.get(
        "last_pap_smear", "Missing")
    questions["When was your last mammogram?"] = profile.get(
        "last_mammogram", "Missing")

    # Age 65+ Specific
    if profile.get("age", 0) >= 65:
        questions["Do you feel little interest or pleasure in doing things?"] = profile.get(
            "interest_in_activities", "Missing")
        questions["Do you feel down, depressed, or hopeless?"] = profile.get(
            "feeling_depressed", "Missing")
        questions["Have you fallen in the last year?"] = f"Yes, {profile.get(
            'falls_in_last_year', 0)} times" if profile.get("falls_in_last_year") else "Missing"
        questions["Were you injured in a fall?"] = "Yes" if profile.get(
            "was_injured_in_fall") else "Missing"

    # Advance Health Care Directive
    questions["Do you have an advance health care directive?"] = "Yes" if profile.get(
        "advance_health_directive") else "Missing"
    if questions["Do you have an advance health care directive?"] == "Missing":
        missing_questions.append(
            "Do you have an advance health care directive?")

    return questions, missing_questions


# Sample health profile with important details
profile = {
    "name": "John Doe",
    "date_of_birth": "1985-07-22",
    "doctor": "Dr. Emily Smith",
    "phone_number": "555-123-4567",
    "sex": "Male",
    "language": "English",
    "occupation": "Engineer",
    "medical_illnesses": {
        "glaucoma": True,
        "heart_disease": False,
        "diabetes": False,
        "migraines": True
    },
    "surgeries": [
        {"type": "Appendectomy", "date": "2005-09-10"}
    ],
    "medications": [
        {"name": "Aspirin", "dosage": "81mg", "frequency": "Once daily"}
    ],
    "hospitalizations": [
        {"type": "Emergency Room", "date": "2021-08-15"},
        {"type": "Hospitalization", "date": "2020-03-12"}
    ],
    "allergies": [
        {"allergen": "Peanuts", "reaction": "Anaphylaxis"}
    ],
    "vaccines": {
        "tetanus": "2020-01-01",
        "flu": "2023-09-15"
    },
    "family_history": {
        "heart_disease": ["Father"],
        "diabetes": ["Mother"]
    },
    "marital_status": "Married",
    "children": 2,
    "smoking_status": "Former smoker",
    "exercise_frequency": "3 times a week",
    "last_colonoscopy": "2023-10-01",
    "advance_health_directive": True
}

# # Generate and print the questions with populated answers
# autopopulated_questions, missing_questions = generate_questions_and_autopopulate(
#     profile)

# # Output the questions with responses
# print("Populated Questions:")
# for question, answer in autopopulated_questions.items():
#     print(f"{question}: {answer}")

# # Output missing questions
# print("\nMissing Questions:")
# for question in missing_questions:
#     print(f"{question}")
