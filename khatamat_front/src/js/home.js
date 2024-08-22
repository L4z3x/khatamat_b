import React, { useEffect, useRef } from 'react';
import '../style/home.css';
import { useNavigate } from 'react-router-dom';
export default function Home() {

    const nav = useNavigate();
    const imgRef = useRef(null);
    const homeRef = useRef(null);
    const handleSize = () => {
        console.log('resized');
        if (imgRef.current && homeRef.current) {
            console.log(imgRef.current.height);
            homeRef.current.style.height = `${imgRef.current.height}px`;
        }
    }
    useEffect(() => {
        window.addEventListener('resize', handleSize);
        handleSize();
        return () => {
            window.removeEventListener('resize', handleSize);
        };
    }, []);
    return (
        <div ref={homeRef} className='home-back'>
            <di v className='home-content'>
                <span className='home-welcome'>Welcome</span>
                <p className='home-description'>
                    Join us in a spiritual journey to read and complete the Holy Quran together.
                    Connect with fellow Muslims, participate in group readings, and grow your faith.
                </p>
                <div className='home-signup-login'>
                    <div>
                        <span className='home-but-span'>First time here?</span>
                        <button onClick={()=>{nav('/signup')}} className='home-but'>Sign up</button>
                    </div>
                    <div>
                        <span className='home-but-span'>Already have an account?</span>
                        <button  onClick={()=>{nav('/login')}} className='home-but'>Login</button>
                    </div>
                </div>
                <div className='home-info'>
                    <div className='home-info-item'>
                        <h3>What is Khatamat?</h3>
                        <p>Khatamat is a platform that brings together Muslims to complete readings of the Holy Quran, known as khatmas.</p>
                        <a href='/what-is-khatamat' className='home-info-link'>Learn more</a>
                    </div>
                    <div className='home-info-item'>
                        <h3>About Us</h3>
                        <p>We are a group dedicated to earning Allah's blessings by providing a space for collective Quran reading and remembrance of Allah.</p>
                        <a href='/aboutus' className='home-info-link'>More about us</a>
                    </div>
                    <div className='home-info-item'>
                        <h3>Contact Us</h3>
                        <p>Have any questions? Get in touch with us for more information.</p>
                        <a href='/contact' className='home-info-link'>Contact us</a>
                    </div>
                </div>
            </di>
        </div>
    );
}
