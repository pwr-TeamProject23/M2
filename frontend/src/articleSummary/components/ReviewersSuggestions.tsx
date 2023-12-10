import { useEffect, useState } from "react";
import { getDetails } from "../api";
import { Author, DetailsResponseModel } from "../models";
import Tab from "./Tab";
import Select from "./Select";
import useSuggestions from "./useSuggestions";
import { CursorStyle } from "../../models/styling";
import Modal from "./Modal";
import { Link, useParams } from "react-router-dom";
import CircularProgressBar from "./CircularProgressBar";

enum TabOptions {
  smartSort = "Smart sort",
  scopus = "Scopus",
  dblp = "DBLP",
  googleScholar = "Google Scholar",
}

type DetailProps = {
  text?: string | number;
  list?: string[];
  label: string;
};

type Source = Omit<TabOptions, "smartSort">;

type ExternalLinkProps = {
  id: string;
  source: Source;
};

function ExternalLink(props: ExternalLinkProps) {
  const { id, source } = props;
  const linkToProfile = "Link to profle";

  const getLink = () => {
    if (source == TabOptions.googleScholar) {
      return `https://scholar.google.com/citations?hl=pl&user=${id}`;
    }

    if (source == TabOptions.scopus) {
      return `https://www.scopus.com/authid/detail.uri?authorId=${id}`;
    }

    return `https://dblp.org/pid/${id}.html`;
  };

  return <Link to={getLink()} target="_blank" rel="noopener noreferrer">{linkToProfile}</Link>;
}

function DetailText(props: { children: React.ReactNode }) {
  return (
    <div className="text-base text-stone-900 font-light">{props.children}</div>
  );
}

function Detail(props: DetailProps) {
  return (
    <div className="mb-2">
      <div className="text-xs font-thin -mb-1"> {props.label} </div>
      {props.text && <DetailText> {props.text} </DetailText>}
      {props.list &&
        props.list.map((elem, i) => <DetailText key={i}> {elem} </DetailText>)}
    </div>
  );
}

function AuthorDetails(props: Author & { isModalOpen: boolean }) {
  const { id, authorExternalId, firstName, lastName, source, publication } =
    props;
  const { doi, title, year, venues, citationCount, similarityScore } =
    publication;
  const [details, setDetails] = useState<DetailsResponseModel | undefined>(
    undefined,
  );
  const { searchId } = useParams();

  useEffect(() => {
    if (props.isModalOpen && searchId && details === undefined)
      getDetails(searchId, source, id).then(setDetails);
  }, [props.isModalOpen]);

  return (
    <>
      <div className="text-5xl text-stone-800 mb-2">{`${firstName} ${lastName}`}</div>

      <div className="underline font-thin text-stone-900 -mt-2 mb-2">
        <ExternalLink id={authorExternalId} source={source} />
      </div>

      <Detail label="Source" text={source} />

      {(details?.affiliation !== undefined && details?.affiliation !== null) && (
        <Detail label="Affiliation" text={details.affiliation} />
      )}

      <div className="text-2xl text-stone-800 mt-4 pt-4 mb-2 border-t border-stone-300">
        {title}
      </div>

      <Detail label="Article publication" text={year} />
      {venues !== null && venues !== undefined && (
        <Detail label="Venues" list={venues} />
      )}
      {doi && <Detail label="DOI" text={doi} />}
      {citationCount !== null && (
        <Detail label="Citations count" text={citationCount.toString()} />
      )}
      {similarityScore && (
        <Detail label="Accuracy score" text={similarityScore.toFixed(2)} />
      )}
      <Detail label="External id" text={authorExternalId} />
    </>
  );
}

function AuthorRow(props: Author) {
  const { id, firstName, lastName, source, publication } = props;
  const { year, similarityScore } = publication;
  const [isModalOpen, setModalOpen] = useState<boolean>(false);

  return (
    <>
      <div
        className={`py-6 flex justify-between items-center h-min border-b border-stone-300 py-4 hover:bg-stone-100 ${CursorStyle.ready}`}
        key={id}
        onClick={() => setModalOpen(true)}
      >
        <div>
          <div className="text-2xl text-stone-800">{`${firstName} ${lastName}`}</div>
          <div className="text-stone-700 font-extralight text-sm">{`${source} ${year}`}</div>
        </div>
        {similarityScore !== null && (
          <CircularProgressBar progress={similarityScore} />
        )}
      </div>

      <Modal setOpen={setModalOpen} isOpen={isModalOpen}>
        <AuthorDetails {...props} isModalOpen={isModalOpen} />
      </Modal>
    </>
  );
}

export default function ReviewersSuggestions() {
  const [selectedTab, setSelectedTab] = useState<TabOptions>(
    TabOptions.smartSort,
  );
  const [venue, setVenue] = useState<string | undefined>();
  const { authors, venueOptions, filename } = useSuggestions();

  return (
    <div>
      <div className="pb-4 text-stone-900 font-light">
        {`Suggested reviewers for ${filename}`}
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
      isVenueUnselected || isScopusTabSelected
        ? true
        : author.publication.venues?.includes(venue);

    if (selectedOption == TabOptions.smartSort) return true && venueMatches;
    return (author.source as TabOptions) === selectedOption && venueMatches;
  };
  return filter;
}
