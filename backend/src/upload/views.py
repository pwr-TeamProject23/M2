from fastapi import APIRouter, Depends, HTTPException, UploadFile
from src.articles_service.articles_parser import ArticleParser, KeywordParsingError
from src.api_parsers.dblp_parser import DBLPParser
from src.api_parsers.scopus_parser import ScopusParser
from src.api_parsers.exceptions import NoAuthorsException
from typing_extensions import BinaryIO
from src.auth import is_authorized

router = APIRouter()


@router.get("/")  # , dependencies=[Depends(is_authorized)])
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
async def retrieve_results() -> list[dict[str, str|int]]:
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


@router.post("/get_authors/", status_code=200, dependencies=[Depends(is_authorized)])
async def get_authors(file: UploadFile):
    if file.content_type != "application/pdf":
        raise HTTPException(400, detail="Invalid document type.")
    try:
        authors = []
        file_content: BinaryIO = file.file
        article_parser = ArticleParser(file_content)
        keywords = article_parser.get_keywords()
        for keyword in keywords[0]:
            parser = ScopusParser(keywords=keyword.replace('\n', ' '))
            try:
                scopus_authors = parser.get_authors()
            except NoAuthorsException:
                continue
            authors.extend(scopus_authors)
        for keyword in keywords[1]:
            parser = DBLPParser(keywords=keyword.replace('\n', ' '))
            try:
                dblp_authors = parser.get_authors()
            except NoAuthorsException:
                continue
            authors.extend(dblp_authors)
        file_content.close()
        authors_dicts = [author.get_attrs() for author in authors]
    except KeywordParsingError:
        raise HTTPException(500, detail="An error occurred whilst parsing the article.")
    except Exception:
        raise HTTPException(500, detail="Internal server error.")
    return authors_dicts
