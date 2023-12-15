import { CloseIcon } from "../../components/Icons";

type Props = {
  children: React.ReactNode;
  setOpen: (open: boolean) => void;
  isOpen: boolean;
};

export default function Modal(props: Props) {
  const { children, setOpen, isOpen } = props;

  const close = () => setOpen(false);

  return (
    <>
      {isOpen && (
        <div
          className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50"
          onClick={close}
        >
          <div
            className="bg-white p-8 shadow-lg lg:w-1/3 lg:h-4/5 md:w-2/3 lg:h-max h-max w-max overflow-y-scroll"
            onClick={(e) => e.stopPropagation()}
          >
            <div className="flex justify-end">
              <button onClick={close}>
                <CloseIcon />
              </button>
            </div>
            {children}
          </div>
        </div>
      )}
    </>
  );
}
