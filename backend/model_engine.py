ACTIVITY_SCORES = {
    "CYP2D6": {
        "*1": 1.0, "*2": 1.0, "*2xN": 2.0, "*1xN": 2.0,  # xN = gene duplication
        "*3": 0.0, "*4": 0.0, "*5": 0.0, "*6": 0.0,       # no function
        "*10": 0.25, "*17": 0.5, "*29": 0.5, "*41": 0.5,  # decreased
        "*9": 0.5,
    },
    "CYP2C19": {
        "*1": 1.0,
        "*17": 1.5,                          # increased function
        "*2": 0.0, "*3": 0.0,               # no function
        "*4": 0.0, "*5": 0.0, "*6": 0.0,
    },
    "CYP2C9": {
        "*1": 1.0,
        "*2": 0.5, "*3": 0.0,
        "*4": 0.0, "*5": 0.0, "*6": 0.0,
        "*8": 0.5, "*11": 0.5,
    },
    "SLCO1B1": {
        "*1": 1.0, "*14": 1.0,
        "*5": 0.0, "*15": 0.0, "*17": 0.0,
        "*1a": 1.0, "*1b": 1.0,
    },
    "TPMT": {
        "*1": 1.0,
        "*2": 0.0, "*3A": 0.0, "*3B": 0.0,
        "*3C": 0.0, "*4": 0.0,
    },
    "DPYD": {
        "*1": 1.0,
        "*2A": 0.0, "*13": 0.0,
        "HapB3": 0.5,
        "*4": 0.5, "*5": 0.5, "*6": 0.5,
    }
}

PHENOTYPE_RULES = {
    "CYP2D6": [
        (0.0, 0.0,   "PM"),    # Poor
        (0.0, 0.5,   "IM"),    # Intermediate (exclusive lower, inclusive upper)
        (0.5, 1.25,  "IM"),
        (1.25, 2.25, "NM"),    # Normal
        (2.25, 99,   "URM"),   # Ultrarapid
    ],
    "CYP2C19": [
        (0.0, 0.0,   "PM"),
        (0.0, 1.25,  "IM"),
        (1.25, 1.75, "NM"),
        (1.75, 2.5,  "RM"),    # Rapid (one *17)
        (2.5, 99,    "URM"),   # Ultrarapid (two *17)
    ],
    "CYP2C9": [
        (0.0, 0.0,   "PM"),
        (0.0, 1.0,   "IM"),
        (1.0, 99,    "NM"),
    ],
    "SLCO1B1": [
        (0.0, 0.0,   "Poor Function"),
        (0.0, 1.5,   "Decreased Function"),
        (1.5, 99,    "Normal Function"),
    ],
    "TPMT": [
        (0.0, 0.0,   "PM"),
        (0.0, 1.5,   "IM"),
        (1.5, 99,    "NM"),
    ],
    "DPYD": [
        (0.0, 0.0,   "PM"),
        (0.0, 1.5,   "IM"),
        (1.5, 99,    "NM"),
    ],
}

CPIC_RULES = {
    "CODEINE": {
        "gene": "CYP2D6",
        "PM":  ("Ineffective", 0.97, "high",     "Avoid codeine. Lacks efficacy — cannot convert to morphine. Use non-opioid alternative.", "CPIC 2019"),
        "IM":  ("Ineffective", 0.85, "moderate", "Monitor for reduced analgesia. Consider lower dose or alternative analgesic.", "CPIC 2019"),
        "NM":  ("Safe",        0.95, "none",     "Standard codeine dosing per label.", "CPIC 2019"),
        "URM": ("Toxic",       0.98, "critical", "CONTRAINDICATED. Ultrarapid morphine conversion risks fatal respiratory depression.", "CPIC 2019"),
        "RM":  ("Toxic",       0.90, "high",     "Avoid codeine. Increased morphine exposure risk.", "CPIC 2019"),
    },
    "WARFARIN": {
        "gene": "CYP2C9",
        "PM":  ("Adjust Dosage", 0.96, "high",     "Reduce initial dose by 50-75%. High bleeding risk — intensive INR monitoring.", "CPIC 2017"),
        "IM":  ("Adjust Dosage", 0.93, "moderate", "Reduce initial dose by 25-50%. Moderate bleeding risk.", "CPIC 2017"),
        "NM":  ("Safe",          0.95, "none",     "Standard warfarin dosing. Routine INR monitoring.", "CPIC 2017"),
    },
    "CLOPIDOGREL": {
        "gene": "CYP2C19",
        "PM":  ("Ineffective", 0.98, "high",     "Avoid clopidogrel. Use prasugrel or ticagrelor.", "CPIC 2022"),
        "IM":  ("Ineffective", 0.87, "moderate", "Consider alternative P2Y12 inhibitor. Discuss benefit/risk.", "CPIC 2022"),
        "NM":  ("Safe",        0.95, "none",     "Standard 75mg/day clopidogrel.", "CPIC 2022"),
        "RM":  ("Safe",        0.90, "none",     "Standard dosing. Slightly enhanced activation.", "CPIC 2022"),
        "URM": ("Safe",        0.88, "none",     "Standard dosing. Monitor for enhanced platelet inhibition.", "CPIC 2022"),
    },
    "SIMVASTATIN": {
        "gene": "SLCO1B1",
        "Poor Function":      ("Toxic",         0.97, "high",     "Avoid simvastatin. High myopathy risk. Switch to pravastatin or rosuvastatin.", "CPIC 2022"),
        "Decreased Function": ("Adjust Dosage", 0.94, "moderate", "Max 20mg/day simvastatin. Monitor for muscle pain/weakness. Consider alternative.", "CPIC 2022"),
        "Normal Function":    ("Safe",          0.95, "none",     "Standard simvastatin dose up to 40mg/day.", "CPIC 2022"),
    },
    "AZATHIOPRINE": {
        "gene": "TPMT",
        "PM":  ("Toxic",        0.99, "critical", "CONTRAINDICATED at standard doses. 90% dose reduction or switch to mycophenolate. Fatal myelosuppression risk.", "CPIC 2018"),
        "IM":  ("Adjust Dosage", 0.96, "moderate", "Start at 30-70% of standard dose. Weekly CBC for first 8 weeks.", "CPIC 2018"),
        "NM":  ("Safe",          0.95, "none",     "Standard dosing. Routine CBC monitoring.", "CPIC 2018"),
    },
    "FLUOROURACIL": {
        "gene": "DPYD",
        "PM":  ("Toxic",         0.98, "critical", "CONTRAINDICATED. Life-threatening toxicity risk. Use alternative chemotherapy regimen.", "CPIC 2017"),
        "IM":  ("Adjust Dosage", 0.95, "high",     "Reduce starting dose by 50%. Monitor closely for mucositis, diarrhea, neutropenia.", "CPIC 2017"),
        "NM":  ("Safe",          0.95, "none",     "Standard dosing per oncology protocol.", "CPIC 2017"),
    },
}


def get_activity_score(gene: str, allele: str) -> float | None:
    """Returns activity score for a star allele, None if unknown."""
    scores = ACTIVITY_SCORES.get(gene, {})
    if allele in scores:
        return scores[allele]
    normalized = allele if allele.startswith("*") else f"*{allele}"
    return scores.get(normalized, None)


def diplotype_to_phenotype(gene: str, diplotype: str):

    if not diplotype or diplotype == "Unknown" or "/" not in diplotype:
        return "Unknown", -1

    a1, a2 = diplotype.split("/", 1)
    a1, a2 = a1.strip(), a2.strip()

    score1 = get_activity_score(gene, a1)
    score2 = get_activity_score(gene, a2)

    if score1 is None and score2 is None:
        return "Unknown", -1

    if score1 is None:
        score1 = 1.0
    if score2 is None:
        score2 = 1.0

    total = score1 + score2

    rules = PHENOTYPE_RULES.get(gene)
    if not rules:
        return "Unknown", total

    for low, high, label in rules:
        if low == high == 0.0:
            if total == 0.0:
                return label, total
        elif low < total <= high or (low == 0.0 and total == 0.0):
            return label, total

    return rules[-1][2], total


def predict_risk(drug_name: str, primary_gene: str, diplotype: str):
    drug = drug_name.upper().strip()
    gene = primary_gene.upper().strip()

    phenotype, activity_score = diplotype_to_phenotype(gene, diplotype)

    rule_set = CPIC_RULES.get(drug)

    if not rule_set or rule_set["gene"] != gene:
        return (
            {"risk_label": "Unknown", "confidence_score": 0.0, "severity": "none"},
            phenotype,
            {"action": "No CPIC guideline match. Consult clinical pharmacist.",
             "guideline_source": "None",
             "activity_score": activity_score}
        )

    outcome = rule_set.get(phenotype)

    if not outcome:
        outcome = rule_set.get("NM", ("Unknown", 0.5, "none", "No specific recommendation.", "CPIC"))

    risk_label, confidence, severity, action, source = outcome

    risk_assessment = {
        "risk_label": risk_label,
        "confidence_score": confidence,
        "severity": severity
    }
    recommendation = {
        "action": action,
        "guideline_source": source,
        "activity_score": round(activity_score, 2) if activity_score >= 0 else "unknown"
    }

    return risk_assessment, phenotype, recommendation