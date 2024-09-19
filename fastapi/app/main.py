from fastapi import FastAPI, File, UploadFile, Form, status
import cv2
import numpy as np
from pydantic import BaseModel
import base64
from PIL import Image
from imageio import imread
from io import BytesIO
import io
from transformers import TrOCRProcessor, VisionEncoderDecoderModel

app = FastAPI()

processor = TrOCRProcessor.from_pretrained('microsoft/trocr-large-handwritten')
model = VisionEncoderDecoderModel.from_pretrained('microsoft/trocr-large-handwritten')

class HealthCheck(BaseModel):
    """Response model to validate and return when performing a health check."""

    status: str = "OK"

@app.get(
    "/health",
    tags=["healthcheck"],
    summary="Perform a Health Check",
    response_description="Return HTTP Status Code 200 (OK)",
    status_code=status.HTTP_200_OK,
    response_model=HealthCheck,
)
def get_health() -> HealthCheck:
    """
    ## Perform a Health Check
    Endpoint to perform a healthcheck on. This endpoint can primarily be used Docker
    to ensure a robust container orchestration and management is in place. Other
    services which rely on proper functioning of the API service will not deploy if this
    endpoint returns any other HTTP status code except 200 (OK).
    Returns:
        HealthCheck: Returns a JSON response with the health status
    """
    return HealthCheck(status="OK")

@app.post("/predict/model")
async def predict(file: str = Form(...)):
    image_as_bytes = str.encode(file)  # convert string to bytes
    img_recovered = base64.b64decode(image_as_bytes)  # decode base64string
    img = Image.open(BytesIO(img_recovered)).convert("RGB")
   
    if img is None:
        return {"successful": False, "text": ""}
    else:
        return {"successful": True, "text": recognizeText(img)}

@app.put("/detect")
async def predict(file: UploadFile = File(...)):
    data = {"successful": False, "text": ""}

    # convert to numpy image
    img = Image.open(file.file).convert("RGB")

    if img is None:
        return data
    else:
        return {"successful": True, "text": recognizeText(img)}
    
def recognizeText(img):
    pixel_values = processor(images=img, return_tensors="pt").pixel_values
    generated_ids = model.generate(pixel_values)
    generated_text = processor.batch_decode(generated_ids, skip_special_tokens=True)[0]
    return generated_text

def read_cv2_image(base64_string):
    # add padding if base64_string is not a multiple of 4
    base64_string += "=" * ((4 - len(base64_string) % 4) % 4)

    # reconstruct image as an numpy array
    img = Image.open(base64.b64decode(base64_string), encoding="utf-8")

    return img