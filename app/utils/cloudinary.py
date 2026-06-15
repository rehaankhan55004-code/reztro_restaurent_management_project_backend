import cloudinary
import cloudinary.uploader

from fastapi import FastAPI, UploadFile, File, HTTPException
from app.core.config import settings

app = FastAPI()

# CLOUDINARY CONFIG

cloudinary.config(
    cloud_name=settings.CLOUD_NAME,
    api_key=settings.API_KEY,
    api_secret=settings.API_SECRET,
    secure=True
)

# Allowed file types
ALLOWED_TYPES = ["image/jpeg", "image/png", "image/webp"]


# UPLOAD IMAGE TO CLOUDINARY

def upload_to_cloudinary(file: UploadFile, folder: str = "reztro"):
    try:
        # Validate file type
        if file.content_type not in ALLOWED_TYPES:
            raise HTTPException(
                status_code=400,
                detail="Invalid file type. Only JPEG, PNG, WEBP allowed."
            )

        # Upload file
        result = cloudinary.uploader.upload(
            file.file,
            folder=folder
        )

        return {
            "url": result.get("secure_url"),
            "public_id": result.get("public_id")
        }

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Upload failed: {str(e)}"
        )


# DELETE IMAGE FROM CLOUDINARY

def delete_from_cloudinary(public_id: str):
    try:
        result = cloudinary.uploader.destroy(public_id)

        return {
            "result": result
        }

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Delete failed: {str(e)}"
        )


# FASTAPI ROUTES

@app.post("/upload-image")
async def upload_image(file: UploadFile = File(...)):
    result = upload_to_cloudinary(file)

    return {
        "message": "Image uploaded successfully",
        "data": result
    }


@app.delete("/delete-image/{public_id}")
async def delete_image(public_id: str):
    result = delete_from_cloudinary(public_id)

    return {
        "message": "Image deleted successfully",
        "data": result
    }