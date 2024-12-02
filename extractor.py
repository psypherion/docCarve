import PIL.Image
import os
import google.generativeai as genai
import json
from absl import logging
logging.set_verbosity(logging.ERROR)
import asyncio
from pdfslicer import PDFToImageConverter
import re

GEMINI_API_KEY: str = os.getenv("GEMINI_API_KEY")
MODELNAME: str = "gemini-1.5-pro"

PROMPT: str = """
Please extract all MCQ questions and their options from the images provided. 
Ensure you include answers for each question where possible.

The expected output should be in the following JSON format:
{
  "questions": [
    {
      "question_no": <int>,
      "question": "<str>",
      "options": {
        "a": "<str>",
        "b": "<str>",
        "c": "<str>",
        "d": "<str>"
      },
      "answer": "<str>"
    }
  ]
}

Key Points:
- Include **all questions** present in the images (up to 100 or more).
- Ensure each question has four options (a, b, c, d).
- Provide the answer to each question in the "answer" field.
- If an answer is not clear from the image, leave the "answer" field blank.
- Parse and include even partially visible questions if possible.

Deliver the output in valid JSON format.
"""

PDF_PATH: str = r"pdfs/paper_2_X.pdf"

class QuestionExtractor:
    def __init__(self, model_name: str = MODELNAME, prompt: str = PROMPT, api_key: str = GEMINI_API_KEY, pdf_path: str = PDF_PATH):
        # Configure GEMINI API
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel(model_name=model_name)
        self.prompt = prompt
        self.pdf_path = pdf_path

    async def pdf_to_images(self):
        pdf_slicer = PDFToImageConverter(pdf_path=self.pdf_path)
        image_streams = await pdf_slicer.convert_pdf_to_images()
        image_dir = await pdf_slicer.save_images(image_streams)
        return image_dir

    async def extract_questions(self, image_dir: str):
        image_files = [PIL.Image.open(os.path.join(image_dir, img_path)) for img_path in os.listdir(image_dir)]
        prompted_files = image_files.insert(0, self.prompt)
        response = await self.model.generate(prompted_files)
        return response.text
    
    async def jsonify(self, response: str):
        pattern: str = r"```json\n(.*?)\n```"
        matches = re.findall(pattern, response, re.DOTALL)
        return matches
    
    async def save_json(self, json_data: str):
        with open("output.json", "w") as json_file:
            json.dump(json_data, json_file, indent=4)
        return True
    
    async def run(self):
        image_dir = await self.pdf_to_images()
        response = await self.extract_questions(image_dir)
        json_data = await self.jsonify(response)
        await self.save_json(json_data)
        return "Done !!"
    

if __name__ == "__main__":
    extractor = QuestionExtractor()
    asyncio.run(extractor.run())