import { PersonIcon } from "../../components/Icons";

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
        <div className="text-stone-600 font-thin text-sm">{`\u2022 ${source}`}</div>
      ))}
    </div>
  );
}

function Author(props: Author) {
  const { name, surname, affiliation, email, sources } = props;
  return (
    <>
      <div className="flex space-x-24 items-center px-24 h-min border-t border-stone-300 py-4">
        <PersonIcon />
        <div className="m-6">
          <div className="text-3xl text-stone-800">{`${name} ${surname}`}</div>
          <div className="text-sm text-stone-800 font-thin">{email}</div>
          <div className="text-sm text-stone-800 font-thin">{affiliation}</div>
        </div>

        <Sources sources={sources} />
      </div>
    </>
  );
}

export default function ReviewersSuggestions() {
  const getFileName = () => "some.pdf";

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
    <div className="">
      <div className="pb-4 text-stone-900 font-light">
        {`Suggested reviewers for ${getFileName()}`}
      </div>
      {authors.map((author) => (
        <Author {...author} />
      ))}
    </div>
  );
}
