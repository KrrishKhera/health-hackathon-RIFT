def predict_risk(drug_name: str, primary_gene: str, diplotype: str):
    """
    Evaluates CPIC guidelines for 6 specific drug-gene pairs to determine
    phenotype, risk level, and clinical recommendations.
    """
    drug = drug_name.upper()
    gene = primary_gene.upper()

    # Default fallback response
    risk_assessment = {"risk_label": "Unknown", "confidence_score": 0.0, "severity": "none"}
    phenotype = "Unknown"
    recommendation = {"action": "Consult clinical guidelines.", "guideline_source": "None"}

    # 1. CLOPIDOGREL & CYP2C19
    if drug == "CLOPIDOGREL" and gene == "CYP2C19":
        if diplotype in ["*1/*1", "*1/*17", "*17/*17"]:
            phenotype = "NM" # Normal / Rapid Metabolizer
            risk_assessment = {"risk_label": "Safe", "confidence_score": 0.95, "severity": "none"}
            recommendation = {"action": "Initiate standard dose of clopidogrel.", "guideline_source": "CPIC 2022"}
        elif diplotype in ["*1/*2", "*1/*3", "*2/*17"]:
            phenotype = "IM" # Intermediate Metabolizer
            risk_assessment = {"risk_label": "Ineffective", "confidence_score": 0.92, "severity": "moderate"}
            recommendation = {"action": "Consider alternative P2Y12 inhibitor (e.g., prasugrel or ticagrelor).", "guideline_source": "CPIC 2022"}
        elif diplotype in ["*2/*2", "*3/*3", "*2/*3"]:
            phenotype = "PM" # Poor Metabolizer
            risk_assessment = {"risk_label": "Ineffective", "confidence_score": 0.98, "severity": "high"}
            recommendation = {"action": "Avoid clopidogrel. Use alternative P2Y12 inhibitor.", "guideline_source": "CPIC 2022"}

    # 2. CODEINE & CYP2D6
    elif drug == "CODEINE" and gene == "CYP2D6":
        if diplotype in ["*1/*1", "*1/*2"]:
            phenotype = "NM" # Normal Metabolizer
            risk_assessment = {"risk_label": "Safe", "confidence_score": 0.95, "severity": "none"}
            recommendation = {"action": "Initiate standard dose of codeine.", "guideline_source": "CPIC 2019"}
        elif "xN" in diplotype or diplotype in ["*2xN/*2xN", "*1/*2xN"]:
            phenotype = "UM" # Ultrarapid Metabolizer
            risk_assessment = {"risk_label": "Toxic", "confidence_score": 0.98, "severity": "critical"}
            recommendation = {"action": "Avoid codeine due to potential for severe toxicity (rapid morphine conversion).", "guideline_source": "CPIC 2019"}
        elif diplotype in ["*3/*4", "*4/*4", "*5/*5", "*4/*5"]:
            phenotype = "PM" # Poor Metabolizer
            risk_assessment = {"risk_label": "Ineffective", "confidence_score": 0.97, "severity": "high"}
            recommendation = {"action": "Avoid codeine due to lack of efficacy. Use alternative analgesic.", "guideline_source": "CPIC 2019"}
        elif diplotype in ["*10/*10", "*4/*10"]:
            phenotype = "IM" # Intermediate Metabolizer
            risk_assessment = {"risk_label": "Ineffective", "confidence_score": 0.90, "severity": "moderate"}
            recommendation = {"action": "Monitor for lack of efficacy. Consider alternative.", "guideline_source": "CPIC 2019"}

    # 3. WARFARIN & CYP2C9
    elif drug == "WARFARIN" and gene == "CYP2C9":
        if diplotype == "*1/*1":
            phenotype = "NM" # Normal Metabolizer
            risk_assessment = {"risk_label": "Safe", "confidence_score": 0.95, "severity": "none"}
            recommendation = {"action": "Initiate standard warfarin dosing.", "guideline_source": "CPIC 2017"}
        elif diplotype in ["*1/*2", "*1/*3"]:
            phenotype = "IM" # Intermediate Metabolizer
            risk_assessment = {"risk_label": "Adjust Dosage", "confidence_score": 0.93, "severity": "moderate"}
            recommendation = {"action": "Consider lower initial dose. Patient has moderate bleeding risk.", "guideline_source": "CPIC 2017"}
        elif diplotype in ["*2/*2", "*2/*3", "*3/*3"]:
            phenotype = "PM" # Poor Metabolizer
            risk_assessment = {"risk_label": "Adjust Dosage", "confidence_score": 0.96, "severity": "high"}
            recommendation = {"action": "Significantly reduce initial dose. Patient has high bleeding risk.", "guideline_source": "CPIC 2017"}

    # 4. SIMVASTATIN & SLCO1B1
    elif drug == "SIMVASTATIN" and gene == "SLCO1B1":
        if diplotype == "*1/*1":
            phenotype = "Normal Function"
            risk_assessment = {"risk_label": "Safe", "confidence_score": 0.95, "severity": "none"}
            recommendation = {"action": "Standard simvastatin dosing.", "guideline_source": "CPIC 2022"}
        elif diplotype in ["*1/*5", "*1/*15"]:
            phenotype = "Decreased Function"
            risk_assessment = {"risk_label": "Adjust Dosage", "confidence_score": 0.94, "severity": "moderate"}
            recommendation = {"action": "Prescribe lower dose or consider alternative statin (e.g., rosuvastatin).", "guideline_source": "CPIC 2022"}
        elif diplotype in ["*5/*5", "*15/*15"]:
            phenotype = "Poor Function"
            risk_assessment = {"risk_label": "Toxic", "confidence_score": 0.97, "severity": "high"}
            recommendation = {"action": "Avoid simvastatin due to high risk of myopathy. Prescribe alternative statin.", "guideline_source": "CPIC 2022"}

    # 5. AZATHIOPRINE & TPMT
    elif drug == "AZATHIOPRINE" and gene == "TPMT":
        if diplotype == "*1/*1":
            phenotype = "NM" # Normal Metabolizer
            risk_assessment = {"risk_label": "Safe", "confidence_score": 0.95, "severity": "none"}
            recommendation = {"action": "Initiate standard dose.", "guideline_source": "CPIC 2018"}
        elif diplotype in ["*1/*2", "*1/*3A", "*1/*3C"]:
            phenotype = "IM" # Intermediate Metabolizer
            risk_assessment = {"risk_label": "Adjust Dosage", "confidence_score": 0.96, "severity": "moderate"}
            recommendation = {"action": "Start at 30-80% of standard dose due to myelosuppression risk.", "guideline_source": "CPIC 2018"}
        elif diplotype in ["*2/*2", "*3A/*3A", "*3C/*3C", "*2/*3A"]:
            phenotype = "PM" # Poor Metabolizer
            risk_assessment = {"risk_label": "Toxic", "confidence_score": 0.99, "severity": "critical"}
            recommendation = {"action": "Avoid azathioprine or reduce dose by 90% due to fatal myelosuppression risk.", "guideline_source": "CPIC 2018"}

    # 6. FLUOROURACIL & DPYD
    elif drug == "FLUOROURACIL" and gene == "DPYD":
        if diplotype == "*1/*1":
            phenotype = "NM" # Normal Metabolizer
            risk_assessment = {"risk_label": "Safe", "confidence_score": 0.95, "severity": "none"}
            recommendation = {"action": "Standard dosing.", "guideline_source": "CPIC 2017"}
        elif diplotype in ["*1/*2A", "*1/*13"]:
            phenotype = "IM" # Intermediate Metabolizer
            risk_assessment = {"risk_label": "Adjust Dosage", "confidence_score": 0.95, "severity": "high"}
            recommendation = {"action": "Reduce starting dose by 50% due to severe toxicity risk.", "guideline_source": "CPIC 2017"}
        elif diplotype in ["*2A/*2A", "*13/*13", "*2A/*13"]:
            phenotype = "PM" # Poor Metabolizer
            risk_assessment = {"risk_label": "Toxic", "confidence_score": 0.98, "severity": "critical"}
            recommendation = {"action": "Avoid fluorouracil entirely due to high risk of fatal systemic toxicity.", "guideline_source": "CPIC 2017"}

    return risk_assessment, phenotype, recommendation