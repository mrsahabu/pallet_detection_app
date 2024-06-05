import React, { useState } from "react";
import { Link, useLocation, useNavigate } from "react-router-dom";
import ApiService from "../shared/data-service";
import { toast } from "react-toastify";

const ResetPassword = () => {
  const api = new ApiService();
  const location = useLocation();
  const navigation = useNavigate();
  const searchParams = new URLSearchParams(location.search);
  const accessToken = searchParams.get("access_token");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");

  const handleChange = (e) => {
    setPassword(e.target.value);
  };

  const handleSubmit = (e) => {
    e.preventDefault();

    // Basic validation
    if (!password.trim()) {
      setError("Password is required");
      return;
    }
    toast.loading("Please wait");
    api
      .resetPassword(password, accessToken)
      .then((res) => {
        if (res.data) {
          toast.dismiss();
          toast.success(`Password updated successfully`);
          navigation("/");
        }
      })
      .catch((err) => {
        toast.dismiss();
        toast.error(`Something went wrong ${err}`);
      });

    setPassword("");
    setError("");
  };

  return (
    <div className="flex justify-center items-center h-screen">
      <form
        className="w-full max-w-md bg-white shadow-2xl rounded px-8 pt-6 pb-8 mb-4"
        onSubmit={handleSubmit}
      >
        <h2 className="text-2xl font-bold mb-4 text-center">Reset Password</h2>
        <div className="mb-4">
          <label
            className="block text-gray-700 text-sm font-bold mb-2"
            htmlFor="password"
          >
            Enter new Password
          </label>
          <input
            className={`shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline ${
              error ? "border-red-500" : ""
            }`}
            id="password"
            type="password"
            name="password"
            placeholder="Password"
            value={password}
            onChange={handleChange}
          />
          {error && <p className="text-red-500 text-xs italic">{error}</p>}
        </div>
        <div className="flex items-center justify-between">
          <button
            className="bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded focus:outline-none focus:shadow-outline"
            type="submit"
          >
            Reset Password
          </button>
          <Link
            to={"/"}
            className="bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded focus:outline-none focus:shadow-outline"
            type="submit"
          >
            Go Back
          </Link>
        </div>
      </form>
    </div>
  );
};

export default ResetPassword;
