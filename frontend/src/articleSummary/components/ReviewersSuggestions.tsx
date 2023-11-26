import { useEffect, useState } from "react";
import { getDetails } from "../api";
import { Author, DetailsResponseModel } from "../models";
import Tab from "./Tab";
import Select from "./Select";
import useSuggestions from "./useSuggestions";
import { CursorStyle } from "../../models/styling";
import Modal from "./Modal";
import { useParams } from "react-router-dom";

enum TabOptions {
  smartSort = "Smart sort",
  scopus = "Scopus",
  dblp = "DBLP",
  googleScolar = "Google Scholar",
}

type DetailProps = {
  text: string;
  label: string;
};

function Detail(props: DetailProps) {
  return (
    <div className="mb-4">
      <div className="text-xs font-thin -mb-1"> {props.label} </div>
      <div className="text-base text-stone-900 font-light"> {props.text} </div>
    </div>
  );
}

function AuthorDetails(props: Author & { isModalOpen: boolean }) {
  const { name, affiliation, src, id, year, venue } = props;
  const [details, setDetails] = useState<DetailsResponseModel | undefined>(
    undefined,
  );
  const { uploadId } = useParams();

  useEffect(() => {
    if (props.isModalOpen && uploadId && details === undefined)
      getDetails(uploadId, src, id).then(setDetails);
  }, [props.isModalOpen]);

  return (
    <>
      <div className="mb-8">
        <div className="text-3xl text-stone-800">{name}</div>
        <div className="text-base text-stone-900 font-light">{affiliation}</div>
      </div>
      <Detail label="Source" text={src} />
      <Detail label="Year of article publication" text={year} />
      {venue !== null && <Detail label="Venue" text={venue} />}
      {details?.affiliation !== undefined && (
        <Detail label="Affiliation" text={details.affiliation} />
      )}
    </>
  );
}

function AuthorRow(props: Author) {
  const { name, affiliation, src, id, year, venue } = props;
  const [isModalOpen, setModalOpen] = useState<boolean>(false);

  return (
    <>
      <div
        className={`flex items-center h-min border-b border-stone-300 py-4 hover:bg-stone-100 ${CursorStyle.ready}`}
        key={id}
        onClick={() => setModalOpen(true)}
      >
        <div className="my-6">
          <div className="text-2xl text-stone-800">{name}</div>
          <div className="text-sm text-stone-900 font-light">{affiliation}</div>
          <div className="text-stone-700 font-extralight text-sm">{`${src} ${year} ${
            venue === null ? "" : venue
          }`}</div>
        </div>
      </div>
      <Modal setOpen={setModalOpen} isOpen={isModalOpen}>
        <AuthorDetails {...props} isModalOpen={isModalOpen} />
      </Modal>
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
