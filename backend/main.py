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
TARGET_GENES = ["CYP2D6", "CYP2C19", "CYP2C9", "SLCO1B1", "TPMT", "DPYD"]
SUPPORTED_DRUGS = [
    "CODEINE", "WARFARIN", "CLOPIDOGREL",
    "SIMVASTATIN", "AZATHIOPRINE", "FLUOROURACIL"
]#these 6 drugs aman and vaibhav
@app.post("/analyze")
async def analyze(
    drug: str = Form(...),
    file: UploadFile = File(...)
):
    MAX_FILE_SIZE = 5 * 1024 * 1024

    if not file.filename.endswith(".vcf"):
        raise HTTPException(
            status_code=400,
            detail="invalid file format. Only .vcf allowed."
        )

    if file.size and file.size > MAX_FILE_SIZE:
        raise HTTPException(
            status_code=400,
            detail="File size exceeds the 5MB limit. Please upload a smaller VCF file."
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
    # Ensure a diplotype exists before passing it, otherwise use 'Unknown'
    parsing_success = len(detected_variants)>0
    final_diplotype = detected_variants[0]["diplotype"] if detected_variants else "Unknown"

    # 1. Call the engine
    risk_assessment, phenotype, recommendation = predict_risk(drug, primary_gene, final_diplotype)

    # 2. Return the structured response
    return {
        "patient_id": f"PATIENT_{uuid.uuid4().hex[:6]}",
        "drug": drug,
        "timestamp": datetime.utcnow().isoformat(),
        "risk_assessment": risk_assessment,
        "pharmacogenomic_profile": {
            "primary_gene": primary_gene,
            "diplotype": final_diplotype,
            "phenotype": phenotype,
            "detected_variants": detected_variants
        },
        "clinical_recommendation": recommendation,
        "llm_generated_explanation": {
            "summary": "AI logic pending." # We will inject the Gemini output here next!
        },
        "quality_metrics": {
            "vcf_parsing_success": parsing_success
        }
    }


