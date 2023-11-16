from fastapi import APIRouter, Depends, HTTPException, UploadFile
from src.auth import is_authorized
from typing_extensions import BinaryIO

router = APIRouter()


@router.get("/", dependencies=[Depends(is_authorized)])
async def root() -> dict:
    return {"greeting": "hello"}


@router.post("/upload/file/", status_code=200)
async def upload_pdf(file: UploadFile) -> dict:
    if file.content_type != "application/pdf":
        raise HTTPException(400, detail="Invalid document type.")
    try:
        file_content: BinaryIO = file.file
    except Exception:
        raise HTTPException(500, detail="Internal server error.")
    return {"message": "successful upload", "filename": file.filename}


@router.get("/upload/results/", status_code=200, dependencies=[Depends(is_authorized)])
async def retrieve_results() -> dict:
    result = [
        {
            "name": "Wolfram Fenske",
            "src": "DBLP",
            "date": 2015,
            "title": "When code smells twice as much: Metric-based detection of variability-aware code smells.",
            "affiliation": "Otto von Guericke University of Magdeburg, Germany",
        },
        {
            "name": "Yang Zhang",
            "src": "Scopus",
            "date": 2023,
            "title": "MIRROR: multi-objective refactoring recommendation via correlation analysis",
            "affiliation": "Hebei University of Science and Technology",
        },
        {
            "name": "Francesca Arcelli Fontana",
            "src": "Google Scholar",
            "date": 2012,
            "title": "Evaluating the lifespan of code smells using software repository mining",
            "affiliation": "Università degli Studi di Milano-Bicocca",
        },
    ]
    return result
