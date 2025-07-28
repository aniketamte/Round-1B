# Persona-Driven Document Intelligence (Round 1B)

## Overview
This solution extracts and ranks relevant sections and sub-sections from a PDF collection based on a persona and job-to-be-done prompt.

## Input
- A folder of 3–10 related PDF files in `/app/input`
- Environment variables:
  - `PERSONA`
  - `JOB`

## Output
- `/app/output/output.json` containing metadata, ranked sections, and sub-section text.

## Build and Run

```bash
docker build --platform linux/amd64 -t persona_doc_ai:test .

docker run --rm \
  -v $(pwd)/input:/app/input \
  -v $(pwd)/output:/app/output \
  -e PERSONA="Investment Analyst" \
  -e JOB="Analyze revenue trends, R&D investments..." \
  --network none \
  persona_doc_ai:test
```

## Output Structure
```json
{
  "metadata": {...},
  "extracted_sections": [
    {
      "document": "doc1.pdf",
      "page_number": 3,
      "section_title": "Revenue Growth Trends",
      "importance_rank": 1
    }
  ],
  "subsection_analysis": [
    {
      "document": "doc1.pdf",
      "page_number": 3,
      "refined_text": "The revenue increased by 23%..."
    }
  ]
}
```
