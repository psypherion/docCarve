import asyncio
from extractor import QuestionExtractor
import os
from typing import List
from dotenv import load_dotenv
from absl import logging

load_dotenv()
logging.set_verbosity(logging.ERROR)


async def main() -> None:
    pdf_dir: str = r"pdfs/"
    pdf_files: List[str] = [f for f in os.listdir(pdf_dir) if f.endswith(".pdf")]
    for pdf_file in pdf_files:
        pdf_path: str = os.path.join(pdf_dir, pdf_file)
        extractor = QuestionExtractor(pdf_path=pdf_path)
        await extractor.run()
    print("All PDFs processed.")