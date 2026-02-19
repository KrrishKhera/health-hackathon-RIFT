from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from datetime import datetime
from model_engine import predict_risk
import uuid

app=FastAPI()
#ye frontend ke liya hai:
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
SUPPORTED_DRUGS = [
    "CODEINE", "WARFARIN", "CLOPIDOGREL",
    "SIMVASTATIN", "AZATHIOPRINE", "FLUOROURACIL"
]#these 6 drugs aman and vaibhav
TARGET_GENES = [
    "CYP2D6", "CYP2C19", "CYP2C9",
    "SLCO1B1", "TPMT", "DPYD"
]
@app.post("/analyze")
async def analyze(
    drug: str = Form(...),
    file: UploadFile = File(...)
):
    if not file.filename.endswith(".vcf"):
        raise HTTPException(
            status_code=400,
            detail="invalid file format. Only .vcf allowed."
        )
    drug=drug.upper().strip()
    if drug not in SUPPORTED_DRUGS:
        raise HTTPException(
            status_code=400,
            detail="Unsupported drug."
        )
    try:
        contents = await file.read()
        text = contents.decode("utf-8")
    except:
        raise HTTPException(
            status_code=400,
            detail="Unable to read VCF file."
        )
    if not text.startswith("##fileformat=VCF"):
        raise HTTPException(
            status_code=400,
            detail="Invalid VCF header format."
        )
    if "#CHROM" not in text:
        raise HTTPException(
            status_code=400,
            detail="VCF column header line."
        )
    detected_variants = []
    primary_gene = "Unknown"

    lines = text.splitlines()

    for line in lines:
        if line.startswith("#"):
            continue

        columns = line.strip().split("\t")

        if len(columns) < 10:
            continue

        rsid = columns[2]
        ref = columns[3]
        alt = columns[4]
        info_field = columns[7]
        format_field = columns[8]
        sample_field = columns[9]
        genotype = None
        format_keys = format_field.split(":")
        sample_values = sample_field.split(":")

        if "GT" in format_keys:
            gt_index = format_keys.index("GT")
            genotype = sample_values[gt_index]

        info_dict = {}
        info_parts = info_field.split(";")

        for part in info_parts:
            if "=" in part:
                key, value = part.split("=",1)
                info_dict[key] = value

        gene = info_dict.get("GENE")
        star = info_dict.get("STAR")
        rs=info_dict.get("RS")
       
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
            "rsid": rsid,
            "gene": gene,
            "star": star,
            "genotype": genotype,
            "diplotype": diplotype
        })

        if primary_gene == "Unknown" and gene:
            primary_gene = gene
    if not detected_variants:
        parsing_success = False
    else:
        parsing_success = True
    return {
    "patient_id": f"PATIENT_{uuid.uuid4().hex[:6]}",
    "drug": drug,
    "timestamp": datetime.utcnow().isoformat(),
    "risk_assessment": {
        "risk_label": "Unknown",
        "confidence_score": 0.0,
        "severity": "none"
    },
    "pharmacogenomic_profile": {
        "primary_gene": primary_gene,
        "diplotype": detected_variants[0]["diplotype"] if detected_variants else "Unknown",
        "phenotype": "Unknown",
        "detected_variants": detected_variants
    },
    "clinical_recommendation": {},
    "llm_generated_explanation": {
        "summary": "VCF parsed successfully. Risk prediction not yet applied."
    },
    "quality_metrics": {
        "vcf_parsing_success": parsing_success
    }
}

    