import cloudinary
import cloudinary.uploader

from fastapi import APIRouter, UploadFile, File, HTTPException
from app.core.config import settings

# CLOUDINARY CONFIG

cloudinary.config(
    cloud_name=settings.CLOUD_NAME,
    api_key=settings.API_KEY,
    api_secret=settings.API_SECRET,
    secure=True
)

# Allowed file types
ALLOWED_TYPES = ["image/jpeg", "image/png", "image/webp"]

# ROUTER
router = APIRouter(
    prefix="/images",
    tags=["Images"]
)


# UPLOAD IMAGE TO CLOUDINARY

def upload_to_cloudinary(file: UploadFile, folder: str = "reztro"):
    try:
        if file.content_type not in ALLOWED_TYPES:
            raise HTTPException(
                status_code=400,
                detail="Invalid file type. Only JPEG, PNG, WEBP allowed."
            )

        result = cloudinary.uploader.upload(file.file, folder=folder)

        return {
            "url": result.get("secure_url"),
            "public_id": result.get("public_id")
        }

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Upload failed: {str(e)}")


# DELETE IMAGE FROM CLOUDINARY

def delete_from_cloudinary(public_id: str):
    try:
        result = cloudinary.uploader.destroy(public_id)

        return {
            "result": result
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Delete failed: {str(e)}")


# FASTAPI ROUTES

@router.post("/upload")
async def upload_image(file: UploadFile = File(...)):
    result = upload_to_cloudinary(file)

    return {
        "message": "Image uploaded successfully",
        "data": result
    }


@router.delete("/delete/{public_id}")
async def delete_image(public_id: str):
    result = delete_from_cloudinary(public_id)

    return {
        "message": "Image deleted successfully",
        "data": result
    }