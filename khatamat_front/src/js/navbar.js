import React, { useState, useEffect } from 'react';
import { useLocation, useNavigate } from 'react-router-dom';
import Sidebar from './sidebar';
import '../style/navbar.css';

function Navbar({ loggedIn }) {
    console.log(loggedIn);
    const location = useLocation();
    const nav = useNavigate();
    const [activePath, setActivePath] = useState(location.pathname);
    const [isSidebarOpen, setSidebarOpen] = useState(false);

    const toggleSidebar = () => {
        setSidebarOpen(!isSidebarOpen);
    };
    useEffect(() => {
        setActivePath(location.pathname);
    }, [location.pathname]);

    const renderLink = (path, label) => (
        <li className="li-nav">
            <a onClick={() => { nav(path); }} className={activePath === path ? 'active li-a' : 'li-a'}>{label}</a>
        </li>
    );

    return (
        <div className="backdiv">
            <ul className="ul-nav">
                <li className="title li-nav">
                    <a onClick={() => { nav('/Userhome'); }} className="title">ختمات</a>
                </li>
                {loggedIn==='true' ? (
                    <>
                        {renderLink('/Userhome', 'Home')}
                        {renderLink('/articles', 'Articles')}
                        {renderLink('/khatamat', 'Khatamat')}
                        {renderLink('/resources', 'Resources')}
                        <li className="li-nav">
                            <a className="li-a">Search</a>
                        </li>
                        <li className="user1">
                            <div className="user">
                                <div className="menu-icon" onClick={toggleSidebar}>
                                    <div className="bar"></div>
                                    <div className="bar"></div>
                                    <div className="bar"></div>
                                </div>
                                <Sidebar isOpen={isSidebarOpen} toggleSidebar={toggleSidebar} />
                            </div>
                        </li>
                    </>
                ) : (
                    <>
                        {renderLink('/home', 'Home')}
                        {renderLink('/forum', 'Forum')}
                        {renderLink('/aboutus', 'About')}
                        {renderLink('/faqs', 'FAQs')}
                        {renderLink('/contact', 'Contact')}
                        {location.pathname !== '/signup' && location.pathname !== '/login' && (
                            <li className="user1">
                                <button onClick={() => { nav('/signup'); }} className="signup-button">
                                    Sign Up
                                </button>
                            </li>
                        )}
                    </>
                )}
            </ul>
        </div>
    );
}

export default Navbar;
