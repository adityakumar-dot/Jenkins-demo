from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def home():
    return {"message": "Hello from FastAPI CI/CD Hii i just changes again3🚀"}

@app.get("/health")
def health():
    return {"status": "ok"}