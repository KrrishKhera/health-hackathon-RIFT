# Variant-RX — Pharmacogenomic Risk Prediction System

> **Transforming Genetic Data into Safer Prescriptions.**
> Clinical decision support that analyzes patient VCF files to predict personalized drug risks and generate explainable, CPIC-aligned recommendations — with zero external API dependencies.

**RIFT 2026 Hackathon** · Pharmacogenomics / Explainable AI Track

---

## 🔗 Submission Links

| | |
|---|---|
| 🌐 **Live Demo** | https://health-hackathon-rift.vercel.app |
| 🎥 **LinkedIn Video** | `[your-linkedin-video-url]` |
| 📦 **GitHub Repository** | https://github.com/KrrishKhera/health-hackathon-RIFT.git |
| ⚙️ **Backend API** | https://health-hackathon-rift.onrender.com |

---

## Screenshots

| | |
|---|---|
| <img width="600" src="https://github.com/user-attachments/assets/1ccb6131-849a-41a0-acee-e5d198e8281d" /> | <img width="600" src="https://github.com/user-attachments/assets/b0b7f519-a4b8-409b-9910-2e697e260280" /> |
| <img width="600" src="https://github.com/user-attachments/assets/e2aef9ad-a512-46f5-af5a-ec38c0e8102a" /> | <img width="600" src="https://github.com/user-attachments/assets/9fbc81de-4800-4456-89e0-4745b5da2127" /> |

<img width="1280" src="https://github.com/user-attachments/assets/e7873339-df54-4f24-ad8b-0842182415cb" />

---

## Problem Statement

Adverse drug reactions kill over **100,000 Americans annually** — many of which are preventable through pharmacogenomic testing. A patient's genetic variants directly affect how their body metabolizes medications, yet this information is rarely integrated into prescribing decisions due to the complexity of interpreting genomic data.

VariantRX bridges this gap by automating the full pipeline: from raw VCF genomic data to actionable clinical risk predictions with structured explanations grounded in published CPIC guidelines.

---

## Features

- **VCF File Parsing** — Supports standard VCF v4.2 format with `GENE`, `STAR`, `RS` INFO tags
- **Activity Score–Based Phenotype Derivation** — Any valid diplotype produces a phenotype via CPIC translation tables, not brittle string matching
- **CPIC-Aligned Risk Prediction** — Safe / Adjust Dosage / Toxic / Ineffective across 6 drug-gene pairs
- **Rule-Based Clinical Explanation Engine** — Deterministic, structured explanations with variant citations, biological mechanisms, alternatives, and monitoring parameters — instant and consistent, no external API
- **Multi-Drug Analysis** — Analyze multiple drugs from a single VCF upload in one request
- **Structured JSON Output** — Schema-compliant response for every request
- **Zero External API Dependencies** — Fully self-contained backend, no rate limits, no API keys required

---

## Supported Drug–Gene Pairs

| Drug | Gene | Phenotypes | Primary Risk |
|------|------|-----------|-------------|
| Codeine | CYP2D6 | PM, IM, NM, RM, URM | Toxicity (URM) / Inefficacy (PM) |
| Warfarin | CYP2C9 | PM, IM, NM | Bleeding risk |
| Clopidogrel | CYP2C19 | PM, IM, NM, RM, URM | Antiplatelet failure |
| Simvastatin | SLCO1B1 | Poor/Decreased/Normal Function | Myopathy |
| Azathioprine | TPMT | PM, IM, NM | Fatal myelosuppression |
| Fluorouracil | DPYD | PM, IM, NM | Life-threatening systemic toxicity |

---

## Tech Stack

### Backend
| Technology | Purpose |
|-----------|---------|
| Python 3.11 | Runtime |
| FastAPI | REST API framework |
| Uvicorn | ASGI server |
| Rule-Based Explanation Engine | Deterministic clinical explanations per CPIC guidelines |
| python-multipart | VCF file upload handling |

### Frontend
| Technology | Purpose |
|-----------|---------|
| React 18 | UI framework |
| Vite | Build tool |
| React Router v6 | Client-side routing |
| Axios | HTTP client |
| Tailwind CSS | Styling |

### Deployment
| Service | Purpose |
|---------|---------|
| Render | Backend hosting |
| Vercel | Frontend hosting |

---

## Architecture

```
Browser (React Frontend)
        │
        │  POST /analyze
        │  multipart/form-data
        │  { file: .vcf, drug: [...] }
        ▼
┌──────────────────────────────────────────┐
│           FastAPI Backend                │
│                                          │
│  ┌─────────────────────────────────┐     │
│  │         VCF Parser              │     │
│  │  • Reads ##fileformat header    │     │
│  │  • Extracts GENE, STAR, RS      │     │
│  │    from INFO field              │     │
│  │  • Builds diplotype from        │     │
│  │    genotype (0/0→*1/*1,         │     │
│  │    0/1→*1/STAR, 1/1→STAR/STAR) │     │
│  └────────────────┬────────────────┘     │
│                   │                      │
│  ┌────────────────▼────────────────┐     │
│  │        Model Engine             │     │
│  │  • Activity score lookup        │     │
│  │    per star allele per gene     │     │
│  │  • Score → Phenotype            │     │
│  │    (PM/IM/NM/RM/URM)           │     │
│  │  • Phenotype + Drug →           │     │
│  │    CPIC risk label +            │     │
│  │    confidence + severity        │     │
│  └────────────────┬────────────────┘     │
│                   │                      │
│  ┌────────────────▼────────────────┐     │
│  │   Rule-Based Explanation Engine │     │
│  │  • Deterministic templates      │     │
│  │    per gene, phenotype, drug    │     │
│  │  • Cites detected variants      │     │
│  │    and activity scores          │     │
│  │  • Biological mechanism per     │     │
│  │    gene pathway                 │     │
│  │  • CPIC-aligned alternatives    │     │
│  │    and monitoring parameters    │     │
│  │  • Instant — zero latency       │     │
│  └─────────────────────────────────┘     │
└──────────────────────────────────────────┘
        │
        │  Structured JSON Response
        ▼
Browser → ResultDashboard
  • Color-coded risk labels
  • Tabbed multi-drug view
  • Expandable clinical explanation
  • Download / Copy JSON
```

### Phenotype Derivation Model

```
Diplotype  →  Per-allele activity scores  →  Total score  →  Phenotype

CYP2D6 *1/*4:
  *1 = 1.0 (wildtype, normal function)
  *4 = 0.0 (non-functional, splice defect at rs3892097)
  Total = 1.0  →  Intermediate Metabolizer (IM)
  CODEINE + IM  →  Ineffective (0.85 confidence, moderate severity)
```

### Explanation Engine Design

Rather than relying on an external LLM API, VariantRX uses a deterministic rule-based explanation engine. Each explanation is composed from clinically validated templates parameterized by gene, diplotype, phenotype, activity score, and detected variants. This approach guarantees:

- **Consistency** — identical inputs always produce identical outputs
- **Speed** — zero network latency, sub-millisecond generation
- **Reliability** — no API rate limits, quota exhaustion, or downtime
- **Clinical accuracy** — templates written directly from CPIC guideline text

---

## Project Structure

```
├── backend/
│   ├── main.py              # FastAPI app, VCF parsing, request handling
│   ├── model_engine.py      # Activity scores, phenotype derivation, CPIC rules
│   ├── llm_engine.py        # Rule-based clinical explanation engine
│   ├── requirements.txt     # Python dependencies
│   └── runtime.txt          # Python version pin (3.11.0)
├── frontend/
│   ├── src/
│   │   ├── App.jsx                    # Router setup
│   │   ├── pages/
│   │   │   ├── HomePage.jsx           # Upload + drug selection
│   │   │   └── ResultDashboard.jsx    # Results display
│   │   └── components/
│   │       ├── VCFUploader.jsx
│   │       └── DrugSelector.jsx
│   ├── vercel.json          # SPA routing fix for Vercel
│   └── package.json
├── sample_vcfs/             # Test VCF files
├── .env.example
└── README.md
```

---

## Local Setup & Installation

### Prerequisites
- Python 3.11+
- Node.js 18+
- No API keys required

---

### Backend

```bash
# 1. Clone the repository
git clone https://github.com/KrrishKhera/health-hackathon-RIFT.git
cd health-hackathon-RIFT

# 2. Create and activate virtual environment
python -m venv venv

# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate

# 3. Install dependencies
cd backend
pip install -r requirements.txt

# 4. Start the backend server
uvicorn main:app --reload --port 8000
```

Backend running at: `http://localhost:8000`
API docs at: `http://localhost:8000/docs`

---

### Frontend

```bash
# From project root
cd frontend

# 1. Install dependencies
npm install

# 2. Create frontend/.env
echo "VITE_BACKEND_URL=http://localhost:8000" > .env

# 3. Start dev server
npm run dev
```

Frontend running at: `http://localhost:5173`

---

### Environment Variables

**Frontend only** — `frontend/.env`
```env
VITE_BACKEND_URL=http://localhost:8000
```

**`.env.example`**
```env
VITE_BACKEND_URL=http://localhost:8000
```

No backend environment variables required.

---

## API Documentation

### `POST /analyze`

Analyzes a VCF file for pharmacogenomic risk against one or more drugs.

**Request** — `multipart/form-data`

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `file` | `.vcf` file | Yes | VCF v4.2 file. Max 5MB. Must contain `GENE`, `STAR`, `RS` INFO tags. |
| `drug` | string | Yes | Drug name(s). Comma-separated or multiple fields. Case-insensitive. |

**Supported drug values:**
`CODEINE` · `WARFARIN` · `CLOPIDOGREL` · `SIMVASTATIN` · `AZATHIOPRINE` · `FLUOROURACIL`

**Example Request**
```bash
curl -X POST https://health-hackathon-rift.onrender.com/analyze \
  -F "file=@sample_vcfs/cyp2d6_im.vcf" \
  -F "drug=CODEINE" \
  -F "drug=WARFARIN"
```

**Response Schema**
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
    "llm_explanation_status": "rule_based"
  }
}
```

For multiple drugs, response is an array of the above objects.

**Error Responses**

| Code | Detail |
|------|--------|
| 400 | Invalid file format — only `.vcf` allowed |
| 400 | File size exceeds 5MB limit |
| 400 | Unsupported drug(s) |
| 400 | Invalid VCF header format |
| 400 | Missing `#CHROM` column header |
| 500 | Internal server error |

---

## Sample VCF Files

Located in `sample_vcfs/`. Use these to test the application:

| File | Gene Variant | Best Drug to Test | Expected Result |
|------|-------------|------------------|-----------------|
| `cyp2d6_im.vcf` | CYP2D6 *1/*4 | CODEINE | Ineffective (IM) |
| `cyp2c19_pm.vcf` | CYP2C19 *2/*2 | CLOPIDOGREL | Ineffective (PM) |
| `multi_gene.vcf` | CYP2D6 + CYP2C19 | CODEINE + CLOPIDOGREL | Multi-drug results |
| `wildtype.vcf` | All *1/*1 | Any | Safe (NM) |

---

## Deployment

### Backend (Render)

1. Push to GitHub
2. Go to [render.com](https://render.com) → New → Web Service
3. Connect GitHub repo
4. Configure:
```
Root Directory:  backend
Build Command:   pip install -r requirements.txt
Start Command:   python -m uvicorn main:app --host 0.0.0.0 --port $PORT
```
5. Environment Variables:
```
PYTHON_VERSION = 3.11.0
```
6. Deploy

### Frontend (Vercel)

1. Go to [vercel.com](https://vercel.com) → New Project → Import GitHub repo
2. Configure:
```
Root Directory:  frontend
Framework:       Vite
Build Command:   npm run build
Output Dir:      dist
```
3. Environment Variables:
```
VITE_BACKEND_URL = https://health-hackathon-rift.onrender.com
```
4. Deploy

---

## Usage

1. Open the live app at https://health-hackathon-rift.vercel.app
2. Upload a `.vcf` file (use files from `sample_vcfs/` to test)
3. Select one or more drugs from the panel
4. Click **Analyze**
5. View color-coded risk results:
   - 🟢 **Safe** — standard dosing recommended
   - 🟡 **Adjust Dosage** — dose modification required
   - 🔴 **Toxic / Ineffective** — avoid or switch to alternative
6. Expand each section to read the structured clinical explanation
7. Download or copy the structured JSON output

---

## Team

| Name | Role |
|------|------|
| Krrish Khera | Backend, Deployment |
| Aman Anilkumar | Frontend, UI/UX, Deployment |
| Vaibhav Jain | Model Engine, Explanation Engine |

---

## Clinical Disclaimer

VariantRX is a **research and educational prototype** built for the RIFT 2026 Hackathon. It is not a certified medical device and must not be used for actual clinical decision-making without review by a licensed clinical pharmacist or physician. All risk predictions are based on published CPIC guidelines (2017–2022) and are intended to demonstrate the feasibility of AI-assisted pharmacogenomic decision support.

