import { useEffect, useState } from "react";
import { ErrorIcon, PendingIcon, CheckmarkIcon } from "../../components/Icons";
import { Search, SearchStatus } from "./models";
import { getHistory } from "./api";
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

function SearchRow(props: Pick<Search, "status" | "filename">) {
  return (
    <div className="flex items-center justify-between h-full w-full ">
      <div>{props.filename}</div>
      <div className="pr-4">
        <StatusIcon status={props.status} />
      </div>
    </div>
  );
}

type RowContainerProps = {
  children: React.ReactNode;
} & Pick<Search, "index" | "status">;

function ArticleRedirect(props: RowContainerProps) {
  if (props.status == SearchStatus.ready) {
    const link = `/search/${props.index}`;
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

  return searches.map((upload: Search) => (
    <RowContainer index={upload.index} status={upload.status}>
      <SearchRow status={upload.status} filename={upload.filename} />
    </RowContainer>
  ));
}
