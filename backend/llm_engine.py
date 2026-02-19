import json
import os

def generate_explanation(
    patient_id, drug, gene, diplotype, phenotype,
    activity_score, detected_variants, risk_label, severity, recommendation
):
    relevant = [v for v in detected_variants if v.get("gene") == gene]
    variant_str = ", ".join([f"{v.get('rsid','?')} ({v.get('star','?')})" for v in relevant]) if relevant else "no non-wildtype variants (wildtype *1/*1 assumed)"
    activity_str = round(activity_score, 2) if isinstance(activity_score, float) and activity_score >= 0 else "unknown"

    phenotype_full = {
        "PM": "Poor Metabolizer", "IM": "Intermediate Metabolizer",
        "NM": "Normal Metabolizer", "RM": "Rapid Metabolizer",
        "URM": "Ultrarapid Metabolizer"
    }.get(phenotype, phenotype)

    mechanisms = {
        "CYP2D6": f"CYP2D6 encodes a hepatic cytochrome P450 enzyme responsible for metabolizing ~25% of clinically used drugs. The {diplotype} diplotype yields an activity score of {activity_str}, resulting in {phenotype_full} status and {'reduced' if activity_score < 2 else 'normal'} enzymatic conversion of {drug}.",
        "CYP2C19": f"CYP2C19 encodes a key hepatic oxidase involved in the bioactivation of prodrugs like clopidogrel. The {diplotype} diplotype yields an activity score of {activity_str}. As a {phenotype_full}, the patient shows {'impaired' if activity_score < 2 else 'normal'} conversion of {drug} to its active metabolite.",
        "CYP2C9": f"CYP2C9 is the primary enzyme responsible for metabolizing warfarin's S-enantiomer. The {diplotype} diplotype results in an activity score of {activity_str}, indicating {phenotype_full} status and {'reduced clearance with increased bleeding risk' if activity_score < 2 else 'normal warfarin clearance'}.",
        "SLCO1B1": f"SLCO1B1 encodes the OATP1B1 hepatic uptake transporter responsible for statin clearance. The {diplotype} diplotype impairs simvastatin transport into hepatocytes, increasing plasma drug exposure and myopathy risk.",
        "TPMT": f"TPMT encodes thiopurine methyltransferase, which inactivates thiopurine drugs like azathioprine. The {diplotype} diplotype yields activity score {activity_str}. Reduced TPMT activity leads to accumulation of cytotoxic thioguanine nucleotides.",
        "DPYD": f"DPYD encodes dihydropyrimidine dehydrogenase, responsible for ~80% of fluorouracil catabolism. The {diplotype} diplotype significantly reduces enzymatic breakdown, causing toxic drug accumulation.",
    }

    clinical_contexts = {
        "Toxic": f"With {phenotype_full} status, {drug} cannot be safely metabolized at standard doses. Toxic drug or metabolite accumulation is expected, posing serious risk of {'respiratory depression' if drug == 'CODEINE' else 'severe systemic toxicity'}.",
        "Ineffective": f"With {phenotype_full} status, {drug} {'cannot be activated' if drug in ['CODEINE','CLOPIDOGREL'] else 'is not processed efficiently'}. Standard doses are unlikely to produce therapeutic benefit.",
        "Adjust Dosage": f"With {phenotype_full} status, standard doses of {drug} carry elevated risk. Dose adjustment is required to maintain therapeutic efficacy while minimizing toxicity.",
        "Safe": f"The {phenotype_full} phenotype is consistent with normal {drug} metabolism. Standard dosing is expected to achieve therapeutic levels without increased risk.",
    }

    alternatives = {
        "CODEINE":       "Consider morphine or hydromorphone (direct-acting opioids not requiring CYP2D6 activation), or non-opioid analgesics such as acetaminophen or NSAIDs.",
        "WARFARIN":      "If dose adjustment is insufficient, consider direct oral anticoagulants (DOACs) such as apixaban or rivaroxaban, which do not require CYP2C9 metabolism.",
        "CLOPIDOGREL":   "Prasugrel or ticagrelor are recommended alternatives — both are effective regardless of CYP2C19 status per CPIC 2022 guidelines.",
        "SIMVASTATIN":   "Pravastatin or rosuvastatin are preferred alternatives — both show minimal SLCO1B1-dependent transport and carry lower myopathy risk.",
        "AZATHIOPRINE":  "Mycophenolate mofetil is the primary alternative for immunosuppression in TPMT-deficient patients. If thiopurine therapy is essential, reduce dose by 90% with CBC monitoring.",
        "FLUOROURACIL":  "Alternative chemotherapy regimens not dependent on DPYD should be considered. Consult oncology for regimen adjustment based on cancer type and treatment protocol.",
    }

    monitoring = {
        "Toxic":         f"Do not initiate {drug}. If already administered, monitor for toxicity signs immediately. {'Check respiratory rate and oxygen saturation.' if drug == 'CODEINE' else 'Monitor CBC, liver function, and organ-specific toxicity markers per clinical protocol.'}",
        "Ineffective":   f"If {drug} is trialled, assess therapeutic response within 24–48 hours. Lack of efficacy at standard doses confirms genotype prediction. Switch to recommended alternative.",
        "Adjust Dosage": f"{'Monitor INR every 3–5 days for first 2 weeks.' if drug == 'WARFARIN' else 'Monitor clinical response and relevant labs at 1–2 week intervals.'} Titrate dose to therapeutic target.",
        "Safe":          "Standard monitoring per drug label. No additional pharmacogenomic-specific surveillance required.",
    }

    return {
        "summary": f"Patient {patient_id} carries the {diplotype} diplotype for {gene}, consistent with {phenotype_full} (activity score: {activity_str}). Risk assessment for {drug}: {risk_label} — {severity} severity. {recommendation}",
        "mechanism": mechanisms.get(gene, f"The {diplotype} diplotype alters {gene} function, affecting {drug} metabolism."),
        "variant_impact": f"Detected variants: {variant_str}. These alleles reduce {gene} functional activity to a combined score of {activity_str} (scale: 0.0 = no function, 2.0 = fully normal).",
        "clinical_context": clinical_contexts.get(risk_label, f"The {phenotype_full} phenotype affects {drug} response."),
        "alternative_options": alternatives.get(drug, "Consult clinical pharmacist for evidence-based alternatives.") if severity in ["moderate", "high", "critical"] else "No alternatives required.",
        "monitoring_parameters": monitoring.get(risk_label, "Follow institutional pharmacogenomics monitoring protocol."),
        "_llm_status": "rule_based"
    }


def _fallback_explanation(drug, gene, diplotype, phenotype, risk_label, recommendation, error="unknown"):

    return {
        "summary": f"Patient carries the {diplotype} diplotype for {gene}, consistent with {phenotype} status. Risk assessment for {drug}: {risk_label}.",
        "mechanism": f"The {diplotype} diplotype alters {gene} enzymatic activity, directly affecting {drug} metabolism.",
        "variant_impact": "Detailed variant annotation available in pharmacogenomic_profile.detected_variants.",
        "clinical_context": f"As a {phenotype}, this patient's response to {drug} is predicted to be: {risk_label}.",
        "alternative_options": "Consult clinical pharmacist for evidence-based alternatives.",
        "monitoring_parameters": "Follow institutional pharmacogenomics monitoring protocol.",
        "_llm_status": "fallback",
        "_llm_error": error
    }