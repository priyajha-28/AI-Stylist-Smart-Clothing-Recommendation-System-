
"""
llm_descriptions.py - robust simplified implementation
Generates mock JSON description files for PNGs in uploads/.
"""

import json
from pathlib import Path

PROJECT_ROOT = Path(__file__).parent
UPLOADS = PROJECT_ROOT / "uploads"
DESCRIPTIONS_DIR = PROJECT_ROOT / "descriptions"

PROMPT_TEMPLATE = """SYSTEM / INSTRUCTION:
You are an image-aware fashion copywriter. Analyze the provided outfit PNG and produce an HTML-ready, user-facing description block...
(Full prompt omitted here for brevity in the file; use full prompt when calling external LLM.)
"""

def build_prompt(filename, image_path):
    return PROMPT_TEMPLATE + f"\nFILENAME: {filename}\nIMAGE_PATH: {image_path}\n"

def mock_generate_for_filename(filename):
    name = Path(filename).stem.replace('_', ' ').title()
    headline = f"{name} — Tailored Layered Outfit With Detail"
    desc = f"A {name.lower()} showing layered silhouettes, visible texture and tailored lines; neutral tones with subtle contrast and structured details."
    eco = "Repair small wear, prefer secondhand sourcing, and launder in cold water then line-dry to reduce energy use."
    tip = "Add a slim belt and low-profile loafers for balance."
    card = (
        '<div class="outfit-card" style="font-family: Montserrat, sans-serif; color:#333; '
        'background: rgba(255,255,255,0.88); border:1px solid #ddd; box-shadow:0 6px 18px rgba(0,0,0,0.06); '
        'border-radius:12px; padding:14px; max-width:420px;">'
        f'<h3 class="outfit-title" style="margin:0 0 8px; font-weight:700;">{headline}</h3>'
        f'<p class="outfit-desc" style="margin:0 0 8px;">{desc}</p>'
        f'<p class="eco" style="margin:0 0 8px;"><strong style="color:#F4D03F;">Eco:</strong> {eco}</p>'
        f'<p class="tip" style="margin:0; font-style:italic;">{tip}</p>'
        '</div>'
    )
    plain = f"{headline}\n{desc}\nEco: {eco}\nTip: {tip}"
    return {
        "filename": filename,
        "description_html": card,
        "plain_text": plain,
        "language": "en"
    }

def generate_descriptions_for_uploads(output_folder="descriptions"):
    DESCRIPTIONS_DIR = PROJECT_ROOT / output_folder
    DESCRIPTIONS_DIR.mkdir(exist_ok=True)
    created = []
    for p in UPLOADS.glob("*"):
        if p.suffix.lower() not in (".png", ".jpg", ".jpeg"):
            continue
        out = mock_generate_for_filename(p.name)
        with open(DESCRIPTIONS_DIR / (p.stem + ".json"), "w", encoding="utf-8") as f:
            json.dump(out, f, ensure_ascii=False, indent=2)
        created.append(DESCRIPTIONS_DIR / (p.stem + ".json"))
    return created

if __name__ == "__main__":
    created = generate_descriptions_for_uploads()
    print("Created description files:", created)
