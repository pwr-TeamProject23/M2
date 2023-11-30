interface Props<T> {
  displayName: string;
  setSelectedTab: (option: T) => void;
  isSelected: boolean;
}

export default function Tab<T>(props: Props<T>) {
  const { displayName, isSelected, setSelectedTab } = props;
  const onSelected = () => setSelectedTab(displayName as T);
  const underLine = isSelected ? "border-b-2 border-teal-950" : "";
  const onHover = isSelected ? "" : "hover:border-b-2 hover:border-stone-300";
  const style = `w-full p-2 flex items-center justify-center ${onHover} ${underLine}`;

  return (
    <div className={style} onClick={onSelected}>
      <button>{displayName}</button>
    </div>
  );
}
