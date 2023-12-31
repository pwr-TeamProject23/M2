import { useEffect, useState } from "react";
import { CheckmarkIcon, ErrorIcon, PendingIcon } from "../../components/Icons";
import { Search, SearchStatus } from "./models";
import { deleteSearch, getHistory, getSearchStatus } from "./api";
import { useAuthStore } from "../../store/AuthStore";
import { CursorStyle } from "../../models/styling";
import { useHistoryStore } from "../HistoryStore";

function StatusIcon(props: Pick<Search, "status">) {
  const status = props.status;

  if (status == SearchStatus.error) return <ErrorIcon />;
  if (status == SearchStatus.pending) return <PendingIcon />;
  if (status == SearchStatus.ready) return <CheckmarkIcon />;
}

const getCursor = (status: string) => {
  if (status == SearchStatus.error) return CursorStyle.error;
  if (status == SearchStatus.ready) return CursorStyle.ready;
  if (status == SearchStatus.pending) return CursorStyle.pending;
  return CursorStyle.default;
};

type SearchRowProps = {
  id: number;
  callback: () => any;
} & Pick<Search, "status" | "filename">;

function SearchRow(props: SearchRowProps) {
  const { callback, id, status, filename } = props;

  const onDelete = () => deleteSearch(id).then(callback);

  useEffect(() => {
    if (status === SearchStatus.pending) {
      const fetchData = () => {
        getSearchStatus(id)
          .then((newStatus: SearchStatus) => {
            if (newStatus !== SearchStatus.pending) {
              callback();
              clearInterval(intervalId);
            }
          })
          .catch(() => clearInterval(intervalId));
      };
      const interval = 2500;
      const intervalId = setInterval(() => fetchData(), interval);
    }
  }, [status]);

  return (
    <div className="flex items-center justify-between h-full w-full">
      <div className="w-full">
        <ArticleRedirect {...props} filename={filename} />
      </div>
      <div className="flex">
        <button className="font-light" onClick={onDelete}>
          Delete
        </button>
        <div className="pr-4 ml-12">
          <StatusIcon status={status} />
        </div>
      </div>
    </div>
  );
}

type RowContainerProps = {
  children: React.ReactNode;
} & Pick<Search, "id" | "status">;

type ArticleRedirectProps = {
  filename: string;
} & Omit<RowContainerProps, "children">;

function ArticleRedirect(props: ArticleRedirectProps) {
  if (props.status != SearchStatus.error) {
    const link = `/search/${props.id}`;
    return (
      <a href={link} target="_self">
        <div className="py-6">{props.filename}</div>
      </a>
    );
  }

  return <div className="py-6">{props.filename}</div>;
}

function RowContainer(props: RowContainerProps) {
  const hover = props.status == SearchStatus.ready ? "hover:bg-stone-200" : "";
  const cursorStyle = getCursor(props.status);

  return (
    <div className={`border-b border-stone-300 ${cursorStyle} ${hover}`}>
      {props.children}
    </div>
  );
}

export default function History() {
  const { searches, setSearches } = useHistoryStore((state) => ({
    searches: state.searches,
    setSearches: state.setSearches,
  }));
  const user = useAuthStore((state) => state.user);
  const [isLoading, setIsLoading] = useState<boolean>(true);

  const setHistory = (s: Search[]) => {
    setSearches(s);
    setIsLoading(false);
  };

  useEffect(() => {
    if (user != null) {
      getHistory().then(setHistory);
    }
  }, []);

  useEffect(() => {}, [searches]);

  const callback = () => {
    if (user !== null) getHistory().then(setSearches);
  };

  if (isLoading) {
    return (
      <div className="w-100 flex justify-center text-3xl p-24 text-stone-300">
        Loading your history, please wait
      </div>
    );
  }

  if (searches.length == 0) {
    return (
      <div className="w-100 flex justify-center text-3xl p-24 text-stone-300">
        There are no searches in your history
      </div>
    );
  }

  return searches.map((upload: Search) => (
    <RowContainer key={upload.id} status={upload.status} id={upload.id}>
      <SearchRow
        id={upload.id}
        status={upload.status}
        filename={upload.filename}
        callback={callback}
      />
    </RowContainer>
  ));
}
