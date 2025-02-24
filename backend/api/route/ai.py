from fastapi import APIRouter
from api.service import insta
import base64


router = APIRouter()


prefix = "/ai"

@router.get("/insta-post")
def get_insta_details(username: str):
    caption, image = insta.get_latest_post(username=username)
    # base64 encode the binary image 
    image = base64.b64encode(image).decode("utf-8")
    return {
        "caption": caption,
        "image": image
    }
    
def setup(app):
    print("Loading")
    app.include_router(router, prefix=prefix)