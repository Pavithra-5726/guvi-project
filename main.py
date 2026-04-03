from fastapi import FastAPI, UploadFile, File, Header, HTTPException

app = FastAPI()

API_KEY = "MY_SECRET_123"

@app.post("/analyze")
async def analyze(file: UploadFile = File(...), authorization: str = Header(None)):
    
    if not authorization:
        raise HTTPException(status_code=401, detail="Missing token")

    if "Bearer" not in authorization:
        raise HTTPException(status_code=401, detail="Invalid token format")

    token = authorization.split(" ")[1]

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