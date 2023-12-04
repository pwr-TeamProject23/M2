type Props = {
  progress: number;
};

export default function CircularProgressBar(props: Props) {
  const strokeWidth = 5;
  const radius = 25;
  const circumference = 2 * Math.PI * radius;
  const side = 60;
  const center = side / 2;

  const progressOffset = circumference - props.progress * circumference;

  return (
    <div>
      <svg
        height={side}
        width={side}
        className="transform rotate-[-90deg] scale-y-[-1]"
      >
        <circle
          className="stroke-stone-200"
          strokeWidth={strokeWidth}
          fill="transparent"
          r={radius}
          cx={center}
          cy={center}
        />
        <circle
          className="stroke-emerald-900"
          strokeWidth={strokeWidth}
          strokeDasharray={circumference}
          strokeDashoffset={progressOffset}
          fill="transparent"
          r={radius}
          cx={center}
          cy={center}
        />
      </svg>
    </div>
  );
}
