import '../style/login.css'
import React ,{ useState } from 'react';

const changePath = ()=>{
    let url = window.location.pathname
    console.log(url)
    window.location.pathname = '/signup'

    
}
function Login(){
        const [Input,setInput] = useState({
        username: '',
        password: ''
    })
    async function LoginApi(){
        try {
            const response = await fetch('http://localhost:8000/api/login/',{
                method: 'POST',
                headers:{"Content-Type":"application/json",},
                body: JSON.stringify({
                    username: Input.username,
                    password: Input.password,
                })})  
            
            const data = await response.json();  
            console.log(data); 
            localStorage.setItem('access',JSON.stringify(data.TOKEN.access))
            localStorage.setItem('refrech',JSON.stringify(data.TOKEN.refrech))
        } catch (error) {
            console.log(error)
        }
    }
    
    const handleSubmit = (e)=>{
        e.preventDefault();
        LoginApi();
        
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
        }
    }

    
    return (
        <div className='background'>
            <div className='log-form-window'>
                <p className='form-title'>Welcome to Khatamat</p>
                <form onSubmit={handleSubmit}>
                    <input type='text' onChange={handleChange} className='input' placeholder='username' required/>
                    <input type='password' onChange={handleChange} className='input1' placeholder='password' required/>
                    <button type='submit' className='form-submit-but'>Log in</button>
                </form>
                <div className='other-option-div'>
                    <span className='go-to-signup'>
                        don't have an account yet ? &nbsp;<strong onClick={changePath}>Sign up</strong> {/*TODO: link to sign in form*/}
                    </span>
                    <span>
                        &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<strong>Forgot password ?</strong> {/*TODO: link to change password using email */}
                    </span>

                </div>
                
            </div>
        </div>
    );
}
export default Login;