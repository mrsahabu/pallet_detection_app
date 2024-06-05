// ProfileModal.js
import React from 'react';
import 'primeicons/primeicons.css';

const ProfileModal = ({ isOpen, onClose, user }) => {
  if (!isOpen) return null;

  return (
    <div className="fixed inset-0 bg-gray-600 bg-opacity-50 flex justify-center items-center z-10">
      <div className="bg-white rounded-lg shadow-lg w-1/3">
        <div className="flex justify-between items-center border-b p-4">
          <h2 className="text-xl font-bold">User Profile</h2>
          <button onClick={onClose} className="text-gray-600 hover:text-gray-800">
            <i className="pi pi-times"></i>
          </button>
        </div>
        <div className="p-4">
          <div className="flex items-center mb-4">
            <i className="pi pi-user mr-2 text-blue-500"></i>
            <span className="font-semibold">Name:</span>
            <span className="ml-2">{user?.name || user.username}</span>
          </div>
          <div className="flex items-center mb-4">
            <i className="pi pi-envelope mr-2 text-blue-500"></i>
            <span className="font-semibold">Email:</span>
            <span className="ml-2">{user.email}</span>
          </div>
          <div className="flex items-center mb-4">
            <i className="pi pi-briefcase mr-2 text-blue-500"></i>
            <span className="font-semibold">Role:</span>
            <span className="ml-2">{user.role}</span>
          </div>
        </div>
        <div className="border-t p-4 flex justify-end">
          <button onClick={onClose} className="bg-blue-500 text-white px-4 py-2 rounded hover:bg-blue-700">
            Close
          </button>
        </div>
      </div>
    </div>
  );
};

export default ProfileModal;
