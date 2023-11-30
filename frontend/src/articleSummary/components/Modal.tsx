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
          className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center"
          onClick={close}
        >
          <div
            className="bg-white p-8 shadow-lg w-1/3 h-2/3 overflow-y-scroll"
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
