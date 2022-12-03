import { BrowserRouter as Router, Route, Switch } from 'react-router-dom';
import AdminHeader from './AdminHeader';
import { useState } from 'react';
import PendingEvents from '../../events/admin/feeds/PendingEvents';
import ApprovedEvents from '../../events/admin/feeds/ApprovedEvents';
import RejectedEvents from '../../events/admin/feeds/RejectedEvents';
import EventPageAdmin from '../../events/admin/details/EventPageAdmin - old';
import Nav from './AdminHeader';
const AdminNav = () => {

  // Toggle for header sections
  const [pendingSelected, setPendingSelected] = useState(true);
  const [approvedSelected, setApprovedSelected] = useState(false);
  const [rejectedSelected, setRejectedSelected] = useState(false);


  const togglePending = () => {
    setPendingSelected(true);
    setApprovedSelected(false);
    setRejectedSelected(false);
  };

  const toggleApproved = () => {
    setPendingSelected(false);
    setApprovedSelected(true);
    setRejectedSelected(false);
  };

  const toggleRejected = () => {
    setPendingSelected(false);
    setApprovedSelected(false);
    setRejectedSelected(true);
  };

  return (
    <Router>
      <AdminHeader
        togglePending={togglePending}
        toggleApproved={toggleApproved}
        toggleRejected={toggleRejected}
        pendingSelected={pendingSelected}
        approvedSelected={approvedSelected}
        rejectedSelected={rejectedSelected}
      />

      <Switch>
        <Route exact path="/admin/home">
          <PendingEvents />
        </Route>
        <Route exact path="/admin/pending">
          <PendingEvents />
        </Route>
        <Route exact path="/admin/approved">
          <ApprovedEvents />
        </Route>
        <Route exact path="/admin/rejected">
          <RejectedEvents />
        </Route>
        <Route path="/admin/events/:id">
          <EventPageAdmin />
        </Route> 
      </Switch>
    </Router>
  );
};

export default AdminNav;