import React from "react";
import { useLocation,Navigate } from "react-router-dom";
import axios from "axios";
import ApiService from "./data-service";
const restrictedPaths = ["/", "/signup", "/forgot-password"];

const AppWrapper = (props) => {
  const api = new ApiService();
  const isAuthenticated = api.getAccessToken();
  const isAdmin = api.getAdmin();
  const location = useLocation();

  if (isAuthenticated) {
    if (isAdmin) {
      return <Navigate to="/admin" replace />;
    } else {
      return <Navigate to="/upload-picture" />;
    }
  } else if (!isAuthenticated && !restrictedPaths.includes(location.pathname)) {
    return <Navigate to="/" />;
  }

  axios.interceptors.request.use(
    (config) => {
      const token = api.getAccessToken();
      if (token) {
        config.headers["Authorization"] = "Bearer " + token;
        config.headers["system"] = "assistance_tool";
      }
      return config;
    },
    (error) => {
      Promise.reject(error);
    }
  );
};

export default AppWrapper;
