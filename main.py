from fastapi import FastAPI, UploadFile, File, Header, HTTPException

app = FastAPI()

API_KEY = "MY_SECRET_123"

@app.post("/analyze")
async def analyze(file: UploadFile = File(...), authorization: str = Header(None)):
    
    if authorization != f"Bearer {API_KEY}":
        raise HTTPException(status_code=401, detail="Invalid token")

    content = await file.read()
    text = content.decode(errors="ignore")

    summary = text[:100]

    entities = []
    for word in text.split():
        if word.istitle():
            entities.append(word)

    sentiment = "neutral"

    return {
        "summary": summary,
        "entities": entities,
        "sentiment": sentiment
    }