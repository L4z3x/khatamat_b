import api from "../api";
import { Navigate} from "react-router-dom";
import {jwtDecode} from 'jwt-decode';
import { ACCESS_TOKEN,REFRESH_TOKEN } from "../constants";
import { useState,useEffect } from "react";
import Login from "./login";

export default function ProtectedRoute ({children}) {

    const [IsAuthorized,setIsAuthorized] = useState(null)
    useEffect(()=>{
        auth()
    },[])
    const refrechToken = async () => {
        const refresh = localStorage.getItem(REFRESH_TOKEN)
        console.log(refresh)
        if (!refresh) {
            setIsAuthorized(false)
            console.log("no refresh")
            return 
        } else {
            console.log("there is a refresh")
            try {
                const res = await api.post("/api/token/refresh/", { refresh: refresh, 
                });
                if (res.status === 200) {
                    localStorage.setItem(ACCESS_TOKEN, res.data.access)
                    setIsAuthorized(true)
                } else {
                    setIsAuthorized(false)
                }

            } catch (error) {
                setIsAuthorized(false);
                console.log(error)
            }
        }
        
        
        
        
    }

    const auth = async () => {
        const token = localStorage.getItem(ACCESS_TOKEN);
        //console.log(token)
        if (!token) {
            setIsAuthorized(false);
            return refrechToken()
        }
        const decoded = jwtDecode(token);
        const tokenExp = decoded.exp ;
        const now = Date.now() / 100 ;
        //console.log(tokenExp,now)
        if (tokenExp > now) {
            setIsAuthorized(true) ;
            return
        }else{
           // console.log('expired token')
            await refrechToken();
        }
    }

    if (IsAuthorized === null){
        return <div>Loading...</div>
    }
    if (children === '<Login />') {
        console.log('navigating to login')
      return  IsAuthorized ? <Navigate to="/home" /> : <Login />
    }
    return IsAuthorized ? children : <Navigate to='/login' />
}