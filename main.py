from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def home():
    return {"message": "Hello from FastAPI CI/CD Nothing Chnage"}

@app.get("/health")
def health():
    return {"status": "ok"}