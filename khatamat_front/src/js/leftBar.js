import "../style/leftBar.css"
import React from 'react';
import { ACCESS_TOKEN } from "../constants";
import { useState } from "react";

export default function Leftbar () {
    const [gr,setGr] = useState([])
    async function handleGetGroups() {
        const token = localStorage.getItem(ACCESS_TOKEN)
        try{
            const res = await fetch ("http://localhost:8000/katma/create",{
                method: 'GET',
                headers: {
                    Authorization: `Bearer ${token}`
                }
            })
            const data = await res.json()
            console.log(data)
            setGr(data)
        }catch(error){
            console.log(error)
        }
        
            
    }

return (
<div className="lefBar-container">
    <div className="box">
        <div className="btns-box">
            <div>Home</div> 
            <div>Profile</div>
        </div>
    </div>
    <div className="box">
        <div className="btns-box">
            <div>Settings</div> 
            <div>Logout</div>
        </div>
    </div>
    <div className="box">
        <div className="btns-box">
            <div>Contact</div> 
            <div>Help</div>
        </div>
    </div>
    <div className="box">
        <div className="btns-box">
            <div>Additional</div> 
            <div>Content</div>
        </div>
    </div>
    
</div>

)
}
