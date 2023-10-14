from backend.src.services.dblp import Dblp


def main():
    dblp = Dblp()
    print(dblp.get_authors(query="Lech Madeyski"))


if __name__ == "__main__":
    main()
