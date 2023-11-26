import { useState } from "react";
import { PersonIcon } from "../../components/Icons";
import { Author } from "../models";
import Tab from "./Tab";
import Select from "./Select";
import useSuggestions from "./useSuggestions";

enum TabOptions {
  smartSort = "Smart sort",
  scopus = "Scopus",
  dblp = "DBLP",
  googleScolar = "Google Scholar",
}

function AuthorRow(props: Author) {
  const { name, affiliation, email, src, id, year, venue } = props;
  return (
    <>
      <div
        className="flex space-x-24 items-center px-24 h-min border-b border-stone-300 py-4"
        key={id}
      >
        <PersonIcon />
        <div className="m-6">
          <div className="text-2xl text-stone-800">{name}</div>
          <div className="text-sm text-stone-900 font-light">{email}</div>
          <div className="text-sm text-stone-900 font-light">{affiliation}</div>
          <div className="text-stone-700 font-extralight text-sm">{`${src} ${year} ${
            venue === null ? "" : venue
          }`}</div>
        </div>
      </div>
    </>
  );
}

export default function ReviewersSuggestions() {
  const getFileName = () => "some.pdf";
  const [selectedTab, setSelectedTab] = useState<TabOptions>(
    TabOptions.smartSort,
  );
  const [venue, setVenue] = useState<string | undefined>();
  const { authors, venueOptions } = useSuggestions();

  return (
    <div>
      <div className="pb-4 text-stone-900 font-light">
        {`Suggested reviewers for ${getFileName()}`}
      </div>

      <div className="flex justify-between border-b border-stone-300">
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

      <div
        className={`w-1/4 py-4 ${
          selectedTab === TabOptions.scopus ? "hidden" : ""
        }`}
      >
        <Select
          options={venueOptions}
          label="Select venue"
          onChange={setVenue}
        />
      </div>

      {authors.filter(filterAuthors(selectedTab, venue)).map((author) => (
        <AuthorRow key={author.id} {...author} />
      ))}
    </div>
  );
}

function filterAuthors(selectedOption: TabOptions, venue: string | undefined) {
  const filter = (author: Author) => {
    const isScopusTabSelected = TabOptions.scopus == selectedOption;
    const isVenueUnselected = venue === undefined;
    const venueMatches =
      isVenueUnselected || isScopusTabSelected ? true : author.venue === venue;

    if (selectedOption == TabOptions.smartSort) return true && venueMatches;
    return (author.src as TabOptions) === selectedOption && venueMatches;
  };
  return filter;
}
