import React, { useState } from "react";
import "../style/logout.css";

function Logout({ show, onClose }) {
  if (!show) {
    return null;
  }

  const handleLogout = () => {
    localStorage.clear();
    window.location.href = "/login"; // Redirect to login page
    console.log("User logged out");
  };

  return (
    <div className="logout-modal">
      <div className="logout-modal-content">
        <p>Are you sure you want to logout?</p>
        <div className="logout-modal-buttons">
          <button className="confirm-button" onClick={handleLogout}>
            Yes
          </button>
          <button className="cancel-button" onClick={onClose}>
            No
          </button>
        </div>
      </div>
    </div>
  );
}

export default Logout;
