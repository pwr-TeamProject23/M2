import os
from pathlib import Path


base_path = Path(__file__).parent
article_path = (base_path / "article_parser_tests/articles").resolve()
a =os.path.join(article_path, "Article_test_data.json")
x =2