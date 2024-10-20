import React, { useState } from "react"
import api from "../api"
import "../style/khatamat.css";
import { ACCESS_TOKEN } from "../constants";

function Khatamat(){
    const [file,setFile] = useState()
    async function handleCreatingKhatma () {
        try {
            const res = await api.post('/khatma/create/',
                {
                    "G_name":"gr2",
                    "name":"k1",
                    "period":"4"
                }
            )
            console.log(res) 
        } catch(error){
            console.log(error)
        }
                  
    }
    async function handleAddingMember_kg() {
        try{
            const res = await api.post('khatma/add-member-kg/',
                {
                    "G_name": "gr6",
                    "username": "moussa2"
                }
            )
            console.log(res.status)
        }catch(error){
            console.log(error)
        }
        
    }
    async function handleCreatingKhatmaGroup (e) {
        e.preventDefault()
        console.log(e.target)
        const data = new FormData();
        if (file) {
            data.append("icon",file)
        }
        data.append("name","gr2")
        try {
            const res = await api.post('/khatma/create-khatma-group/',data)
            console.log(res.status) 
        } catch(error){
            console.log(error)
        }
                  
    }
    const handleImg = (e) => {
        e.preventDefault();
        setFile(e.target.files[0])
        // const formData = new FormData(form);
        // console.log(formData)
        console.log(file)
    }
    async function handleJoinRequest () {
        try{    
            const res = await api.post('/api/join-request/',
            {
                "G_name":"gr6"
            },
        )
        console.log(res.status)
        }catch(error){
            console.log(error);
        }
       
    } 
    async function handleAddingMember_k () {
        try {
            const res = await api.post('/khatma/add-member-k/',
                {
                    "G_name":"gr6",
                    "KH_name":"k12"
                }
            )
            console.log(res.status,res.statusText) 
        } catch(error){
            console.log(error)
        }
                  
    }
    async function getkhatmaGoups() {
        try{
            // const res = await api.get('/khatma/create/')
            console.log("fetching")
            const token = localStorage.getItem(ACCESS_TOKEN);
            console.log(token)
            const res = await fetch("http://localhost:8000/khatma/create/",
                {
                    method: "GET",
                    headers:{
                        Authorization: `Bearer ${token}`,
                        // contentType: 'application/json'
                    }
                }
            )
            console.log(res.status)
            const data = await res.json();
            console.log(data)
        }catch(error){
            console.log(error)
        }
    }
    return(
    
      <div className="khatamat-container">
        <button onClick={handleCreatingKhatma}>create khatma</button>
        <button onClick={handleCreatingKhatmaGroup}>create khatmaGroup</button>
        <button onClick={handleJoinRequest}>send joinRequest</button>
        <button onClick={handleAddingMember_kg}>accept joinRequest</button>
        <button onClick={handleAddingMember_k}>add member to khatma</button>
        <button onClick={getkhatmaGoups}>get khatma</button>
        <form>
        <input name="file" type="file" onChange={handleImg}/>
        <button type="submit">Upload</button>
        </form>
        </div>  
    );
}
export default Khatamat