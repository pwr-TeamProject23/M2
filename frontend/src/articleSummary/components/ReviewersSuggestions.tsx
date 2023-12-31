import React, { ChangeEvent, useEffect, useState } from "react";
import { getDetails, search, getKeywords } from "../api";
import { Author, DetailsResponseModel } from "../models";
import Tab from "./Tab";
import Select from "./Select";
import useSuggestions from "./useSuggestions";
import { CursorStyle } from "../../models/styling";
import Modal from "./Modal";
import { Link, useParams } from "react-router-dom";
import CircularProgressBar from "./CircularProgressBar";
import { getSearchStatus } from "../../fileUpload/components/api";
import { SearchStatus } from "../../fileUpload/components/models";

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

function ExternalProfileLink(props: ExternalLinkProps) {
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

  return (
    <Link to={getLink()} target="_blank" rel="noopener noreferrer">
      {linkToProfile}
    </Link>
  );
}

type ContainerProps = { children: React.ReactNode };

function DetailText(props: ContainerProps) {
  return (
    <div className="text-base text-stone-900 font-light">{props.children}</div>
  );
}

function DetailContainer(props: ContainerProps) {
  return <div className="mb-2">{props.children}</div>;
}

function DetailLabelContainer(props: ContainerProps) {
  return <div className="text-xs font-thin -mb-1"> {props.children} </div>;
}

function Detail(props: DetailProps) {
  return (
    <DetailContainer>
      <DetailLabelContainer> {props.label} </DetailLabelContainer>
      {props.text && <DetailText> {props.text} </DetailText>}
      {props.list &&
        props.list.map((elem, i) => <DetailText key={i}> {elem} </DetailText>)}
    </DetailContainer>
  );
}

function DoiLink(props: { doi: string }) {
  const { doi } = props;
  return (
    <div className="underline text-base text-stone-900 font-light">
    <Link
      to={`https://doi.org/${doi}`}
      target="_blank"
      rel="noopener noreferrer"
    >
      {doi}
    </Link>
  </div>
  )
}

function DoiDetail(props: { doi: string }) {
  return (
    <DetailContainer>
      <DetailLabelContainer> DOI </DetailLabelContainer>
      <DoiLink {...props}/>
    </DetailContainer>
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

  useEffect(() => {
    if (props.isModalOpen && details === undefined)
      getDetails(source, id).then(setDetails);
  }, [props.isModalOpen]);

  return (
    <>
      <div className="text-5xl text-stone-800 mb-2">{`${firstName} ${lastName}`}</div>

      <div className="underline font-thin text-stone-900 -mt-2 mb-2">
        <ExternalProfileLink id={authorExternalId} source={source} />
      </div>

      <Detail label="Source" text={source} />

      {details?.affiliation !== undefined && details?.affiliation !== null && (
        <Detail label="Affiliation" text={details.affiliation} />
      )}

      <div className="text-2xl text-stone-800 mt-4 pt-4 mb-2 border-t border-stone-300">
        {title}
      </div>

      <Detail label="Article publication" text={year} />
      {venues !== null && venues !== undefined && (
        <Detail label="Venues" list={venues} />
      )}
      {doi !== null && <DoiDetail doi={doi} />}
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
          <div className="text-md text-stone-800">{`${firstName} ${lastName}`}</div>
          <div className="text-2xl text-stone-800">{publication.title}</div>
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

function UserInfo(props: { text: string }) {
  return (
    <div className="w-100 flex justify-center text-3xl p-24 text-stone-500 font-light">
      {props.text}
    </div>
  );
}

function SuggestedReviewersBanner(props: { filename?: string }) {
  if (props.filename === undefined) {
    return null;
  }
  return (
    <div className="pb-4 text-stone-900 font-light">
      {`Suggested reviewers for ${props.filename}`}
    </div>
  );
}

type KeywordsFormProps = {
  status?: SearchStatus;
  setStatus: (s: SearchStatus) => void;
  isLoading: boolean;
};

function KeywordsForm(props: KeywordsFormProps) {
  const { status, setStatus, isLoading } = props;
  const [keywords, setKeywords] = useState<string>("");
  const { searchId } = useParams();
  const isStatusPending = status === SearchStatus.pending;
  const isDisabled = isLoading || isStatusPending;
  const emptyKeywords = keywords.length === 0;

  useEffect(() => {
    if (searchId !== undefined) {
      getSearchStatus(parseInt(searchId)).then(setStatus);
    }
  }, []);

  useEffect(() => {
    if (searchId !== undefined) {
      getKeywords(searchId).then((r) => setKeywords(r.join(",")));
    }
  }, [status]);

  const handleSubmit = () => {
    if (searchId !== undefined && keywords !== "") {
      search(
        searchId,
        keywords
          .replace(/,\s*$/, "")
          .split(",")
          .map((item) => item.trim()),
      ).then(() => setStatus(SearchStatus.pending));
    }
  };
  const isButtonDisabled = isDisabled || emptyKeywords;
  const onHover = isButtonDisabled ? "" : "hover:bg-stone-400";
  const buttonBg = isButtonDisabled ? "bg-stone-100" : "bg-teal-950";
  const disabledLabel = isDisabled ? "text-stone-300" : "";
  const inputBg = isDisabled ? "bg-stone-100" : "";
  const inputBorder = isDisabled ? "border-none" : "";
  const disabledButtonText = isDisabled ? "text-stone-400" : "text-white";
  const disabledInputText = isDisabled ? "text-stone-400" : "";

  const handleChange = (e: ChangeEvent<HTMLInputElement>) =>
    setKeywords(e.target.value);
  return (
    <>
      <div className={`pr-4 ${disabledLabel}`}>Keywords, comma separated</div>
      <div className="w-full flex">
        <input
          className={`${inputBg} ${inputBorder} ${disabledInputText} lg:w-11/12 w-9/12`}
          type="text"
          value={keywords}
          onChange={handleChange}
          disabled={isDisabled}
        />
        <button
          className={`ml-4 ${buttonBg} ${onHover} ${disabledButtonText} h-12 lg:w-1/12 w-3/12`}
          onClick={handleSubmit}
          disabled={isButtonDisabled}
        >
          Search
        </button>
      </div>
    </>
  );
}

type ResultsProps = {
  isLoading: boolean;
  filteredAuthors: Author[];
};

function Results(props: ResultsProps) {
  const { isLoading, filteredAuthors } = props;
  const isFilteredEmpty = filteredAuthors.length == 0;
  if (isLoading) return <UserInfo text="Results are loading, please wait" />;

  if (isFilteredEmpty) return <UserInfo text="No results found" />;

  return (
    <>
      {filteredAuthors.map((author) => (
        <AuthorRow key={author.id} {...author} />
      ))}
    </>
  );
}

export default function ReviewersSuggestions() {
  const [selectedTab, setSelectedTab] = useState<TabOptions>(
    TabOptions.smartSort,
  );
  const [venue, setVenue] = useState<string | undefined>();
  const [status, setStatus] = useState<SearchStatus>();
  const { authors, venueOptions, filename, isLoading } = useSuggestions(status);
  const filteredAuthors = authors.filter(filterAuthors(selectedTab, venue));
  const { searchId } = useParams();

  useEffect(() => {
    if (status === SearchStatus.pending && searchId !== undefined) {
      const fetchData = () => {
        getSearchStatus(parseInt(searchId))
          .then((newStatus: SearchStatus) => {
            if (newStatus !== SearchStatus.pending) {
              clearInterval(intervalId);
              setStatus(newStatus as SearchStatus);
            }
          })
          .catch(() => clearInterval(intervalId));
      };
      const interval = 2500;
      const intervalId = setInterval(() => fetchData(), interval);
    }
  }, [status]);

  if (status == SearchStatus.pending) {
    return (
      <div>
        <SuggestedReviewersBanner filename={filename} />
        <KeywordsForm {...{ isLoading, setStatus, status }} />
        <UserInfo text="Search in progress. Please wait a moment for your results. Thank you!" />
      </div>
    );
  }

  if (status == SearchStatus.error) {
    return (
      <div>
        <SuggestedReviewersBanner filename={filename} />
        <UserInfo text="We are sorry, this search failed, please try uploading another file" />
      </div>
    );
  }

  return (
    <div>
      <SuggestedReviewersBanner filename={filename} />
      <KeywordsForm {...{ isLoading, setStatus, status }} />
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
      <Results {...{ isLoading, filteredAuthors }} />
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
