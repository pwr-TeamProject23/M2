import { useEffect, useState } from "react";
import { PersonIcon } from "../../components/Icons";
import { getSuggestions } from "../api";
import { Author } from "../models";
import { useAuthStore } from "../../store/AuthStore";

function AuthorRow(props: Author) {
  const { name, affiliation, email, src } = props;
  return (
    <>
      <div className="flex space-x-24 items-center px-24 h-min border-t border-stone-300 py-4">
        <PersonIcon />
        <div className="m-6">
          <div className="text-2xl text-stone-800">{name}</div>
          <div className="text-sm text-stone-900 font-light">{email}</div>
          <div className="text-sm text-stone-900 font-light">{affiliation}</div>
          <div className="text-stone-700 font-extralight text-sm">{src}</div>
        </div>
      </div>
    </>
  );
}

export default function ReviewersSuggestions() {
  const getFileName = () => "some.pdf";
  const [authors, setAuthors] = useState<Author[]>([]);
  const user = useAuthStore((state)=> state.user)

  useEffect(() => {
    if (user != null) {
      getSuggestions(user?.user_id).then(setAuthors);
    };
  }, []);

  return (
    <div className="">
      <div className="pb-4 text-stone-900 font-light">
        {`Suggested reviewers for ${getFileName()}`}
      </div>
      {authors.map((author) => (
        <AuthorRow {...author} />
      ))}
    </div>
  );
}
