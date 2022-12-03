import React, { useState } from 'react';
import { BrowserRouter as Router, Route, Switch } from 'react-router-dom';
import UserHeader from "./UserHeader";
import BrowseEvents from "../../events/user/feeds/BrowseEvents";
import EnrolledEvents from "../../events/user/feeds/EnrolledEvents";
import ProposedEvents from "../../events/user/feeds/ProposedEvents";
import EventPage from '../../events/user/details/EventPage';
import ProposeNewEvent from "../../events/user/feeds/ProposeNewEvent";
import EditEvent from '../../events/user/details/EditEvent';


const UserNav = () => {
  
  // Toggle for header sections
  const [browseSelected, setBrowseSelected] = useState(true);
  const [enrolledSelected, setEnrolledSelected] = useState(false);
  const [proposedSelected, setProposedSelected] = useState(false);
  const [proposeNewSelected, setProposeNewSelected] = useState(false);

  const toggleBrowse = () => {
    setBrowseSelected(true);
    setEnrolledSelected(false);
    setProposedSelected(false);
    setProposeNewSelected(false);
  };

  const toggleEnrolled = () => {
    setBrowseSelected(false);
    setEnrolledSelected(true);
    setProposedSelected(false);
    setProposeNewSelected(false);
  };

  const toggleProposed = () => {
    setBrowseSelected(false);
    setEnrolledSelected(false);
    setProposedSelected(true);
    setProposeNewSelected(false);
  };

  const toggleProposeNew = () => {
    setBrowseSelected(false);
    setEnrolledSelected(false);
    setProposedSelected(false);
    setProposeNewSelected(true);
  };

  return (
    <Router>
      <UserHeader
        toggleBrowse={toggleBrowse}
        toggleEnrolled={toggleEnrolled}
        toggleProposed={toggleProposed}
        toggleProposeNew={toggleProposeNew}
        browseSelected={browseSelected}
        enrolledSelected={enrolledSelected}
        proposedSelected={proposedSelected}
        proposeNewSelected={proposeNewSelected}
      />

      <Switch>
        <Route exact path="/home">
          <BrowseEvents />
        </Route>
        <Route exact path="/browse">
          <BrowseEvents />
        </Route>
        <Route exact path="/enrolled">
          <EnrolledEvents />
        </Route> 
        <Route exact path="/proposed">
          <ProposedEvents />
        </Route>
        <Route exact path="/new">
          <ProposeNewEvent />
        </Route> 
        <Route exact path="/edit/:id">
          <EditEvent />
        </Route> 
        <Route exact path="/events/:id">
          <EventPage />
        </Route> 
      </Switch>
    </Router>
  );
};

export default UserNav;