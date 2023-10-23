import { PersonIcon } from "./Icons";

interface Author {
  name: string;
  surname: string;
  affiliation: string;
  email: string;
  sources: string[];
}

function Sources(props: Pick<Author, "sources">) {
  const { sources } = props;
  return (
    <div className="p-4">
      {sources.map((source) => (
        <div className="text-white font-thin text-sm">{`\u2022 ${source}`}</div>
      ))}
    </div>
  );
}

function Author(props: Author) {
  const { name, surname, affiliation, email, sources } = props;
  return (
    <>
      <div className="flex space-x-28 items-center px-24 h-min border-b border-accent p-4">
        <PersonIcon />
        <div className="m-6">
          <div className="text-3xl text-white">{`${name} ${surname}`}</div>
          <div className="text-sm text-white font-thin">{email}</div>
          <div className="text-sm text-white font-thin">{affiliation}</div>
        </div>

        <Sources sources={sources} />
      </div>
    </>
  );
}

export default function AuthorsListing() {
  const authors = [
    {
      name: "Lech",
      surname: "Madeyski",
      affiliation: "Politechnika Wrocławska",
      email: "lech@pwr.com",
      sources: ["GoogleScholar", "DBLP", "Scopus"],
    },
    {
      name: "Lech",
      surname: "Madeyski",
      affiliation: "Politechnika Wrocławska",
      email: "lech@pwr.com",
      sources: ["GoogleScholar", "DBLP", "Scopus"],
    },
    {
      name: "Lech",
      surname: "Madeyski",
      affiliation: "Politechnika Wrocławska",
      email: "lech@pwr.com",
      sources: ["GoogleScholar", "DBLP", "Scopus"],
    },
    {
      name: "Lech",
      surname: "Madeyski",
      affiliation: "Politechnika Wrocławska",
      email: "lech@pwr.com",
      sources: ["GoogleScholar", "DBLP", "Scopus"],
    },
    {
      name: "Lech",
      surname: "Madeyski",
      affiliation: "Politechnika Wrocławska",
      email: "lech@pwr.com",
      sources: ["GoogleScholar", "DBLP", "Scopus"],
    },
    {
      name: "Lech",
      surname: "Madeyski",
      affiliation: "Politechnika Wrocławska",
      email: "lech@pwr.com",
      sources: ["GoogleScholar", "DBLP", "Scopus"],
    },
  ];

  return (
    <div className="bg-light-grey m-8">
      <div className="text-white text-2xl font-extralight pb-4 bg-background">
        Suggested reviewers for "pdf name"
      </div>
      {authors.map((author) => (
        <Author {...author} />
      ))}
    </div>
  );
}
