import { useEffect, useState } from "react";
import { PersonIcon } from "../../components/Icons";
import { getSuggestions } from "../api";
import { Author } from "../models";
import { useAuthStore } from "../../store/AuthStore";
import { useParams } from "react-router-dom";

enum TabOptions {
  smartSort = "Smart sort",
  scopus = "Scopus",
  dblp = "DBLP",
  googleScolar = "Google Scholar",
}

function AuthorRow(props: Author) {
  const { name, affiliation, email, src, id, year } = props;
  return (
    <>
      <div
        className="flex space-x-24 items-center px-24 h-min border-t border-stone-300 py-4"
        key={id}
      >
        <PersonIcon />
        <div className="m-6">
          <div className="text-2xl text-stone-800">{name}</div>
          <div className="text-sm text-stone-900 font-light">{email}</div>
          <div className="text-sm text-stone-900 font-light">{affiliation}</div>
          <div className="text-stone-700 font-extralight text-sm">{`${src} ${year}`}</div>
        </div>
      </div>
    </>
  );
}

interface TabProps {
  displayName: string;
  setSelectedTab: (option: TabOptions) => void;
  isSelected: boolean;
}

function Tab(props: TabProps) {
  const { displayName, isSelected, setSelectedTab } = props;
  const onSelected = () => setSelectedTab(displayName as TabOptions);
  const underLine = isSelected ? "border-b-2 border-teal-950" : "";
  const onHover = isSelected ? "" : "hover:border-b-2 hover:border-stone-300";
  const style = `w-full p-2 flex items-center justify-center ${onHover} ${underLine}`;

  return (
    <div className={style} onClick={onSelected}>
      <button>{displayName}</button>
    </div>
  );
}

export default function ReviewersSuggestions() {
  const getFileName = () => "some.pdf";
  const [authors, setAuthors] = useState<Author[]>([]);
  const user = useAuthStore((state) => state.user);
  const [selectedTab, setSelectedTab] = useState<TabOptions>(
    TabOptions.smartSort,
  );
  const { uploadId } = useParams();

  useEffect(() => {
    if (user != null && uploadId) {
      getSuggestions(uploadId).then(setAuthors);
    }
  }, []);

  return (
    <div>
      <div className="pb-4 text-stone-900 font-light">
        {`Suggested reviewers for ${getFileName()}`}
      </div>
      <div className="flex justify-between">
        {Object.values(TabOptions).map((value) => {
          return (
            <Tab
              key={value}
              displayName={value}
              setSelectedTab={setSelectedTab}
              isSelected={(value as TabOptions) == selectedTab}
            />
          );
        })}
      </div>
      {authors.filter(filterAuthors(selectedTab)).map((author) => (
        <AuthorRow key={author.id} {...author} />
      ))}
    </div>
  );
}

function filterAuthors(selectedOption: TabOptions) {
  const filter = (author: Author) => {
    if (selectedOption == TabOptions.smartSort) return true;
    return (author.src as TabOptions) === selectedOption;
  };
  return filter;
}
