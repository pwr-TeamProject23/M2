export type Option = {
  label: string;
  value: string;
};

type Props = {
  options: Option[];
  label: string;
  onChange: (value: string | undefined) => void;
  disabled?: boolean;
};

export default function Select(props: Props) {
  const onChange = (e: React.ChangeEvent<HTMLSelectElement>) => {
    if (e.target.value === props.label) props.onChange(undefined);
    else props.onChange(e.currentTarget.value);
  };

  return (
    <div className="flex flex-col">
      <select
        id="select"
        className="border-stone-300"
        onChange={onChange}
        disabled={props.disabled}
      >
        <option value={undefined}>{props.label}</option>
        {props.options.map((option: Option, i:number) => (
          <option key={i} value={option.value}>{option.label}</option>
        ))}
      </select>
    </div>
  );
}
