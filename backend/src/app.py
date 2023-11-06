from fastapi import FastAPI, UploadFile, HTTPException

app = FastAPI(title="ZRECENZOWANE")


@app.get("/")
async def root():
    return {"greeting": "hello"}


@app.post("/upload/file/", status_code=200)
async def upload_pdf(file: UploadFile):
    if file.content_type != "application/pdf":
        raise HTTPException(400, detail="Invalid document type.")
    try:
        file_content = file.file    # file object same as returned by open()
    except Exception:
        raise HTTPException(500, detail="Internal server error.")
    return {"message": "successful upload", "filename": file.filename}


@app.get("/upload/results/", status_code=200)
async def retrieve_results():
    pass


@app.get("/user_history/")
async def user_history():
    pass

