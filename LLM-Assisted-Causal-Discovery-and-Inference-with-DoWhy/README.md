# LLM-Assisted Causal Discovery and Inference (Student Notebook)

This repository contains a short teaching notebook (≈ 15–30 minutes) that walks you through a modern causal workflow:

1. Use a **local LLM** to propose a *plausible* causal DAG (a semantic prior)
2. Visualize that proposed DAG
3. Compare with **statistical causal discovery** (PC algorithm)
4. Estimate a causal effect with **DoWhy**

Dataset: the **Lalonde** job training study (loaded via DoWhy).

Core message:

> LLMs can help you formulate causal assumptions, but causal validity still requires statistical testing and scientific judgment.

---

## What you will do in the notebook

By the end, you should be able to:

- interpret an LLM-generated DAG as a *hypothesis*, not ground truth,
- use PC output as a *statistical hint* about variable relationships,
- choose a conservative **adjustment set** using pre-treatment/domain reasoning,
- encode those assumptions as a DoWhy graph and estimate an ATE.

---

## Quickstart (recommended)

### 1) Create and activate a virtual environment

```bash
python3 -m venv .venv
source .venv/bin/activate
```

Windows (PowerShell):

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
```

### 2) Install dependencies

```bash
python -m pip install -r requirements.txt
```

### 3) Start Jupyter

```bash
jupyter notebook
```

### 4) Open the notebook

Open:

`notebooks/llm_causal_discovery_and_inf.ipynb`

---

## Optional: run a local LLM (recommended)

The notebook uses the **OpenAI Python SDK** against an **OpenAI-compatible local server**.
No cloud API keys are required for local usage.

### Option A — Ollama (recommended)

1. Install Ollama: https://ollama.com/
2. Pull the model used in the notebook by default:

```bash
ollama pull phi4
```

3. Start the server:

```bash
ollama serve
```

Default OpenAI-compatible base URL:

```text
http://localhost:11434/v1
```

### Option B — LM Studio

1. Install LM Studio: https://lmstudio.ai/
2. Enable **Local Server** mode.

Typical base URL:

```text
http://localhost:1234/v1
```

---

## If you don’t have an LLM running

That’s okay.

If the notebook cannot reach a local LLM server, it will **fall back to a built-in JSON DAG** so you can still:

- visualize a “semantic prior” graph,
- run PC,
- build a DoWhy graph,
- estimate the causal effect and run refuters.

---

## Troubleshooting

### “ModuleNotFoundError: …”
Make sure your environment is activated and dependencies are installed:

```bash
source .venv/bin/activate
python -m pip install -r requirements.txt
```

### Local LLM connection fails
- Check that the server is running (`ollama serve` or LM Studio local server).
- Verify the notebook’s `BASE_URL` matches your server.

### Interpreting the results
- PC graphs can be partially oriented and unstable on mixed data (binary + continuous). Treat it as a hint.
- The DoWhy estimate is only as valid as the *graph assumptions* and the *adjustment set*.
