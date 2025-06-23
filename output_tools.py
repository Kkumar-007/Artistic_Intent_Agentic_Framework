import json
from tools import ArtAnalysisTools
import sys
import os
from docx import Document  # <-- Use this to read .docx files

# Determine the directory where run.py resides
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Construct an absolute path to the .docx file
doc_path = os.path.join(BASE_DIR, "Data", "Starry_Night.docx")

# Use python-docx to read the document
doc = Document(doc_path)
document_text = "\n".join([para.text for para in doc.paragraphs])

# Now use your tool
tools = ArtAnalysisTools()
artwork_info = tools.extract_artwork_info(document_text)
period_from_text = tools._detect_periods_from_text(document_text)
fuzzy_color = tools._extract_colors_fuzzy(document_text)
historical_perspective = tools.parse_historical_perspectives(document_text)


print("=== TOOLS.PY OUTPUT ===")
print("ArtAnalysisTools.extract_artwork_info() results:")
print(json.dumps(artwork_info, indent=2))
# print("ArtAnalysisTools._determine_periods_with_confidence() results:")
print("ArtAnalysisTools._detect_periods_from_text() results:")
print(json.dumps(period_from_text, indent=2))
print("ArtAnalysisTools._extract_colors_fuzzy() results:")
print(json.dumps(fuzzy_color, indent=2))
print("ArtAnalysisTools.parse_historical_perspectives() results:")
print(json.dumps(historical_perspective, indent=2))