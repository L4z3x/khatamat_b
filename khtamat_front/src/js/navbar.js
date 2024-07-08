import React, {useRef } from 'react'
import '../style/navbar.css'
export default function Navbar(){
    const GoProfile = ()=>{window.location.href = '/profile';};
    const homeRef = useRef('');
    const contactRef = useRef('');
    const aboutRef = useRef('');
    const khatamatRef = useRef('');
    const changeTagColor = ()=>{
        const url = window.location.pathname;
        switch(url) {
            case '/about':
                aboutRef.current.style.color = 'green';
                break;
            case '/contact':
                contactRef.current.style.color = 'green';
                break;
            case '/home':
                homeRef.current.style.color = 'green';
                break;
        }
    }
    return(
        <div onLoad={changeTagColor}className='backdiv'>
            <ul className='ul-nav '>
                <li className='title li-nav'>
                    <a ref={khatamatRef} className='title li-nav'>ختمات</a>
                </li>
                <li className='li-nav'>
                    <a onClick={()=>{window.location.pathname = '/home'}} ref={homeRef} className='li-nav'>Home</a>
                </li>
                <li className='li-nav'>
                    <a onClick={()=>{window.location.pathname = '/contact'}} ref={contactRef} className='li-nav'>Contact</a>
                </li>
                <li className='li-nav'>
                    <a onClick={()=>{window.location.pathname = '/about'}} ref={aboutRef} className='li-nav'>About</a>
                </li>
                <li className='user1'>
                    <div className='user'>
                        <a>username</a>
                        <img className='profile-pic' onClick={GoProfile} src={require('../img/Default-Profile-pic.jpg')}/>
                    </div>
                </li>
            </ul>
        </div>
            
    )
}

