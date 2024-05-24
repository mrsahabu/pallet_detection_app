import React, { useState } from "react";
import { Link } from "react-router-dom";

const ForgotPassword = () => {
  const [email, setEmail] = useState("");
  const [error, setError] = useState("");
  const [successMessage, setSuccessMessage] = useState("");

  const handleChange = (e) => {
    setEmail(e.target.value);
  };

  const handleSubmit = (e) => {
    e.preventDefault();

    // Basic validation
    if (!email.trim()) {
      setError("Email is required");
      return;
    } else if (!/^\S+@\S+\.\S+$/.test(email)) {
      setError("Invalid email address");
      return;
    }

    // Here you can implement your forgot password logic, like sending a reset link to the email

    // Simulating a successful request for demonstration
    setSuccessMessage(`Password reset link has been sent to ${email}`);
    setEmail("");
    setError("");
  };

  return (
    <div className="flex justify-center items-center h-screen">
      <form
        className="w-full max-w-md bg-white shadow-2xl rounded px-8 pt-6 pb-8 mb-4"
        onSubmit={handleSubmit}
      >
        <h2 className="text-2xl font-bold mb-4 text-center">Forgot Password</h2>
        <div className="mb-4">
          <label
            className="block text-gray-700 text-sm font-bold mb-2"
            htmlFor="email"
          >
            Email
          </label>
          <input
            className={`shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline ${
              error ? "border-red-500" : ""
            }`}
            id="email"
            type="email"
            name="email"
            placeholder="Enter your email"
            value={email}
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
        {successMessage && (
          <p className="text-green-500 text-center mt-4">{successMessage}</p>
        )}
      </form>
    </div>
  );
};

export default ForgotPassword;
