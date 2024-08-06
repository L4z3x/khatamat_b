import React from 'react';
import '../style/NotFound.css'; // Ensure you have this CSS file

export default function NotFound({loggedIn}) {
    return (
        <div className="notfound-back">
            <div className="notfound-content">
                <h1 className="notfound-title">404</h1>
                <p className="notfound-description">
                    Oops! The page you’re looking for doesn’t exist.
                </p>
                <p className="notfound-subdescription">
                    It might have been removed, renamed, or you might have just entered the wrong URL.
                </p>
                <a href="/home" className="notfound-button">Go to Home</a>
                <a href="/contact" className="notfound-link">Contact Us</a>
            </div>
        </div>
    );
}
