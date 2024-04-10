from fastapi import FastAPI, UploadFile
from PIL import Image
from pydantic import BaseModel

from ml_module import Predictor

app = FastAPI()

predictor = Predictor(
    fixes_path="/home/khroma-son/data/fixes.json",
    latents_path="/home/khroma-son/data/latents2.pt",
    df_e="/home/khroma-son/data/e_places.csv",
    df_n="/home/khroma-son/data/n_places.csv",
    df_v="/home/khroma-son/data/v_places.csv",
    df_y="/home/khroma-son/data/y_places.csv",
    device="cpu",
)


class TextReqest(BaseModel):
    text: str
    city: str  # e - ekb, n - nihniy, y - yaroslaval, v - vladimir


@app.post("/text")
async def text_predict(body: TextReqest) -> list:
    ml_res = predictor.get_cors_text(text=body.text, topk=5, city=body.city)
    texts = ml_res[0]
    probs = ml_res[1]
    coords = ml_res[2]
    # ml_res is a tuple of 3 lists: names probs, and list of coordinates
    # return dict of city: {name: name, probs: probs, coords: coords}
    for i in range(len(probs)):
        probs[i] = float(probs[i])
    for i in range(len(coords)):
        coords[i] = [float(coord) for coord in coords[i]]

    result = [{"name": texts[i], "probs": probs[i], "coord": coords[i]} for i in range(len(texts))]
    return result


@app.post("/image")
async def image_predict(file: UploadFile, city: str) -> list:
    pil_image = Image.open(file.file)
    ml_res = predictor.get_cors_image(image=pil_image, topk=5, city=city)
    texts = ml_res[0]
    probs = ml_res[1]
    coords = ml_res[2]
    for i in range(len(probs)):
        probs[i] = float(probs[i])
    for i in range(len(coords)):
        coords[i] = [float(coord) for coord in coords[i]]
    # ml_res is a tuple of 3 lists: names probs, and list of coordinates
    # return dict of city: {name: name, probs: probs, coords: coords}
    result = [{"name": texts[i], "probs": probs[i], "coords": coords[i]} for i in range(len(texts))]
    return result


# start fastapi
if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8050)
