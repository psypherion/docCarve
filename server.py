from starlette.applications import Starlette
from starlette.responses import JSONResponse
from starlette.routing import Route
from starlette.responses import StreamingResponse, HTMLResponse
import os
from pdfslicer import PDFToImageConverter  # Assuming it's in pdfslicer.py

base_dir = os.path.dirname(os.path.abspath(__file__))
pdf_src = r"pdfs/paper_2_X.pdf"  # Path to your PDF file

# Instantiate PDFToImageConverter
pdf_converter = PDFToImageConverter(pdf_path=os.path.join(base_dir, pdf_src))

# Route to fetch all pages as images
async def get_all_pdf_pages(request):
    # Convert PDF pages to images
    image_streams = await pdf_converter.convert_pdf_to_images()
    
    # Generate the URLs for the images to serve them dynamically (based on page numbers)
    image_urls = [f"/pdf-images/{i+1}" for i in range(len(image_streams))]
    
    return JSONResponse({"images": image_urls, "totalPages": len(image_streams)})

# Function to serve individual pages
async def convert_and_serve_image(request):
    page_number = int(request.path_params['page_number']) - 1  # Page numbers start from 1

    # Convert PDF pages to images
    image_streams = await pdf_converter.convert_pdf_to_images()

    if page_number < len(image_streams):
        image_stream = image_streams[page_number]

        # Return the image as a stream
        return StreamingResponse(image_stream, media_type="image/jpeg")
    else:
        return HTMLResponse("Page not found", status_code=404)

# Define your routes
routes = [
    Route("/pdf-images/{page_number}", convert_and_serve_image),
    Route("/pdf-images/pages", get_all_pdf_pages),  # New route to get all images
]

# Initialize the app
app = Starlette(debug=True, routes=routes)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
