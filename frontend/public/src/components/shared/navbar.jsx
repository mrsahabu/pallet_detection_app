import React from "react";
import { useLocation } from "react-router-dom";

const Navbar = ({ onLogout }) => {
  const location = useLocation();
  const restrictedPaths = ["/", "/signup", "/forgot-password"];

  if (restrictedPaths.includes(location.pathname)) {
    return null;
  }

  return (
    <nav className="bg-gradient-to-br from-blue-300 to-purple-500 p-4 fixed w-full top-0 flex justify-between items-center z-10 ">
      <div className="flex items-center">
        {/* Icon or logo */}
        <svg
          xmlns="http://www.w3.org/2000/svg"
          className="h-8 w-8 text-white mr-2"
          viewBox="0 0 20 20"
          fill="currentColor"
        >
          <path
            fillRule="evenodd"
            d="M10 2a2 2 0 1 0 0 4 2 2 0 0 0 0-4zM7 10a2 2 0 1 0 0 4 2 2 0 0 0 0-4zm6-6a2 2 0 1 0 0 4 2 2 0 0 0 0-4zm-1.5 6.5a2 2 0 1 0 0 4 2 2 0 0 0 0-4zm-4 4a2 2 0 1 0 0 4 2 2 0 0 0 0-4z"
            clipRule="evenodd"
          />
        </svg>
        <span className="text-white font-semibold">Good Folks</span>
      </div>
      <button
        className="bg-white hover:bg-gray-200 text-blue-500 font-bold py-2 px-4 rounded focus:outline-none focus:shadow-outline"
        onClick={onLogout}
      >
        Logout
      </button>
    </nav>
  );
};

export default Navbar;
