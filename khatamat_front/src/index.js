import React from 'react';
import { useNavigate } from 'react-router-dom';
import ReactDOM from 'react-dom/client';
import { BrowserRouter as Router ,Route,Routes} from 'react-router-dom';  
import './style/index.css'
import Login from './js/login'
import Navbar from './js/navbar'
import Signup from './js/singup'
import Profile from './js/profile'
import DashBoard from './js/dashboard'; 
import reportWebVitals from './reportWebVitals';
import About from './js/about';
import Home from './js/home';
import NotFound from './js/NotFound';
import ProtectedRoute from './js/ProtectedRoutes';
import { ACCESS_TOKEN, REFRESH_TOKEN } from './constants';


function Logout(){
  localStorage.clear();
  return <Login />
}
const root = ReactDOM.createRoot(document.getElementById('root'));
root.render(
  
    <React.StrictMode>
      <Router>
        <Navbar />
        <Routes>
          
          <Route path='/dashboard' element={
            <ProtectedRoute>
              <DashBoard />
            </ProtectedRoute>
          }/>

          <Route path='/home' element={
              <><Home/></>
            }/>

          <Route path='/aboutus' element={
            <About />
          }/>

          <Route path='/signup' element={
              <Signup/>
          }/>

          <Route path={'/login'} element={
              <Login/>
            }/>  

          <Route path={'/profile'} element={
            <ProtectedRoute>
              <Profile/>
            </ProtectedRoute>
          }/>  

          <Route path={'*'} element={
            <ProtectedRoute>
            <><Navbar /><NotFound /></>
            </ProtectedRoute>
          }/> 
          <Route path={'/logout'} element={
            <Logout />
          }/>
        </Routes>
      </Router>
    </React.StrictMode>
  
);


// If you want to start measuring performance in your app, pass a function
// to log results (for example: reportWebVitals(console.log))
// or send to an analytics endpoint. Learn more: https://bit.ly/CRA-vitals
reportWebVitals();
