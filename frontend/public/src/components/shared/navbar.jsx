import React, { useState } from "react";
import { Link, useLocation } from "react-router-dom";
import { Menubar } from "primereact/menubar";
import "primereact/resources/themes/saga-blue/theme.css";
import "primereact/resources/primereact.min.css";
import "primeicons/primeicons.css";
import ApiService from "./data-service";
import ProfileModal from "./modals/userProfile";
import { toast } from "react-toastify";

const Navbar = ({ onLogout }) => {
  const api = new ApiService();
  const location = useLocation();
  const [viewUser, setViewUser] = useState(false);
  const [userDetails, setUserDetails] = useState();
  const start = (
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
      <Link to="/upload-picture" className="text-white font-semibold">
        Good Folks
      </Link>
    </div>
  );

  const viewModal = () => {
    toast.loading("Please wait");
    api
      .getUserDetails()
      .then((res) => {
        setViewUser(true);
        setUserDetails(res.data);
        toast.dismiss();
      })
      .catch(() => {
        toast.dismiss();
        toast.error("Something went wrong");
      });
  };

  const onCloseModal = () => {
    setViewUser(false);
  };

  const items = [
    {
      label: " Profile",
      command: () => {
        viewModal();
      },
    },
    {
      label: " Upload",
      command: () => {
        window.location.href = "/upload-picture";
      },
    },
    {
      label: " Records",
      command: () => {
        window.location.href = "/previous-record";
      },
    },
    api.getAdmin() && {
      label: " Dashboard",
      command: () => {
        window.location.href = "/admin";
      },
    },
    {
      label: "Logout",
      icon: "pi pi-sign-out",
      command: onLogout,
    },
  ].filter(Boolean); // Remove false values (for non-admin users)

  const restrictedPaths = [
    "/",
    "/signup",
    "/forgot-password",
    "/reset_password",
  ];

  if (restrictedPaths.includes(location.pathname)) {
    return null;
  }

  return (
    <>
      <Menubar model={items} start={start} className="w-full" />
      <ProfileModal
        isOpen={viewUser}
        onClose={onCloseModal}
        user={userDetails}
      />
    </>
  );
};

export default Navbar;
