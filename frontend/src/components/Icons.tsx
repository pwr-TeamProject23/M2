import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import {
  faCircleUp,
  faXmarkCircle,
  faCheckCircle,
  faUser,
  faClock,
  faRectangleXmark,
} from "@fortawesome/free-regular-svg-icons";

const accentColor = "#042F2E";
const red = "#7F1D1D";
const stone = "#9EA8A2";

export function UploadIcon() {
  return (
    <div className="flex justify-center">
      <FontAwesomeIcon
        icon={faCircleUp}
        style={{ color: accentColor }}
        size="xl"
      />
    </div>
  );
}

export function ErrorIcon() {
  return (
    <div className="flex justify-center">
      <FontAwesomeIcon icon={faXmarkCircle} style={{ color: red }} size="xl" />
    </div>
  );
}

export function CloseIcon() {
  return (
    <div className="flex justify-center">
      <FontAwesomeIcon
        icon={faXmarkCircle}
        style={{ color: "#9CA3AF" }}
        size="xl"
      />
    </div>
  );
}

export function CheckmarkIcon() {
  return (
    <div className="flex justify-center">
      <FontAwesomeIcon
        icon={faCheckCircle}
        style={{ color: accentColor }}
        size="xl"
      />
    </div>
  );
}

export function PendingIcon() {
  return (
    <div className="flex justify-center">
      <FontAwesomeIcon icon={faClock} style={{ color: stone }} size="xl" />
    </div>
  );
}

export function PersonIcon() {
  return (
    <FontAwesomeIcon icon={faUser} style={{ color: accentColor }} size="xl" />
  );
}
