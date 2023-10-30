import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import {
  faCircleUp,
  faXmarkCircle,
  faCheckCircle,
  faUser,
  faClock,
} from "@fortawesome/free-regular-svg-icons";

const accentColor = "#042F2E";
const red = "#FF0000";
const green = "#008000";

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

export function CheckmarkIcon() {
  return (
    <div className="flex justify-center">
      <FontAwesomeIcon
        icon={faCheckCircle}
        style={{ color: green }}
        size="xl"
      />
    </div>
  );
}

export function PendingIcon() {
  return (
    <div className="flex justify-center">
      <FontAwesomeIcon
        icon={faClock}
        style={{ color: accentColor }}
        size="xl"
      />
    </div>
  );
}

export function PersonIcon() {
  return (
    <FontAwesomeIcon icon={faUser} style={{ color: accentColor }} size="xl" />
  );
}
