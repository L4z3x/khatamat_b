import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import '../style/sidebar.css';
import logo from '../assets/img/Default-Profile-pic.jpg';
import Logout from './logout'; // Import the Logout component

export default function Sidebar({ isOpen, toggleSidebar }) {
  const [showLogout, setShowLogout] = useState(false);

  const handleLogoutClick = (e) => {
    e.preventDefault();
    setShowLogout(true);
  };

  const handleCloseLogout = () => {
    setShowLogout(false);
  };

  return (
    <div>
      <div className={`sidebar ${isOpen ? 'open' : ''}`}>
        <div className="menu-icon" onClick={toggleSidebar}>
          <div className="bar"></div>
          <div className="bar"></div>
          <div className="bar"></div>
        </div>
        {isOpen && (
          <div className="sidebar-photo">
            <img src={logo} alt="Sidebar Logo" />
          </div>
        )}
        <ul>
          <li><a href="/profile" className='sidebar-item'>Profile</a></li>
          <li><a href="/help-center" className='sidebar-item'>Help Center</a></li>
          <li><a href="/feedback" className='sidebar-item'>Feedback</a></li>
          <li><a href="/contact" className='sidebar-item'>Contact</a></li>
          <li><a href="/about" className='sidebar-item'>About</a></li>
          <li><a href="/faqs" className='sidebar-item'>FAQs</a></li>
          <li><a href="/logout" className='sidebar-item' onClick={handleLogoutClick}>Logout</a></li>
          <li><a href="/terms-privacy" className='term-privacy'>terms</a> <a href="/terms-privacy" className='term-privacy'>privacy</a></li>
        </ul>
      </div>
      <Logout show={showLogout} onClose={handleCloseLogout} />
    </div>
  );
}
