import { useEffect, useState } from "react";
import { Author, SuggestionsResponseModel } from "../models";
import { useAuthStore } from "../../store/AuthStore";
import { useParams } from "react-router-dom";
import { getSuggestions, getFilename } from "../api";
import { Option } from "./Select";
import { SearchStatus } from "../../fileUpload/components/models";

export default function useSuggestions(status?: SearchStatus) {
  const user = useAuthStore((state) => state.user);
  const { searchId } = useParams();
  const [authors, setAuthors] = useState<Author[]>([]);
  const [venueOptions, setVenueOptions] = useState<Option[]>([]);
  const [filename, setFilename] = useState<string>();
  const [isLoading, setLoading] = useState<boolean>(true);
  const isUploadReady = status === SearchStatus.ready;

  const setData = (data: SuggestionsResponseModel) => {
    setAuthors(data.authors);
    setVenueOptions(data.venues.map((v: string) => ({ label: v, value: v })));
  };

  useEffect(() => {
    if (user != null && searchId) {
      getFilename(searchId).then((r) => setFilename(r.file_name));
      if (isUploadReady) {
        getSuggestions(searchId)
          .then(setData)
          .then(() => setLoading(false));
      }
    }
  }, []);

  useEffect(() => {
    if (isUploadReady && searchId) {
      getSuggestions(searchId)
        .then(setData)
        .then(() => setLoading(false));
    }
  }, [status]);

  return {
    authors,
    venueOptions,
    filename,
    isLoading,
  };
}
