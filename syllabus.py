import asyncio
import os
import json
import PIL.Image
from absl import logging
from dotenv import load_dotenv
import google.generativeai as genai
from pdfslicer import PDFToImageConverter
import re

# Load environment variables
load_dotenv()

# Configure logging
logging.set_verbosity(logging.ERROR)

# Constants
GEMINI_API_KEY: str = os.getenv("GEMINI_API_KEY")
MODEL_NAME: str = "gemini-1.5-pro"

SYLLABUS_PROMPT: str = """
Please extract the syllabus content from the provided images. 

The syllabus contains:
1. Units: High-level categories of the syllabus (e.g., Unit 1: Discrete Structures).
2. Topics: Subcategories within each unit (e.g., Set Theory, Group Theory).

The expected output should be structured in JSON format as follows:
{
  "units": [
    {
      "unit_no": <int>,
      "unit_name": "<str>",
      "topics": [
        "<str>", "<str>", "<str>", ...
      ]
    }
  ]
}

Key Points:
- Ensure that all units and their topics are included.
- For any ambiguous or partially visible text, try your best to reconstruct it, but label incomplete units or topics as "Incomplete" if unsure.
- Organize the topics under the correct unit where possible.
- Provide valid JSON as the final output.
"""

PDF_PATH: str = r"syllabus/syllabus.pdf"


class SyllabusExtractor:
    def __init__(
        self,
        model_name: str = MODEL_NAME,
        prompt: str = SYLLABUS_PROMPT,
        api_key: str = GEMINI_API_KEY,
        pdf_path: str = PDF_PATH,
    ):
        """Initialize the SyllabusExtractor."""
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel(model_name=model_name)
        self.prompt = prompt
        self.pdf_path = pdf_path

    async def pdf_to_images(self) -> str:
        """Convert the syllabus PDF to images and save them."""
        pdf_slicer = PDFToImageConverter(pdf_path=self.pdf_path)
        image_streams = await pdf_slicer.convert_pdf_to_images()
        image_dir = await pdf_slicer.save_images(image_streams)
        return image_dir

    async def extract_syllabus(self, image_dir: str) -> str:
        """Extract syllabus content from images using the model."""
        image_files = [PIL.Image.open(os.path.join(image_dir, img)) for img in os.listdir(image_dir)]
        print(image_files)
        image_files.insert(0, self.prompt)  # Add the prompt as the first input
        response = self.model.generate_content(image_files)
        with open("syllabus_response.txt", "w") as response_file:
            response_file.write(response)
        return response

    @staticmethod
    async def jsonify(response: str) -> dict:
        """Extract JSON data from the response using regex."""
        pattern = r"```json\n(.*?)\n```"
        matches = re.findall(pattern, response, re.DOTALL)
        return json.loads(matches[0]) if matches else {}

    async def save_json(self, json_data: dict, file_name: str = "syllabus.json") -> None:
        """Save the extracted JSON data to a file."""
        with open(file_name, "w") as json_file:
            json.dump(json_data, json_file, indent=4)

    async def run(self) -> str:
        """Run the entire syllabus extraction process."""
        image_dir = await self.pdf_to_images()
        response = await self.extract_syllabus(image_dir)
        json_data = await self.jsonify(response)
        await self.save_json(json_data)
        return "Syllabus extraction completed!"


if __name__ == "__main__":
    extractor = SyllabusExtractor()
    asyncio.run(extractor.run())
