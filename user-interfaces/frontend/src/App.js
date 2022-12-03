import './App.css';
import { BrowserRouter as Router, Route, Switch } from 'react-router-dom';
import Login from './auth/Login';
import UserNav from './accounts/user/UserNav';
import AdminNav from './accounts/admin/AdminNav';
import AdminLoginSuccess from './auth/AdminLoginSuccess';
import UserLoginSuccess from './auth/UserLoginSuccess';
import EventPage from './events/user/details/EventPage';
import Nav from './accounts/admin/AdminHeader';
import UserHeaderNEW from './accounts/user/UserHeader';
import PostContainer from './events/user/community/PostContainer';
import NotFound from './events/NotFound';
import { Redirect } from 'react-router-dom';
import { useState } from 'react';
import ProtectedRouteUser from './auth/ProtectedRouteUser';
import ProtectedRouteAdmin from './auth/ProtectedRouteAdmin';
import { useEffect } from 'react';


function App() {

  return (
    
    <Router>
      <Switch>
        <Route path="/" exact component={Login} />
        {/* <Route path="/login/user" component={UserLoginSuccess} /> */}
        <ProtectedRouteUser path="/browse" component={UserNav} />
        <ProtectedRouteUser path="/enrolled" component={UserNav} />
        <ProtectedRouteUser path="/proposed" component={UserNav} />
        <ProtectedRouteUser path="/new" component={UserNav} />
        <ProtectedRouteUser path="/events/:id" component={UserNav} />
        <ProtectedRouteUser path="/edit/:id" component={UserNav} />
        
        <ProtectedRouteAdmin path="/admin/home" component={AdminNav} />
        <ProtectedRouteAdmin path="/admin/events/:id" component={AdminNav} />

        <Route component={NotFound} />

        {/* <Route path="/events/:id">
          <EventPage />
        </Route>  */}

      </Switch>
    </Router>

    // For V6:
    // <Router>
    //   <Routes>
    //     <Route exact path="/login" element={<Login />}/>
    //     <Route exact path="/login/success" element={<TestSuccess />}/>
    //     <Route exact path="/home" element={<Home />}/>
    //   </Routes>
    // </Router>
  );
}

export default App;
