import '../style/login.css'
import React ,{ useState } from 'react';
import { ACCESS_TOKEN,REFRESH_TOKEN } from '../constants';
import api from "../api.js"
import { useNavigate } from 'react-router-dom';

function Login(){
    
    const navigate = useNavigate()
    const [Input,setInput] = useState({
        username: '',
        password: '',
    })
    
    
    const handleSubmit = (e)=>{
        e.preventDefault();
        LoginApi(Input,navigate);
    }
    const handleChange = (e)=>{
        const { placeholder , value} = e.target
        switch(e.target.placeholder){ 
            case 'username':
                setInput(Input =>({...Input, [placeholder]: value}))
                break;
            case 'password':
                setInput(Input => ({...Input, [placeholder]: value}));
                break;
            default:
                console.log('invalid placeholder !!')
        }
    }

    
    return (
        <div className='background'>
            <div className='log-form-window'>
                <p className='form-title'>Welcome Back</p>
                <form onSubmit={handleSubmit}>
                    <input type='text' onChange={handleChange} className='input' placeholder='username' required/>
                    <input type='password' onChange={handleChange} className='input1' placeholder='password' required/>
                    <button type='submit' className='form-submit-but'>Log in</button>
                </form>
                <div className='other-option-div'>
                    <span className='go-to-signup'>
                        don't have an account yet ? &nbsp;<strong onClick={()=>{navigate('/signup')}}>Sign up</strong> {/*TODO: link to sign in form*/}
                    </span>
                    <span>
                        &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<strong>Forgot password ?</strong> {/*TODO: link to change password using email */}
                    </span>

                </div>
                
            </div>
        </div>
    );
}
async function LoginApi(Input,navigate){
    try {
        const response = await api.post("/api/login/token/",
            {
                headers:{"Content-Type":"application/json",},
                "username": Input.username,
                "password": Input.password,
            });
        const data = await response.data;  
        console.log(data);
        localStorage.setItem(ACCESS_TOKEN,(data.access))
        localStorage.setItem(REFRESH_TOKEN,(data.refresh))
        console.log(localStorage.getItem(ACCESS_TOKEN))
        navigate('/home')
    } catch (error) {
        console.log(error.code)
    }
}
export default Login;
export {LoginApi}