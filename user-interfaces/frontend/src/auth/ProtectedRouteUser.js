import React from "react";
import { Redirect, Route } from "react-router-dom";
import { useState } from "react";
function ProtectedRouteUser({ component: Component, ...restOfProps }) {
  const loggedIn = localStorage.getItem("isAuthenticated");
  console.log("LOGGED IN ???", loggedIn);
  return (
    <Route
      {...restOfProps}
      render={(props) =>
        loggedIn ? <Component {...props} /> : <Redirect to="/" />
      }
    />
  );
}

export default ProtectedRouteUser;
