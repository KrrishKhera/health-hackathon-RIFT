import google.generativeai as genai
import json
import os

from dotenv import load_dotenv
load_dotenv()

genai.configure(api_key=os.environ["GEMINI_API_KEY"])
model = genai.GenerativeModel("gemini-2.5-flash")

def generate_explanation(
    patient_id: str,
    drug: str,
    gene: str,
    diplotype: str,
    phenotype: str,
    activity_score,
    detected_variants: list,
    risk_label: str,
    severity: str,
    recommendation: str
) -> dict:

    relevant_variants = [v for v in detected_variants if v.get("gene") == gene]

    if relevant_variants:
        variants_text = "\n".join([
            f"  - rsID: {v.get('rsid', 'N/A')} | Star allele: {v.get('star', 'N/A')} | Genotype: {v.get('genotype', 'N/A')}"
            for v in relevant_variants
        ])
    else:
        variants_text = "  - No non-wildtype variants detected (wildtype *1/*1 assumed)"

    activity_str = str(round(activity_score, 2)) if isinstance(activity_score, float) and activity_score >= 0 else "unknown"

    prompt = f"""You are a clinical pharmacogenomics specialist writing a report for a treating physician.
Return ONLY a valid JSON object — no markdown, no code fences, no explanation outside the JSON.

PATIENT DATA:
- Patient ID: {patient_id}
- Drug: {drug}
- Primary Gene: {gene}
- Diplotype: {diplotype}
- Phenotype: {phenotype}
- Activity Score: {activity_str} (scale: 0.0 = no function, 1.0 = one normal allele, 2.0 = fully normal)
- Risk Label: {risk_label}
- Severity: {severity}
- Clinical Recommendation: {recommendation}

DETECTED VARIANTS FOR {gene}:
{variants_text}

Generate this exact JSON structure:
{{
  "summary": "2-3 sentences. Name the diplotype, phenotype, activity score, and risk. Written for a clinician, not a patient.",
  "mechanism": "How {gene} variants at this diplotype biologically affect {drug} metabolism or transport. Be specific — mention enzyme activity, pathway, metabolite.",
  "variant_impact": "What each detected star allele does to {gene} function at the molecular level. If wildtype assumed, state that clearly.",
  "clinical_context": "Why the {phenotype} phenotype creates the '{risk_label}' risk for {drug} specifically. Include what could go wrong clinically.",
  "alternative_options": "If severity is moderate/high/critical: name 1-2 specific evidence-based drug alternatives with brief rationale. If severity is none, write 'No alternatives required.'",
  "monitoring_parameters": "Specific labs, symptoms, or follow-up timeframes a clinician should order given this risk profile."
}}"""

    try:
        response = model.generate_content(prompt)
        text = response.text.strip()

        if "```" in text:
            text = text.split("```")[1]
            if text.startswith("json"):
                text = text[4:]
            text = text.strip()

        return json.loads(text)

    except json.JSONDecodeError:
        return _fallback_explanation(drug, gene, diplotype, phenotype, risk_label, recommendation, error="json_parse_failed")

    except Exception as e:
        return _fallback_explanation(drug, gene, diplotype, phenotype, risk_label, recommendation, error=str(e))


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