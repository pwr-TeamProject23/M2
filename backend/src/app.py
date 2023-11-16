from fastapi import FastAPI, UploadFile, HTTPException
from typing_extensions import BinaryIO

app = FastAPI(title="ZRECENZOWANE")


@app.get("/")
async def root():
    return {"greeting": "hello"}


@app.post("/upload/file/", status_code=200)
async def upload_pdf(file: UploadFile):
    if file.content_type != "application/pdf":
        raise HTTPException(400, detail="Invalid document type.")
    try:
        file_content: BinaryIO = file.file
    except Exception:
        raise HTTPException(500, detail="Internal server error.")
    return {"message": "successful upload", "filename": file.filename}


@app.get("/upload/results/", status_code=200)
async def retrieve_results():
    result = [
        {
            'name': 'Wolfram Fenske',
            'src': 'DBLP',
            'date': 2015,
            'title': 'When code smells twice as much: Metric-based detection of variability-aware code smells.',
            'affiliation': 'Otto von Guericke University of Magdeburg, Germany',
        },
        {
            'name': 'Yang Zhang',
            'src': 'Scopus',
            'date': 2023,
            'title': 'MIRROR: multi-objective refactoring recommendation via correlation analysis',
            'affiliation': 'Hebei University of Science and Technology',
        },
        {
            'name': 'Francesca Arcelli Fontana',
            'src': 'Google Scholar',
            'date': 2012,
            'title': 'Evaluating the lifespan of code smells using software repository mining',
            'affiliation': 'Università degli Studi di Milano-Bicocca',
        },
    ]
    return result


@app.get("/user_history/")
async def user_history():
    pass

