import asyncio
import json
import os
import re
from typing import List

import PIL.Image
from absl import logging
from dotenv import load_dotenv
import google.generativeai as genai

from pdfslicer import PDFToImageConverter

# Load environment variables
load_dotenv()

# Configure logging
logging.set_verbosity(logging.ERROR)


# Constants
GEMINI_API_KEY: str = os.getenv("GEMINI_API_KEY")
MODEL_NAME: str = "gemini-1.5-pro"

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
    def __init__(
        self,
        model_name: str = MODEL_NAME,
        prompt: str = PROMPT,
        api_key: str = GEMINI_API_KEY,
        pdf_path: str = PDF_PATH,
    ):
        """Initialize the QuestionExtractor."""
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel(model_name=model_name)
        self.prompt = prompt
        self.pdf_path = pdf_path

    async def pdf_to_images(self) -> str:
        """Convert the PDF to images and save them."""
        pdf_slicer = PDFToImageConverter(pdf_path=self.pdf_path)
        image_streams = await pdf_slicer.convert_pdf_to_images()
        image_dir = await pdf_slicer.save_images(image_streams)
        print("1")
        return image_dir

    async def extract_questions(self, image_dir: str) -> str:
        """Extract questions from images using the model."""
        image_files: List[PIL.Image.Image] = [
            PIL.Image.open(os.path.join(image_dir, img_path))
            for img_path in os.listdir(image_dir)
        ]
        image_files.insert(0, self.prompt)  # Add prompt to the list
        print(image_files)
        response = self.model.generate_content(image_files)
        print("2")
        return response.text

    @staticmethod
    async def jsonify(response: str) -> List[dict]:
        """Extract JSON data from the response using regex."""
        pattern: str = r"```json\n(.*?)\n```"
        matches = re.findall(pattern, response, re.DOTALL)
        print("3")
        return [json.loads(match) for match in matches]

    @staticmethod
    async def save_json(json_data: List[dict], file_name: str = "output.json") -> bool:
        """Save the extracted JSON data to a file."""
        with open(file_name, "w") as json_file:
            json.dump(json_data, json_file, indent=4)
        print("4")
        return True

    async def run(self) -> str:
        """Run the entire extraction process."""
        image_dir = await self.pdf_to_images()
        response = await self.extract_questions(image_dir)
        response_file: str = self.pdf_path.split("/")[-1].split(".")[0]
        with open(f"{response_file}_response.txt", "w") as responsed:
            responsed.write(response)
        with open(f"{response_file}_output.txt", "r") as output:
            content = output.read()
        json_data = await self.jsonify(content)
        await self.save_json(json_data)
        print("5")
        return "Done!"


if __name__ == "__main__":
    extractor = QuestionExtractor()
    asyncio.run(extractor.run())
