import { useEffect, useState } from "react";
import { Author, SuggestionsResponseModel } from "../models";
import { useAuthStore } from "../../store/AuthStore";
import { useParams } from "react-router-dom";
import { getSuggestions } from "../api";
import { Option } from "./Select";

export default function useSuggestions() {
  const user = useAuthStore((state) => state.user);
  const { uploadId } = useParams();
  const [authors, setAuthors] = useState<Author[]>([]);
  const [venueOptions, setVenueOptions] = useState<Option[]>([]);

  const setData = (data: SuggestionsResponseModel) => {
    setAuthors(data.authors);
    setVenueOptions(data.venues.map((v: string) => ({ label: v, value: v })));
  };

  useEffect(() => {
    if (user != null && uploadId) {
      getSuggestions(uploadId).then(setData);
    }
  }, []);

  return {
    authors,
    venueOptions,
  };
}