import React, { useState, useEffect } from "react";
import { BrowserRouter as Router, Switch, Route, Link, useParams, useHistory } from "react-router-dom";
import LoggedInAdmin from "../../../apis/LoggedInAdmin";
import Select from 'react-select';
// import OrgEventPage from "../../user/details/OrgEventPage";
import AdminEventPage from "./AdminEventPage";

function EventPageAdmin() {

  let { id } = useParams();
  let history = useHistory();

  // const [sessionsLoaded, setSessionsLoaded] = useState(false);

  // const [state, setState] = useState({});
  // const [eventId, setEventId] = useState(0);
  // const [name, setName] = useState("");
  // const [info, setInfo] = useState("");
  // const [location, setLocation] = useState("");
  // const [imageUrl, setImageUrl] = useState("");
  // const [status, setStatus] = useState("");
  // const [regOpenDate, setRegOpenDate] = useState("");
  // const [regCloseDate, setRegCloseDate] = useState("");
  // const [employeeId, setEmployeeId] = useState(0);
  // const [proposalDetails, setProposalDetails] = useState("");

  // const [sessions, setSessions] = useState([]);
  // const [options, setOptions] = useState([]);
  // const [chosenId, setChosenId] = useState("");
  // const [chosenDate, setChosenDate] = useState("");

  // // const [sessionId, setSessionId] = useState(0);
  // // const [startTime, setStartTime] = useState("");
  // // const [endTime, setEndTime] = useState("");
  // const [capacity, setCapacity] = useState(0);
  // const [fill, setFill] = useState(0);

  const getEventData = () => {
    console.log("getting event data")
    new LoggedInAdmin().get("/events/" + id).then(
      (res) => {
        const event = res.data.event;
      })
      .catch((err) => {
        console.log(err);
      });

  }

  useEffect(() => {
    getEventData();
  }, []);



  return (
    <div>
      <AdminEventPage event_id={id} />
    </div>
  );
}

export default EventPageAdmin;