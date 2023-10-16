import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import {
  faCircleUp,
  faXmarkCircle,
  faCheckCircle,
} from "@fortawesome/free-regular-svg-icons";

const accentColour = "#088586";
const red = "#FF0000";
const green = "#008000";

export function UploadIcon() {
  return (
    <div className="flex justify-center">
      <FontAwesomeIcon
        icon={faCircleUp}
        style={{ color: accentColour }}
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
