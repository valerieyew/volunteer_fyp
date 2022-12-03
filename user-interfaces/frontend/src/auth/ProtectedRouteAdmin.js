import React from "react";
import { Redirect, Route } from "react-router-dom";
import { useState } from "react";
function ProtectedRouteAdmin({ component: Component, ...restOfProps }) {
  const loggedIn = localStorage.getItem("isAuthenticatedAdmin");
  console.log("LOGGED IN ADMIN ???", loggedIn);
  return (
    <Route
      {...restOfProps}
      render={(props) =>
        loggedIn ? <Component {...props} /> : <Redirect to="/" />
      }
    />
  );
}

export default ProtectedRouteAdmin;
