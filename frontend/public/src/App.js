import "./App.css";
import ForgotPassword from "./components/auth/forgetPassword";
import LoginForm from "./components/auth/signin";
import SignupForm from "./components/auth/signup";
import { BrowserRouter, Routes, Route } from "react-router-dom";
import UploadCapturePicture from "./components/home/uploadPhoto";
import { ToastContainer, toast } from "react-toastify";
import "react-toastify/dist/ReactToastify.css";
import Navbar from "./components/shared/navbar";
import AdminDashboard from "./components/admin/dashboard";
import ApiService from "./components/shared/data-service";
import AppWrapper from "./components/shared/AppWraper";

function App() {
  const api = new ApiService();
  const handleLogout = () => {
    toast.loading("Please wait");
    api
      .logOut()
      .then((res) => {
        if (res.data) {
          localStorage.clear();
          window.location.href = "/";
          toast.success("Logout");
        }
      })
      .catch((err) => {
        toast.error(`Something went wrong ${err}`);
      });
  };

  const isAuthenticated = api.getAccessToken();
  const isAdmin = api.getAdmin();

  return (
    <>
      <ToastContainer />

      <BrowserRouter>
        <AppWrapper />
        <Navbar onLogout={handleLogout} />
        <Routes>
          <Route path="/" element={<LoginForm />} />
          <Route path="/signup" element={<SignupForm />} />
          <Route path="/forgot-password" element={<ForgotPassword />} />
          {isAuthenticated && !isAdmin && (
            <Route path="/upload-picture" element={<UploadCapturePicture />} />
          )}
          {isAuthenticated && isAdmin && (
            <Route path="/admin" element={<AdminDashboard />} />
          )}
          <Route path="**" element={<LoginForm />} />
        </Routes>
      </BrowserRouter>
    </>
  );
}

export default App;
