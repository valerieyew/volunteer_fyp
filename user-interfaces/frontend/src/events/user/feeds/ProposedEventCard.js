import { setDayOfYear } from 'date-fns';
import React, { useCallback, useState, useEffect } from 'react';
import { useHistory } from 'react-router-dom';
import LoggedInUser from '../../../apis/LoggedInUser';

function ProposedEventCard({ event: { event_id, name, date, time, info, image_url, status } }) {
  const history = useHistory();
  const handleOnClick = useCallback(() => history.push(`/events/${event_id}`), [history]);

  const [firstSession, setFirstSession] = useState([]);
  const [numSessions, setNumSessions] = useState(0);
  const [displayImage, setDisplayImage] = useState("");

  let displayUrl = displayImage;
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
        console.log(sessions)
        displaySession = sessions[0]
        setFirstSession(displaySession)
        console.log(sDate(displaySession))
        displaySessionDate = sDate(displaySession);
        setDisplayDate(displaySessionDate)
        displaySessionTime = sTime(displaySession);
        setDisplayTime(displaySessionTime)


        otherSessions = sessions.length
        setNumSessions(otherSessions)
        console.log(otherSessions)

        console.log("Getting images...")
        const images = res.data.event.image_url;
        displayUrl = images[0]
        setDisplayImage(displayUrl)
        console.log(displayUrl)
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

    return `${day} ${month} ${year} (${weekday})`;
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
          <div className="relative">
          <img className="w-full h-48 object-cover opacity-50" src={displayImage} alt="" />
          <p className={`${status === 'Pending' ? "absolute inset-0 mx-12 top-16 h-1/3 pt-3 text-3xl bg-yellow-600 rounded-lg p-2 cursor-pointer group text-white font-oswald uppercase font-extrabold" : "hidden"}`}>
            {status}...
          </p>
          <p className={`${status === 'Approved' ? "absolute inset-0 mx-12 top-16 h-1/3 pt-3 text-3xl bg-green-700 rounded-lg p-2 cursor-pointer group text-white font-oswald uppercase font-extrabold" : "hidden"}`}>
            {status}
          </p>
          <p className={`${status === 'Rejected' ? "absolute inset-0 mx-12 top-16 h-1/3 pt-3 text-3xl bg-red-700 rounded-lg p-2 cursor-pointer group text-white font-oswald uppercase font-extrabold" : "hidden"}`}>
            {status}
          </p>
          </div>
          <div className="p-5">
            <h1 className="text-2xl text-left font-oswald font-extrabold uppercase line-clamp-2 h-16">{name}</h1>
            <p className="mt-2 text-left text-lg font-oswald font-medium text-gray-500">Date: {displayDate}</p>
            <p className="text-left text-lg font-oswald font-medium text-gray-500">Time: {displayTime}</p>
            <p className="h-32 mt-2 text-md text-gray-500 text-left line-clamp-5 border-t-2 border-gray-300 py-2">{info}</p>
          </div>
        </div>
        {/* </Link> */}
      </div>
    </button>
  );
  // return (

  //   <div className="flex items-center mx-auto justify-center p-10">
  //     {/* <Link to={`/events/${id}`} /> only works in react v5 */}
  //     <div className=" w-80 bg-white rounded-xl overflow-hidden shadow-lg hover:shadow-xl hover:scale-105 duration-500 transform transition cursor-pointer">
  //       <img className="w-full h-48 object-cover" src={image} alt=""/>
  //       <p class="absolute right-2 top-2 bg-white rounded-full p-2 cursor-pointer group text-gray-600 italic">
  //         {status}
  //         </p>
  //       <div className="p-5">
  //         <h1 className="text-xl font-bold">{name}</h1>
  //         <p className="mt-2 text-md font-semibold text-gray-600">Date: {date}</p>
  //         <p className="mt-2 text-md font-semibold text-gray-600">Time: {time}</p>
  //         <p className="mt-1 text-gray-500 font-">{info.substring(0,70)}...</p>
  //       </div>
  //     </div> 
  //   </div>
  // );
}
export default ProposedEventCard;