import { useEffect, useState } from "react";
import { ErrorIcon, PendingIcon } from "../../components/Icons";
import { Search, SearchStatus } from "./models";
import { getHistory, getSearchStatus } from "./api";
import { useAuthStore } from "../../store/AuthStore";
import { CursorStyle } from "../../models/styling";

function StatusIcon(props: Pick<Search, "status">) {
  const status = props.status;

  if (status == SearchStatus.error) return <ErrorIcon />;
  if (status == SearchStatus.pending) return <PendingIcon />;
  if (status == SearchStatus.ready) return null;
}

const getCursor = (status: string) => {
  if (status == SearchStatus.error) return CursorStyle.error;
  if (status == SearchStatus.ready) return CursorStyle.ready;
  if (status == SearchStatus.pending) return CursorStyle.pending;
  return CursorStyle.default;
};

type SearchRowProps = {
  update: (i: number, s: SearchStatus) => void;
  id: number;
} & Pick<Search, "status" | "filename">;

function SearchRow(props: SearchRowProps) {
  const { update, id, status, filename } = props;

  useEffect(() => {
    if (status === SearchStatus.pending) {
      const fetchData = () => {
        getSearchStatus(id).then((newStatus: SearchStatus) => {
          update(id, newStatus);
          if (newStatus !== SearchStatus.pending) clearInterval(intervalId);
        });
      };
      const interval = 5000;
      const intervalId = setInterval(() => fetchData(), interval);
    }
  }, []);

  return (
    <div className="flex items-center justify-between h-full w-full ">
      <div>{filename}</div>
      <div className="pr-4">
        <StatusIcon status={status} />
      </div>
    </div>
  );
}

type RowContainerProps = {
  children: React.ReactNode;
} & Pick<Search, "id" | "status">;

function ArticleRedirect(props: RowContainerProps) {
  if (props.status == SearchStatus.ready) {
    const link = `/search/${props.id}`;
    return (
      <a href={link} target="_self">
        {props.children}
      </a>
    );
  }

  return props.children;
}

function RowContainer(props: RowContainerProps) {
  const hover = props.status == SearchStatus.ready ? "hover:bg-stone-200" : "";
  const cursorStyle = getCursor(props.status);

  return (
    <ArticleRedirect {...props}>
      <div className={`h-16 border-b border-stone-300 ${cursorStyle} ${hover}`}>
        {props.children}
      </div>
    </ArticleRedirect>
  );
}

export default function History() {
  const [searches, setSearches] = useState<Search[]>([]);
  const user = useAuthStore((state) => state.user);

  useEffect(() => {
    if (user != null) {
      getHistory(user?.user_id).then(setSearches);
    }
  }, []);

  const updateSearches = (search_id: number, status: SearchStatus) => {
    const updated = [
      ...searches.map((val: Search) => {
        if (val.id === search_id) {
          let newSearch = { ...val };
          newSearch.status = status;
          return newSearch;
        }
        return val;
      }),
    ];
    setSearches(updated);
  };

  return searches.map((upload: Search) => (
    <RowContainer key={upload.index} status={upload.status} id={upload.id}>
      <SearchRow
        id={upload.id}
        status={upload.status}
        filename={upload.filename}
        update={updateSearches}
      />
    </RowContainer>
  ));
}
