import { Outlet, Link } from "react-router-dom";

function StyledLink({ to, display }: { to: string; display: string }) {
  return (
    <div className="flex items-center text-stone-100 font-light h-full hover:text-emerald-800 my-auto hover:text-teal-800">
      <Link to={to}> {display} </Link>
    </div>
  );
}

export default function Navbar() {
  return (
    <>
      <div className="flex h-8 w-full bg-teal-950 px-8">
        <StyledLink to="/" display="Home" />
      </div>
      <Outlet />
    </>
  );
}
