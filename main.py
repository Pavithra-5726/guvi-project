from fastapi import FastAPI, UploadFile, File, Request, HTTPException

app = FastAPI()

API_KEY = "MY_SECRET_123"

@app.post("/analyze")
async def analyze(request: Request, file: UploadFile = File(...)):
    
    auth = request.headers.get("authorization")

    if not auth:
        raise HTTPException(status_code=401, detail="Missing token")

    if "Bearer" not in auth:
        raise HTTPException(status_code=401, detail="Invalid token format")

    token = auth.split(" ")[1]

    if token != API_KEY:
        raise HTTPException(status_code=401, detail="Invalid token")

    content = await file.read()
    text = content.decode(errors="ignore")

    summary = text[:100]
    entities = [word for word in text.split() if word.istitle()]
    sentiment = "neutral"

    return {
        "summary": summary,
        "entities": entities,
        "sentiment": sentiment
    }