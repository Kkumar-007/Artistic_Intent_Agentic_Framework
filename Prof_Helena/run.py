from docx import Document
import os

# Extract text from .docx
doc_path = os.path.join('Data', 'Starry_Night.docx')
doc = Document(doc_path)
text = '\n'.join([p.text for p in doc.paragraphs])

img_path = os.path.join('Data', 'Starry_Night.jpg')

# Run analysis
from main import ProfessorHelena
import asyncio

helena = ProfessorHelena(
    text_model="llama3.1:8b",
    vision_model="llava:13b"
)

critique = asyncio.run(
    helena.analyze_artwork_with_image(
        artwork_description=text,
        image_path=img_path
    )
)

print(critique)