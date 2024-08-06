import React from "react";
import { REFRESH_TOKEN } from "../constants";
import { ACCESS_TOKEN } from "../constants";
import api from "../api";
import { useState,useEffect } from "react";
import {jwtDecode} from 'jwt-decode';



function IsAuth ({children}) {
    const [IsAuthorized,setIsAuthorized] = useState(null);
    useEffect(()=>{
        auth();
    })
    const refreshToken = async () => {
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
        console.log(token)
        if (!token) {
            setIsAuthorized(false);
            return refreshToken()
        }
        const decoded = jwtDecode(token);
        const tokenExp = decoded.exp ;
        const now = Date.now() / 1000 ;
        //console.log(tokenExp,now)
        if (tokenExp > now) {
            setIsAuthorized(true) ;
            return
        }else{
           // console.log('expired token')
            await refreshToken();
        }
    }
    if (IsAuthorized === null){
        return 
    }
    return (<>
        {React.Children.map(children, child =>
        React.cloneElement(child, { loggedIn: IsAuthorized.toString() })
      )}
        </>
    );
}
export default IsAuth;