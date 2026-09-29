from fastapi import FastAPI

app = FastAPI(
    title="Pincode search API",
    description="Auto fill city and state from Indian Pincode during checkout"
)

@app.get("/")
def root():
    return {"message": "Welcome to Pincode Search API"}