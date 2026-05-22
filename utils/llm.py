"""
utils/llm.py
Loads the HuggingFace model once and exposes it as a LangChain-compatible LLM.
All agents and chains import from here so the model is never loaded twice.
"""

from langchain_community.llms import HuggingFacePipeline
from transformers import pipeline, AutoTokenizer
import torch

# ── Model config ───────────────────────────────────────────────────────────────
# flan-t5-base  → ~1GB RAM, CPU-friendly, good for structured tasks
# flan-t5-large → ~3GB RAM, better quality
# TinyLlama/TinyLlama-1.1B-Chat-v1.0 → better chat, ~2GB RAM
MODEL_NAME = "google/flan-t5-base"

_llm = None


def get_llm() -> HuggingFacePipeline:
    """Return the shared LangChain LLM instance (loaded once)."""
    global _llm
    if _llm is None:
        print(f"[LLM] Loading '{MODEL_NAME}'...")
        device = 0 if torch.cuda.is_available() else -1

        hf_pipe = pipeline(
            "text2text-generation",
            model=MODEL_NAME,
            device=device,
            max_new_tokens=512,
            do_sample=False,
        )
        _llm = HuggingFacePipeline(pipeline=hf_pipe)
        print(f"[LLM] Ready on {'GPU' if device == 0 else 'CPU'}")
    return _llm
