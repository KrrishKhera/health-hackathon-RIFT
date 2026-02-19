# VariantRx
### Pharmacogenomic Risk Prediction System

> AI-powered clinical decision support that analyzes patient genetic data (VCF files) to predict personalized drug risks and generate explainable recommendations — aligned with CPIC guidelines.

**RIFT 2026 Hackathon** · Pharmacogenomics / Explainable AI Track

---

## 🔗 Links

| | |
|---|---|
| 🌐 Live Demo | `[your-deployed-url]` |
| 🎥 LinkedIn Demo Video | `[your-linkedin-video-url]` |
| 📦 GitHub Repository | `[your-github-url]` |

---

## What It Does

Adverse drug reactions kill over 100,000 Americans annually — many preventable through pharmacogenomic testing. PharmaGuard bridges the gap between raw genomic data and clinical action:

1. **Upload a VCF file** — standard genomic variant format from any sequencing provider
2. **Select a drug** — from 6 clinically critical medications
3. **Get a risk prediction** — Safe / Adjust Dosage / Toxic / Ineffective, grounded in CPIC guidelines
4. **Read an AI-generated clinical explanation** — with specific variant citations, biological mechanisms, and dosing alternatives

---

## Supported Drugs & Genes

| Drug | Primary Gene | Clinical Concern |
|------|-------------|-----------------|
| Codeine | CYP2D6 | Morphine toxicity in ultrarapid metabolizers; lack of efficacy in poor metabolizers |
| Warfarin | CYP2C9 | Bleeding risk due to reduced anticoagulant clearance |
| Clopidogrel | CYP2C19 | Antiplatelet failure in poor/intermediate metabolizers |
| Simvastatin | SLCO1B1 | Myopathy risk from impaired hepatic transport |
| Azathioprine | TPMT | Fatal myelosuppression in poor metabolizers |
| Fluorouracil | DPYD | Life-threatening systemic toxicity |

---

## Tech Stack

**Backend**
- [FastAPI](https://fastapi.tiangolo.com/) — REST API framework
- Python 3.10+
- Google Gemini 2.5 Flash — LLM-generated clinical explanations
- Custom pharmacogenomic engine — activity score–based phenotype derivation
- CPIC guideline rules — hardcoded from published 2017–2022 guidelines

**Frontend**
- React (Vite)
- Plain CSS — no UI library dependencies

**Deployment**
- Backend: Render / Railway / any WSGI host
- Frontend: Vercel / Netlify

---

## Architecture

```
VCF File Upload
      │
      ▼
┌─────────────────────────────────┐
│         FastAPI /analyze        │
│                                 │
│  1. VCF Parser                  │
│     • Extracts GENE, STAR, RS   │
│       tags from INFO field      │
│     • Builds diplotype from     │
│       genotype (0/0, 0/1, 1/1) │
│                                 │
│  2. Model Engine                │
│     • Activity score lookup     │
│       per star allele           │
│     • Score → Phenotype         │
│       (PM/IM/NM/RM/URM)        │
│     • Phenotype + Drug →        │
│       CPIC risk label           │
│                                 │
│  3. LLM Engine (Gemini)         │
│     • Prompt includes diplotype,│
│       phenotype, activity score,│
│       and detected variants     │
│     • Returns structured JSON   │
│       with mechanism, impact,   │
│       alternatives, monitoring  │
│     • Graceful fallback if API  │
│       call fails                │
└─────────────────────────────────┘
      │
      ▼
  Structured JSON Response
  (matches required schema exactly)
```

---

## How Phenotype Is Derived

Unlike naive string-matching approaches, PharmaGuard uses an **activity score model** per CPIC translation tables:

```
Diplotype → Per-allele activity scores → Total score → Phenotype

Example: CYP2D6 *1/*4
  *1 → 1.0 (normal function)
  *4 → 0.0 (non-functional, loss-of-function splice defect)
  Total = 1.0 → Intermediate Metabolizer (IM)
  CODEINE + IM → Ineffective (reduced morphine conversion)
```

This means **any valid diplotype produces a phenotype** — not just a hardcoded list of combinations.

---

## Installation & Setup

### Prerequisites
- Python 3.10+
- Node.js 18+
- Google Gemini API key ([get one here](https://aistudio.google.com/))

### Backend

```bash
# Clone the repo
git clone https://github.com/your-org/pharmaguard.git
cd pharmaguard/backend

# Install dependencies
pip install -r requirements.txt

# Set up environment variables
cp .env.example .env
# Edit .env and add your GEMINI_API_KEY

# Run the server
uvicorn main:app --reload --port 8000
```

### Frontend

```bash
cd pharmaguard/frontend

# Install dependencies
npm install

# Set API URL (edit src/config.js or set env var)
# Default points to http://localhost:8000

# Run dev server
npm run dev
```

### Environment Variables

```bash
# .env (backend)
GEMINI_API_KEY=your_gemini_api_key_here
```

---

## API Documentation

### `POST /analyze`

Analyzes a VCF file for pharmacogenomic risk.

**Request** — `multipart/form-data`

| Field | Type | Description |
|-------|------|-------------|
| `file` | `.vcf` file | VCF v4.2 file, max 5MB. Must contain `GENE`, `STAR`, `RS` INFO tags. |
| `drug` | string | Drug name. Supports single or comma-separated list. |

**Supported drug values:** `CODEINE`, `WARFARIN`, `CLOPIDOGREL`, `SIMVASTATIN`, `AZATHIOPRINE`, `FLUOROURACIL`

**Response** — `application/json`

```json
{
  "patient_id": "PATIENT_A3F2C1",
  "drug": "CODEINE",
  "timestamp": "2026-02-19T12:51:10.556984Z",
  "risk_assessment": {
    "risk_label": "Ineffective",
    "confidence_score": 0.85,
    "severity": "moderate"
  },
  "pharmacogenomic_profile": {
    "primary_gene": "CYP2D6",
    "diplotype": "*1/*4",
    "phenotype": "IM",
    "detected_variants": [
      {
        "rsid": "rs1065852",
        "gene": "CYP2D6",
        "star": "*4",
        "genotype": "0/1",
        "diplotype": "*1/*4",
        "ref": "C",
        "alt": "T"
      }
    ]
  },
  "clinical_recommendation": {
    "action": "Monitor for reduced analgesia. Consider lower dose or alternative analgesic.",
    "guideline_source": "CPIC 2019",
    "activity_score": 1.0
  },
  "llm_generated_explanation": {
    "summary": "...",
    "mechanism": "...",
    "variant_impact": "...",
    "clinical_context": "...",
    "alternative_options": "...",
    "monitoring_parameters": "..."
  },
  "quality_metrics": {
    "vcf_parsing_success": true,
    "variants_detected": 2,
    "gene_variants_for_drug": 1,
    "diplotype_source": "vcf_parsed",
    "annotation_completeness": 1.0,
    "llm_explanation_status": "generated"
  }
}
```

**Multiple drugs** — pass `drug` as comma-separated or multiple form fields. Response will be an array.

**Error responses**

| Code | Reason |
|------|--------|
| 400 | Invalid file format, file too large, unsupported drug, malformed VCF |
| 500 | Internal server error |

---

## Sample VCF Files

Sample VCF files for testing are included in `/samples/`:

| File | Variants | Good for testing |
|------|----------|-----------------|
| `sample_cyp2d6_im.vcf` | CYP2D6 *1/*4 | CODEINE → Ineffective |
| `sample_cyp2c19_pm.vcf` | CYP2C19 *2/*2 | CLOPIDOGREL → Ineffective |
| `sample_multi_gene.vcf` | CYP2D6 + CYP2C19 | Multi-drug analysis |
| `sample_wildtype.vcf` | All *1/*1 | Baseline / Safe results |

---

## Deployment

### Backend (Render)

1. Push to GitHub
2. Create new **Web Service** on Render
3. Build command: `pip install -r requirements.txt`
4. Start command: `uvicorn main:app --host 0.0.0.0 --port $PORT`
5. Add `GEMINI_API_KEY` in environment variables

### Frontend (Vercel)

```bash
cd frontend
npm run build
vercel deploy
```

Set `VITE_API_URL` in Vercel environment variables to point to your Render backend URL.

---

## Project Structure

```
pharmaguard/
├── backend/
│   ├── main.py              # FastAPI app, VCF parsing, request handling
│   ├── model_engine.py      # Activity scores, phenotype derivation, CPIC rules
│   ├── llm_engine.py        # Gemini integration, prompt engineering, fallback
│   ├── requirements.txt
│   └── .env.example
├── frontend/
│   ├── src/
│   │   └── App.jsx          # React UI — upload, results, LLM display
│   └── package.json
├── samples/
│   └── *.vcf                # Test VCF files
└── README.md
```

---

## Team

| Name | Role |
|------|------|
| [Your Name] | Backend, ML, LLM integration |
| [Teammate] | Frontend, UI/UX |

---

## Clinical Disclaimer

PharmaGuard is a **research and educational tool** built for the RIFT 2026 Hackathon. It is not a certified medical device and should not be used for actual clinical decision-making without validation by a licensed clinical pharmacist or physician. All recommendations are based on published CPIC guidelines and are intended to demonstrate the feasibility of AI-assisted pharmacogenomic decision support.

---

*Built with 🧬 for RIFT 2026 · #RIFT2026 #PharmaGuard #Pharmacogenomics #AIinHealthcare*