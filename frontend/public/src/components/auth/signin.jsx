import React, { useState } from "react";
import { Link, useNavigate } from "react-router-dom";
import ApiService from "../shared/data-service";
import { toast } from "react-toastify";

const LoginForm = () => {
  const apiService = new ApiService();
  const [errors, setErrors] = useState({});
  const [isLoading, setIsLoading] = useState(false);
  const navigate = useNavigate();

  const [formData, setFormData] = useState({
    username: "",
    password: "",
  });

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData({ ...formData, [name]: value });
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    // Reset previous errors and loading state
    setErrors({});
    setIsLoading(true);

    const newErrors = {};
    if (!formData.username.trim()) {
      newErrors.email = "Email is required";
    } else if (!/^\S+@\S+\.\S+$/.test(formData.username)) {
      newErrors.email = "Invalid email address";
    }
    if (!formData.password.trim()) {
      newErrors.password = "Password is required";
    }
    setErrors(newErrors);
    if (Object.keys(newErrors).length === 0) {
      apiService
        .logIn(formData)
        .then((res) => {
          if (res.data) {
            localStorage.setItem("tokens", JSON.stringify(res.data));
            toast.success(" Login successfully");
            setIsLoading(false);
            if (formData.username === "admin") {
              localStorage.setItem("admin",true);
              navigate("/admin");
            } else {
              navigate("/upload-picture");
            }
          }
          window.location.reload();
        })
        .catch((err) => {
          toast.error(`Inccorrect email or password`);
          setIsLoading(false);
        });
    }

    setIsLoading(false);
  };

  return (
    <div className="flex justify-center items-center h-screen">
      <form
        className="w-full max-w-md bg-white shadow-2xl rounded px-8 pt-6 pb-8 mb-4"
        onSubmit={handleSubmit}
        autoComplete="off"
      >
        <h2 className="text-2xl font-bold mb-4 text-center">Login</h2>

        <div className="mb-4">
          <label
            className="block text-gray-700 text-sm font-bold mb-2"
            htmlFor="email"
          >
            Email
          </label>
          <input
            className={`shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline ${
              errors.email ? "border-red-500" : ""
            }`}
            id="username"
            type="email"
            name="username"
            placeholder="Enter your email"
            value={formData.username}
            onChange={handleChange}
            autoComplete="false"
          />
          {errors.email && (
            <p className="text-red-500 text-xs italic">{errors.email}</p>
          )}
        </div>

        <div className="mb-4">
          <label
            className="block text-gray-700 text-sm font-bold mb-2"
            htmlFor="password"
          >
            Password
          </label>
          <input
            className={`shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline ${
              errors.password ? "border-red-500" : ""
            }`}
            id="password"
            type="password"
            name="password"
            placeholder="Enter your password"
            value={formData.password}
            onChange={handleChange}
          />
          {errors.password && (
            <p className="text-red-500 text-xs italic">{errors.password}</p>
          )}
        </div>

        <div className="mb-4 text-center">
          <p>
            <Link
              to="/forgot-password"
              className="text-blue-500 hover:underline"
            >
              Forgot password?
            </Link>
          </p>
        </div>

        <div className="flex items-center justify-center mb-2">
          <button
            className="w-full bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded focus:outline-none focus:shadow-outline relative"
            type="submit"
            disabled={isLoading}
          >
            {isLoading ? (
              <div className="flex items-center">
                <svg
                  className="animate-spin h-5 w-5 mr-3"
                  xmlns="http://www.w3.org/2000/svg"
                  fill="none"
                  viewBox="0 0 24 24"
                >
                  <circle
                    className="opacity-25"
                    cx="12"
                    cy="12"
                    r="10"
                    stroke="currentColor"
                    strokeWidth="4"
                  ></circle>
                  <path
                    className="opacity-75"
                    fill="currentColor"
                    d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A8.003 8.003 0 0117.709 5.29h-2.083A5.99 5.99 0 0012 2c-1.57 0-3.032.605-4.131 1.709l1.414 1.414A3.99 3.99 0 0112 4a4 4 0 110 8c-.86 0-1.66-.28-2.314-.764l1.428-1.428A5.97 5.97 0 0010 10c0-1.67-.68-3.175-1.768-4.262L6.798 7.212z"
                  ></path>
                </svg>
                Logging In...
              </div>
            ) : (
              "Log In"
            )}
          </button>
        </div>

        <div className="text-gray-700 text-center">
          <p className="mb-2">
            Don't have an account?{" "}
            <Link to="/signup" className="text-blue-500 hover:underline">
              Sign Up
            </Link>
          </p>
        </div>
      </form>
    </div>
  );
};

export default LoginForm;
