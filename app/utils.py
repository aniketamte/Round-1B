import os
import fitz
from sentence_transformers import SentenceTransformer, util

model = SentenceTransformer("all-MiniLM-L6-v2")

def extract_text_from_pdfs(folder_path):
    pdf_data = {}
    for filename in os.listdir(folder_path):
        if filename.endswith(".pdf"):
            path = os.path.join(folder_path, filename)
            doc = fitz.open(path)
            pages = {}
            for i, page in enumerate(doc):
                text = page.get_text()
                if text.strip():
                    pages[i + 1] = text
            pdf_data[filename] = pages
    return pdf_data

def rank_sections_by_persona_job(pdf_data, persona, job):
    query = f"{persona} - {job}"
    query_emb = model.encode(query, convert_to_tensor=True)

    results = []
    subresults = []

    for doc_name, pages in pdf_data.items():
        for page_num, text in pages.items():
            paragraphs = [p.strip() for p in text.split("\n") if len(p.strip()) > 40]
            for para in paragraphs:
                para_emb = model.encode(para, convert_to_tensor=True)
                score = util.cos_sim(query_emb, para_emb).item()
                results.append((score, doc_name, page_num, para))

    results.sort(reverse=True, key=lambda x: x[0])
    top_sections = []
    top_subsections = []

    seen = set()
    for rank, (score, doc, page, para) in enumerate(results[:10], 1):
        title = para.split(".")[0][:80]
        key = (doc, page, title)
        if key not in seen:
            top_sections.append({
                "document": doc,
                "page_number": page,
                "section_title": title,
                "importance_rank": rank
            })
            top_subsections.append({
                "document": doc,
                "page_number": page,
                "refined_text": para[:500]
            })
            seen.add(key)

    return top_sections, top_subsections
