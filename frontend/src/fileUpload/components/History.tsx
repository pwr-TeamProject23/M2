import { useEffect, useState } from "react";
import { ErrorIcon, PendingIcon, CheckmarkIcon } from "../../components/Icons";
import { Upload, UploadStatus } from "./models";
import { getHistory } from "./api";
import { useAuthStore } from "../../store/AuthStore";

const CursorStyle = {
  pending: "cursor-progress",
  error: "cursor-not-allowed",
  ready: "cursor-pointer",
  default: "cursor-default",
};

function StatusIcon(props: Pick<Upload, "status">) {
  const status = props.status;

  if (status == UploadStatus.error) return <ErrorIcon />;
  if (status == UploadStatus.pending) return <PendingIcon />;
  if (status == UploadStatus.ready) return <CheckmarkIcon />;
}

const getCursor = (status: string) => {
  if (status == UploadStatus.error) return CursorStyle.error;
  if (status == UploadStatus.ready) return CursorStyle.ready;
  if (status == UploadStatus.pending) return CursorStyle.pending;
  return CursorStyle.default;
};

function UploadRow(props: Pick<Upload, "status" | "filename">) {
  return (
    <div className="flex items-center justify-between h-full w-full ">
      <div>{props.filename}</div>
      <StatusIcon status={props.status} />
    </div>
  );
}

type RowContainerProps = {
  children: React.ReactNode;
} & Pick<Upload, "index" | "status">;

function ArticleRedirect(props: RowContainerProps) {
  if (props.status == UploadStatus.ready) {
    const link = `/article/${props.index}`;
    return (
      <a href={link} target="_self">
        {props.children}
      </a>
    );
  }

  return props.children;
}

function RowContainer(props: RowContainerProps) {
  const background = props.index % 2 == 0 ? "bg-stone-100" : "bg-stone-200";
  const hover = props.status == UploadStatus.ready ? "hover:bg-stone-300" : "";
  const cursorStyle = getCursor(props.status);

  return (
    <ArticleRedirect {...props}>
      <div className={`h-16 p-8 ${background} ${cursorStyle} ${hover}`}>
        {props.children}
      </div>
    </ArticleRedirect>
  );
}

export default function History() {
  const [uploads, setUploads] = useState<Upload[]>([]);
  const user = useAuthStore((state) => state.user);

  useEffect(() => {
    if (user!=null) {
      getHistory(user?.user_id).then(setUploads);
    }
    
  },[])
  
  return uploads.map((upload: Upload) => (
    <RowContainer index={upload.index} status={upload.status}>
      <UploadRow status={upload.status} filename={upload.filename} />
    </RowContainer>
  ));
}
