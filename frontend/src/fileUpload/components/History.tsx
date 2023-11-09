import { Children } from "react";
import { ErrorIcon, PendingIcon, CheckmarkIcon } from "../../components/Icons";

enum Status {
  pending = "pending",
  error = "error",
  ready = "ready",
}

const CursorStyle = {
  pending: "cursor-progress",
  error: "cursor-not-allowed",
  ready: "cursor-pointer",
  default: "cursor-default",
};

type Upload = {
  index: number;
  uploadId: number;
  fileName: string;
  status: string;
};

function StatusIcon(props: Pick<Upload, "status">) {
  const status = props.status;

  if (status == Status.error) return <ErrorIcon />;
  if (status == Status.pending) return <PendingIcon />;
  if (status == Status.ready) return <CheckmarkIcon />;
}

const getCursor = (status: string) => {
  if (status == Status.error) return CursorStyle.error;
  if (status == Status.ready) return CursorStyle.ready;
  if (status == Status.pending) return CursorStyle.pending;
  return CursorStyle.default;
};

function Upload(props: Pick<Upload, "status" | "fileName">) {
  return (
    <div className="flex items-center justify-between h-full w-full ">
      <div>{props.fileName}</div>
      <StatusIcon status={props.status} />
    </div>
  );
}

type RowContainerProps = {
  children: React.ReactNode;
} & Pick<Upload, "index" | "status">;

function ArticleRedirect(props: RowContainerProps) {
  if (props.status == Status.ready) {
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
  const hover = props.status == Status.ready ? "hover:bg-stone-300" : "";
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
  const uploads = [
    {
      uploadId: 1,
      index: 0,
      fileName: "pendingupload.pdf",
      status: "pending",
    },
    {
      uploadId: 2,
      index: 1,
      fileName: "errorupload.pdf",
      status: "error",
    },
    {
      uploadId: 4,
      index: 2,
      fileName: "readyupload.pdf",
      status: "ready",
    },
    {
      uploadId: 8,
      index: 3,
      fileName: "readyupload.pdf",
      status: "ready",
    },
  ];
  return uploads.map((upload: Upload) => (
    <RowContainer index={upload.index} status={upload.status}>
      <Upload status={upload.status} fileName={upload.fileName} />
    </RowContainer>
  ));
}
