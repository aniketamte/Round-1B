import os
import json
from datetime import datetime
from utils import extract_text_from_pdfs, rank_sections_by_persona_job

INPUT_DIR = "/app/input"
OUTPUT_DIR = "/app/output"

def main():
    persona = os.environ.get("PERSONA", "PhD Researcher in Computational Biology")
    job = os.environ.get("JOB", "Prepare a comprehensive literature review focusing on methodologies, datasets, and performance benchmarks")

    pdf_text_data = extract_text_from_pdfs(INPUT_DIR)
    sections, subsections = rank_sections_by_persona_job(pdf_text_data, persona, job)

    output = {
        "metadata": {
            "input_documents": list(pdf_text_data.keys()),
            "persona": persona,
            "job_to_be_done": job,
            "timestamp": datetime.utcnow().isoformat()
        },
        "extracted_sections": sections,
        "subsection_analysis": subsections
    }

    with open(os.path.join(OUTPUT_DIR, "output.json"), "w") as f:
        json.dump(output, f, indent=2)

if __name__ == "__main__":
    main()
