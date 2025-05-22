from fastapi import FastAPI


app = FastAPI(
    title="NewsFudge",
    version="0.1.0",
    description="Fast API AI APP"
)

@app.get("/")
def root():
    return {"message":"Welcome to News Fudge"}

