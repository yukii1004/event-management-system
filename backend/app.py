import importlib
import importlib.util
import json

from fastapi import FastAPI

from api.service import db
import razorpay

app = FastAPI()

app.database = db.Database("database.db")
app.razorpay_client = razorpay.Client(auth=("key_id", "key_secret"))


@app.get("/")
async def index():
    response = {"response": "Hello world"}
    return response


with open("api/route/routes.json") as f:
    routes = json.load(f)

for route in routes:
    importlib.util.spec_from_file_location(route, f"api/route/{route}.py")
    module = importlib.import_module(f"api.route.{route}")
    module.setup(app)

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
