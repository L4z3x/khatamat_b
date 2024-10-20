import React from 'react';
import { useNavigate } from 'react-router-dom';
import ReactDOM from 'react-dom/client';
import { BrowserRouter as Router ,Route,Routes} from 'react-router-dom';  
import './style/index.css'
import Login from './js/login'
import Navbar from './js/navbar'
import Signup from './js/singup'
import Profile from './js/profile'
import reportWebVitals from './reportWebVitals';
import About from './js/about';
import Home from './js/home';
import NotFound from './js/NotFound';
import ProtectedRoute from './js/ProtectedRoutes';
import Contact from './js/contact';
import FAQs from './js/faqs'; 
import IsAuth from './js/isAuth';
import Logout from './js/logout';
import Khatmat from './js/khatamat';
import Userhome from './js/user-home';
import Leftbar from './js/leftBar';

const root = ReactDOM.createRoot(document.getElementById('root'));
root.render(
  
    <React.StrictMode>
      <Router>
        
        <Routes>
          
          <Route path={'/home'} element={
            <IsAuth>
              <Navbar /><Home />
            </IsAuth>
              
            }/>

          <Route path='Forum' element={
            <IsAuth>
              <Navbar />
            </IsAuth>
            }/>
          <Route path='/' element={
            <IsAuth>
              <Leftbar/><Navbar />
            </IsAuth>
            }/>
          <Route path='/aboutus' element={
            <IsAuth>
              <Navbar /><About />
            </IsAuth>
            }/>

          <Route path='/faqs' element={
            <IsAuth><Navbar /><FAQs /></IsAuth>
            }/>

          <Route path='/contact' element={
            <IsAuth>
              <Navbar /><Contact/>
            </IsAuth>
            }/>

          <Route path='/signup' element={
              <IsAuth><Navbar/><Signup/></IsAuth>
            }/>

          <Route path={'/login'} element={
              <IsAuth><Navbar/><Login/></IsAuth>
            }/>  

          <Route path={'/profile'} element={
            <ProtectedRoute>
              <IsAuth>
                <Navbar/><Profile/>
              </IsAuth>
            </ProtectedRoute>
            }/>  

          <Route path={'*'} element={
            <IsAuth><Navbar /><NotFound /></IsAuth>
            }/>

          <Route path={'/logout'} element={
            <IsAuth>
              <Navbar /><Logout />
            </IsAuth>
            }/>

          <Route path={'/khatamat'} element={
            <IsAuth>
              <Navbar/><Khatmat/>
            </IsAuth>
          }/>            

        </Routes>
      </Router>
    </React.StrictMode>
  
);


// If you want to start measuring performance in your app, pass a function
// to log results (for example: reportWebVitals(console.log))
// or send to an analytics endpoint. Learn more: https://bit.ly/CRA-vitals
reportWebVitals();
