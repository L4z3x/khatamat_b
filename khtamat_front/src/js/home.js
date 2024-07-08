import React ,  { useEffect,useRef } from 'react'
import '../style/home.css'

export default function Home () {
    const imgRef = useRef(null)
    const homeRef = useRef(null)
    const handleSize = ()=>{
        console.log('resized')
        if (imgRef.current && homeRef.current) {
            console.log(imgRef.current.height);
            homeRef.current.style.height = `${imgRef.current.height}px` ;
        }
    }
    useEffect(() => {
        window.addEventListener('resize', handleSize);
        handleSize();
        return () => {
            window.removeEventListener('resize', handleSize);
        };
    }, []);
return( 
        <div ref={homeRef} className='home-back'>
            <img  onLoad={handleSize} ref={imgRef} src={require('../img/homeback.jpg')} className='home-back-img'/>
            <span className='home-welcome'>welcome to</span>
            <span className='home-title'>ختمات</span>
            
            <div className='home-signup-login'>
                <div>
                    <span className='home-but-span'>First time here ? </span>
                    <button className='home-but'>Sign up</button>
                </div>
                <div>
                    <span className='home-but-span'>Already have an account ?</span>
                    <button className='home-but'>Login</button>
                </div>
                
            </div>
        </div>

)
}