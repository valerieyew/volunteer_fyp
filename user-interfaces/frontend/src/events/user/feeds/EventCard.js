// import { BrowserRouter as Link } from "react-router-dom";
import { setDayOfYear } from 'date-fns';
import React, { useCallback, useState, useEffect } from 'react';
import { useHistory } from 'react-router-dom';
import LoggedInUser from '../../../apis/LoggedInUser';


function EventCard({ event: { event_id, name, date, time, info, image_url } }) {
  const history = useHistory();
  const handleOnClick = useCallback(() => history.push(`/events/${event_id}`), [history]);
  console.log("IMAGE URL " , image_url);
  const [firstSession, setFirstSession] = useState([]);
  const [numSessions, setNumSessions] = useState(0);
  // const [displayImage, setDisplayImage] = useState("");
  // let displayUrl = displayImage;
  let displaySession = firstSession;
  let otherSessions = numSessions;

  const [displayDate, setDisplayDate] = useState("");
  let displaySessionDate = "";

  const [displayTime, setDisplayTime] = useState("");
  let displaySessionTime = "";


  const getEventData = () => {

    console.log("Fetching event data...")

    new LoggedInUser().get("/events/" + event_id).then(
      (res) => {
        console.log("GETTING EVENT INFO")
        console.log(res.data.sessions)

        const sessions = res.data.sessions;
        console.log("SESSIONS:")
        console.log(sessions.length)
        displaySession = sessions[0]
        setFirstSession(displaySession)
        console.log(sDate(displaySession))
        displaySessionDate = sDate(displaySession);
        setDisplayDate(displaySessionDate)
        displaySessionTime = sTime(displaySession);
        setDisplayTime(displaySessionTime)


        otherSessions = sessions.length - 1
        setNumSessions(otherSessions)
        console.log(otherSessions)

        // console.log("Getting images...")
        // const images = res.data.event.image_url;
        // displayUrl = images[0]
        // setDisplayImage(displayUrl)
        // console.log(displayUrl)
      })
      .catch((err) => {
        console.log(err);
      });
  }

  useEffect(() => {
    getEventData();
  }, []);

  function sDate(s) {
    const start = new Date(s.start_time)

    var weekday = start.toLocaleDateString('en-US', { weekday: 'long' })
    var day = start.toLocaleDateString('en-US', { day: '2-digit' })
    var month = start.toLocaleDateString('en-US', { month: 'long' })
    var year = start.toLocaleDateString('en-US', { year: 'numeric' })

    var start_time = start.toLocaleString('en-US', { hour: 'numeric', minute: 'numeric', hour12: true })

    if (numSessions > 0) {
      return `${day} ${month} ${year} (${weekday}) (+ ${numSessions} more)`;
    } else {
      return `${day} ${month} ${year} (${weekday})`;
    }
  }

  function sTime(s) {
    const start = new Date(s.start_time)
    const end = new Date(s.end_time)

    var start_time = start.toLocaleString('en-US', { hour: 'numeric', minute: 'numeric', hour12: true })
    var end_time = end.toLocaleString('en-US', { hour: 'numeric', minute: 'numeric', hour12: true })

    return `${start_time} - ${end_time}`;
  }

  return (
    <button type="button" onClick={handleOnClick}>
      <div className="flex">
        {/* <Link to={`/events/${id}`} /> only works in react v5 */} {/* TO BE ADDED LATER */}
        <div className="h-auto w-96 bg-white font-roboto text-gray-900 rounded-xl overflow-hidden border-2 border-gray-300 hover:shadow-xl hover:scale-105 duration-500 transform transition cursor-pointer">
          <img className="w-full h-48 object-cover" src={image_url[0]} alt="" />
          <div className="p-5">
            <h1 className="text-2xl text-left font-oswald font-extrabold uppercase line-clamp-2 h-16">{name}</h1>
            <p className="w-full text-left text-lg font-oswald font-medium text-gray-500">Date: {displayDate}</p>
            <p className="w-full text-left text-lg font-oswald font-medium text-gray-500">Time: {displayTime}</p>
            <p className="h-32 mt-2 text-md text-gray-500 text-left line-clamp-5 border-t-2 border-gray-300 py-2">{info}</p>
          </div>
        </div>
        {/* </Link> */}
      </div>
    </button>
  );
}
export default EventCard;