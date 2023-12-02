import { Outlet, Link, useNavigate } from "react-router-dom";
import { logout } from "./api";
import { useAuthStore } from "../store/AuthStore";

function StyledLink({ to, display }: { to: string; display: string }) {
  return (
    <div className="flex items-center text-stone-100 font-light h-full hover:text-emerald-800 my-auto hover:text-teal-800">
      <Link to={to}> {display} </Link>
    </div>
  );
}

export default function Navbar() {
  const setUser = useAuthStore((state) => state.setUser);
  const navigate = useNavigate();
  function logoutAndRedirect() {
    navigate("/login");
    logout();
    setUser(null);
  }

  return (
    <>
      <div className="flex h-8 w-full bg-teal-950 px-8 justify-between fixed">
        <StyledLink to="/" display="Home" />
        <button
          className="text-stone-100 font-extralight"
          onClick={logoutAndRedirect}
        >
          Log out
        </button>
      </div>
      <Outlet />
    </>
  );
}
