import PIL.Image
import os
import google.generativeai as genai
import json
from absl import logging
logging.set_verbosity(logging.ERROR)


# Configure the Gemini API
genai.configure(api_key="AIzaSyCaCE6OsDkyv5jWP46XvCOvNkvZP7KdgIs")
model = genai.GenerativeModel(model_name="gemini-1.5-pro")

# Define the prompt for extracting questions
prompt = """
There are almost 100 mcq questions in the following images extarct them.
Remember to send all the 100 questions.
Extract mcq questions and their options from the following images.
and also provide the answer of the question in the answer part.
Provide the output in JSON format with the structure:
{
  "questions": [
    {
      "question_no": <int>,
      "question": <str>,
      "options": {
        "a": <str>,
        "b": <str>,
        "c": <str>,
        "d": <str>
      },
      "answer": <str>
    }
  ]
}
"""

# Set up image paths
image_dir = "paper_2_X/images/"
img_files = [prompt]

# Load all .jpg files from the directory
for img_path in os.listdir(image_dir):
    if img_path.endswith(".jpg"):
        img_files.append(PIL.Image.open(os.path.join(image_dir, img_path)))

# Send the request to Gemini API
response = model.generate_content(img_files)

print(response.text)

with open("output.txt", "w") as f:
    f.write(response.text)



import asyncio
from pdfslicer import PDFToImageConverter

async def main():
    # Initialize the PDF slicer with the path to your PDF
    pdf_slicer = PDFToImageConverter(pdf_path=r"pdfs/paper_2_X.pdf")
    
    # Convert PDF to images
    image_streams = await pdf_slicer.convert_pdf_to_images()
    
    # Save the images to a directory
    await pdf_slicer.save_images(image_streams)

if __name__ == "__main__":
    asyncio.run(main())
