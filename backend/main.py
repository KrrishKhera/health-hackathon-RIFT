from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from datetime import datetime
from model_engine import predict_risk
from llm_engine import generate_explanation
from typing import List
import uuid

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

TARGET_GENES = ["CYP2D6", "CYP2C19", "CYP2C9", "SLCO1B1", "TPMT", "DPYD"]
SUPPORTED_DRUGS = ["CODEINE", "WARFARIN", "CLOPIDOGREL", "SIMVASTATIN", "AZATHIOPRINE", "FLUOROURACIL"]
DRUG_TO_GENE = {
    "CODEINE": "CYP2D6",
    "WARFARIN": "CYP2C9",
    "CLOPIDOGREL": "CYP2C19",
    "SIMVASTATIN": "SLCO1B1",
    "AZATHIOPRINE": "TPMT",
    "FLUOROURACIL": "DPYD"
}


@app.post("/analyze")
async def analyze(
    drug: List[str] = Form(...),
    file: UploadFile = File(...)
):
    MAX_FILE_SIZE = 5 * 1024 * 1024

    if not file.filename.endswith(".vcf"):
        raise HTTPException(status_code=400, detail="Invalid file format. Only .vcf allowed.")

    contents = await file.read()

    if len(contents) > MAX_FILE_SIZE:
        raise HTTPException(status_code=400, detail="File size exceeds the 5MB limit.")

    try:
        text = contents.decode("utf-8")
    except UnicodeDecodeError:
        raise HTTPException(status_code=400, detail="Unable to read VCF file. Must be UTF-8 encoded.")

    if not text.startswith("##fileformat=VCF"):
        raise HTTPException(status_code=400, detail="Invalid VCF header format.")

    if "#CHROM" not in text:
        raise HTTPException(status_code=400, detail="Missing VCF column header line (#CHROM).")

    # Normalise and validate drugs
    drug = [d.strip().upper() for entry in drug for d in entry.split(",")]
    unsupported = [d for d in drug if d not in SUPPORTED_DRUGS]
    if unsupported:
        raise HTTPException(status_code=400, detail=f"Unsupported drug(s): {', '.join(unsupported)}. Supported: {', '.join(SUPPORTED_DRUGS)}")

    # Parse VCF
    detected_variants = []
    for line in text.splitlines():
        if line.startswith("#"):
            continue
        columns = line.strip().split("\t")
        if len(columns) < 10:
            continue

        rsid         = columns[2]
        ref          = columns[3]
        alt          = columns[4]
        info_field   = columns[7]
        format_field = columns[8]
        sample_field = columns[9]

        genotype = None
        format_keys   = format_field.split(":")
        sample_values = sample_field.split(":")
        if "GT" in format_keys:
            genotype = sample_values[format_keys.index("GT")]

        info_dict = {}
        for part in info_field.split(";"):
            if "=" in part:
                k, v = part.split("=", 1)
                info_dict[k] = v

        gene = info_dict.get("GENE")
        star = info_dict.get("STAR")
        rs   = info_dict.get("RS")

        if gene not in TARGET_GENES:
            continue

        diplotype = "Unknown"
        if genotype and star:
            if genotype == "0/0":
                diplotype = "*1/*1"
            elif genotype == "0/1":
                diplotype = f"*1/{star}"
            elif genotype == "1/1":
                diplotype = f"{star}/{star}"

        detected_variants.append({
            "rsid":     rs if rs else rsid,
            "gene":     gene,
            "star":     star,
            "genotype": genotype,
            "diplotype":diplotype,
            "ref":      ref,
            "alt":      alt
        })

    parsing_success = len(detected_variants) > 0
    all_results = []

    for current_drug in drug:
        target_gene   = DRUG_TO_GENE[current_drug]
        gene_variants = [v for v in detected_variants if v.get("gene") == target_gene]
        final_diplotype = gene_variants[0]["diplotype"] if gene_variants else "*1/*1"

        risk_assessment, phenotype, recommendation = predict_risk(current_drug, target_gene, final_diplotype)

        patient_id = f"PATIENT_{uuid.uuid4().hex[:6].upper()}"

        llm_explanation = generate_explanation(
            patient_id=patient_id,
            drug=current_drug,
            gene=target_gene,
            diplotype=final_diplotype,
            phenotype=phenotype,
            activity_score=recommendation.get("activity_score", -1),
            detected_variants=detected_variants,
            risk_label=risk_assessment["risk_label"],
            severity=risk_assessment["severity"],
            recommendation=recommendation.get("action", "")
        )

        all_results.append({
            "patient_id": patient_id,
            "drug": current_drug,
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "risk_assessment": risk_assessment,
            "pharmacogenomic_profile": {
                "primary_gene": target_gene,
                "diplotype": final_diplotype,
                "phenotype": phenotype,
                "detected_variants": detected_variants
            },
            "clinical_recommendation": recommendation,
            "llm_generated_explanation": llm_explanation,
            "quality_metrics": {
                "vcf_parsing_success": parsing_success,
                "variants_detected": len(detected_variants),
                "gene_variants_for_drug": len(gene_variants),
                "diplotype_source": "vcf_parsed" if gene_variants else "wildtype_assumed",
                "annotation_completeness": round(
                    len([v for v in detected_variants if v.get("star")]) / max(len(detected_variants), 1), 2
                ),
                "llm_explanation_status": "rule_based"
            }
        })

    return all_results[0] if len(all_results) == 1 else all_results