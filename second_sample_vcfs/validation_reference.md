# PharmaGuard Validation Test Reference

One variant per gene. Exactly matches what the current parser handles.

---

## Test Matrix

| File | Drug to Test | Gene | Genotype | Diplotype | Expected Phenotype | Expected Risk | Severity |
|---|---|---|---|---|---|---|---|
| validate_01_codeine_PM.vcf | CODEINE | CYP2D6 | 1/1 | *4/*4 | PM | Ineffective | high |
| validate_02_codeine_URM.vcf | CODEINE | CYP2D6 | 1/1 | *2xN/*2xN | URM | Toxic | critical |
| validate_03_warfarin_IM.vcf | WARFARIN | CYP2C9 | 0/1 | *1/*3 | IM | Adjust Dosage | moderate |
| validate_04_clopidogrel_PM.vcf | CLOPIDOGREL | CYP2C19 | 1/1 | *2/*2 | PM | Ineffective | high |
| validate_05_simvastatin_toxic.vcf | SIMVASTATIN | SLCO1B1 | 1/1 | *5/*5 | Poor Function | Toxic | high |
| validate_06_azathioprine_toxic.vcf | AZATHIOPRINE | TPMT | 1/1 | *3C/*3C | PM | Toxic | critical |
| validate_07_fluorouracil_toxic.vcf | FLUOROURACIL | DPYD | 1/1 | *2A/*2A | PM | Toxic | critical |
| validate_08_all_wildtype_NM.vcf | Any drug | All | 0/0 | *1/*1 | NM / Normal | Safe | none |
| validate_09_all_drugs_mixed.vcf | All 6 drugs | All | Mixed | Mixed | Mixed | Mixed | Mixed |

---

## Expected JSON Snippets Per Test

### Test 01 — CODEINE + PM
```json
{
  "drug": "CODEINE",
  "risk_assessment": {
    "risk_label": "Ineffective",
    "confidence_score": 0.97,
    "severity": "high"
  },
  "pharmacogenomic_profile": {
    "primary_gene": "CYP2D6",
    "diplotype": "*4/*4",
    "phenotype": "PM"
  },
  "quality_metrics": {
    "vcf_parsing_success": true,
    "variants_detected": 1,
    "gene_variants_for_drug": 1,
    "diplotype_source": "vcf_parsed"
  }
}
```

### Test 02 — CODEINE + URM (most critical test)
```json
{
  "drug": "CODEINE",
  "risk_assessment": {
    "risk_label": "Toxic",
    "confidence_score": 0.98,
    "severity": "critical"
  },
  "pharmacogenomic_profile": {
    "primary_gene": "CYP2D6",
    "diplotype": "*2xN/*2xN",
    "phenotype": "URM"
  }
}
```

### Test 03 — WARFARIN + IM
```json
{
  "drug": "WARFARIN",
  "risk_assessment": {
    "risk_label": "Adjust Dosage",
    "confidence_score": 0.93,
    "severity": "moderate"
  },
  "pharmacogenomic_profile": {
    "primary_gene": "CYP2C9",
    "diplotype": "*1/*3",
    "phenotype": "IM"
  }
}
```

### Test 08 — Wildtype NM (diplotype_source should be "vcf_parsed", NOT "wildtype_assumed")
```json
{
  "risk_assessment": {
    "risk_label": "Safe",
    "severity": "none"
  },
  "pharmacogenomic_profile": {
    "diplotype": "*1/*1",
    "phenotype": "NM"
  },
  "quality_metrics": {
    "diplotype_source": "vcf_parsed",
    "variants_detected": 6
  }
}
```

### Test 09 — Multi-drug mixed (send all 6 drugs, expect array response)
```json
[
  { "drug": "CODEINE",      "risk_assessment": { "risk_label": "Ineffective", "severity": "high" },     "pharmacogenomic_profile": { "diplotype": "*4/*4",   "phenotype": "PM" } },
  { "drug": "CLOPIDOGREL",  "risk_assessment": { "risk_label": "Ineffective", "severity": "moderate" }, "pharmacogenomic_profile": { "diplotype": "*1/*2",   "phenotype": "IM" } },
  { "drug": "WARFARIN",     "risk_assessment": { "risk_label": "Adjust Dosage","severity": "moderate" },"pharmacogenomic_profile": { "diplotype": "*1/*3",   "phenotype": "IM" } },
  { "drug": "SIMVASTATIN",  "risk_assessment": { "risk_label": "Adjust Dosage","severity": "moderate" },"pharmacogenomic_profile": { "diplotype": "*1/*5",   "phenotype": "Decreased Function" } },
  { "drug": "AZATHIOPRINE", "risk_assessment": { "risk_label": "Toxic",        "severity": "critical" },"pharmacogenomic_profile": { "diplotype": "*3C/*3C", "phenotype": "PM" } },
  { "drug": "FLUOROURACIL", "risk_assessment": { "risk_label": "Adjust Dosage","severity": "high" },    "pharmacogenomic_profile": { "diplotype": "*1/*2A",  "phenotype": "IM" } }
]
```

---

## curl Commands to Run All Tests

```bash
BASE=http://localhost:8000

# Test 01 - CODEINE PM (Ineffective)
curl -s -X POST $BASE/analyze \
  -F "drug=CODEINE" \
  -F "file=@validate_01_codeine_PM.vcf" | python3 -m json.tool

# Test 02 - CODEINE URM (Toxic/critical — most dangerous)
curl -s -X POST $BASE/analyze \
  -F "drug=CODEINE" \
  -F "file=@validate_02_codeine_URM.vcf" | python3 -m json.tool

# Test 03 - WARFARIN IM (Adjust Dosage)
curl -s -X POST $BASE/analyze \
  -F "drug=WARFARIN" \
  -F "file=@validate_03_warfarin_IM.vcf" | python3 -m json.tool

# Test 04 - CLOPIDOGREL PM (Ineffective)
curl -s -X POST $BASE/analyze \
  -F "drug=CLOPIDOGREL" \
  -F "file=@validate_04_clopidogrel_PM.vcf" | python3 -m json.tool

# Test 05 - SIMVASTATIN Toxic (Poor SLCO1B1 function)
curl -s -X POST $BASE/analyze \
  -F "drug=SIMVASTATIN" \
  -F "file=@validate_05_simvastatin_toxic.vcf" | python3 -m json.tool

# Test 06 - AZATHIOPRINE Toxic/critical (TPMT PM)
curl -s -X POST $BASE/analyze \
  -F "drug=AZATHIOPRINE" \
  -F "file=@validate_06_azathioprine_toxic.vcf" | python3 -m json.tool

# Test 07 - FLUOROURACIL Toxic/critical (DPYD PM)
curl -s -X POST $BASE/analyze \
  -F "drug=FLUOROURACIL" \
  -F "file=@validate_07_fluorouracil_toxic.vcf" | python3 -m json.tool

# Test 08 - All wildtype (Safe/NM for all drugs)
curl -s -X POST $BASE/analyze \
  -F "drug=CODEINE" \
  -F "file=@validate_08_all_wildtype_NM.vcf" | python3 -m json.tool

# Test 09 - All 6 drugs, multi-drug request
curl -s -X POST $BASE/analyze \
  -F "drug=CODEINE,WARFARIN,CLOPIDOGREL,SIMVASTATIN,AZATHIOPRINE,FLUOROURACIL" \
  -F "file=@validate_09_all_drugs_mixed.vcf" | python3 -m json.tool
```

---

## What Each Test Validates

| Test | Validates |
|---|---|
| 01 | `1/1` genotype → `*STAR/*STAR` diplotype, PM phenotype lookup, Ineffective risk label |
| 02 | `*2xN` duplication allele, URM phenotype, critical severity, Toxic label |
| 03 | `0/1` genotype → `*1/*STAR` diplotype, IM phenotype, Adjust Dosage label |
| 04 | PM + Ineffective for CYP2C19 gene (different gene from Test 01) |
| 05 | SLCO1B1 phenotype labels (Poor/Decreased/Normal Function, not PM/IM/NM) |
| 06 | TPMT PM critical path — CONTRAINDICATED language in recommendation |
| 07 | DPYD PM critical path — `diplotype_source: vcf_parsed` confirmed |
| 08 | `0/0` wildtype rows — `diplotype_source: vcf_parsed`, phenotype NM, risk Safe |
| 09 | Multi-drug array response, comma-separated drug input, all 6 genes in one file |
