import { useAuthStore } from "../../store/AuthStore";

const reviewedBanner =
  "Discover smart reviewer suggestions at a click of a button";

export default function Title() {
  const user = useAuthStore((state) => state.user);

  return (
    <div className="w-1/2">
      <div className="text-stone-900 text-3xl">{`Hello ${user?.email}!`}</div>
      <div className="text-stone-900 text-s font-extralight">
        {reviewedBanner}
      </div>
    </div>
  );
}
