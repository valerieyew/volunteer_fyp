// import React, { useState, useEffect } from "react";
// import { BrowserRouter as Router, Switch, Route, Link, useParams, useHistory } from "react-router-dom";
// import LoggedInUser from "../../../apis/LoggedInUser";
// import LoginApi from "../../../apis/LoginApi";
// import Select from 'react-select';
// import locations from "../../../data/locations.json";
// import MapContainer from "./MapContainer";
// import LoggedInTest from "../../../apis/LoggedInTest";
// import axios from "axios";

// function UserEventPage({ event_id }) {

//     // LOGGED IN USER DETAILS //
//     // const userId = userId

//     // EVENT DETAILS //
//     const [name, setName] = useState("");
//     const [info, setInfo] = useState("");
//     const [location, setLocation] = useState("");
//     const [imageUrl, setImageUrl] = useState("");
//     const [regOpenDate, setRegOpenDate] = useState("");
//     const [regCloseDate, setRegCloseDate] = useState("");

//     // SESSION DETAILS //
//     const [allSessions, setAllSessions] = useState([]);
//     const [selectedSession, setSelectedSession] = useState([]);
//     const [options, setOptions] = useState([]);         // List of sessions (displayed in dropdown)

//     const dateNow = new Date();
//     const [regClosedFlag, setRegClosedFlag] = useState(false);

//     const [availability, setAvailability] = useState(-1);
//     let avail = availability;

//     const [enteredLocation, setEnteredLocation] = useState(false);

//     let alreadyEnrolled = false;

//     // LOCATION DETAILS //
//     const [locationOptions, setLocationOptions] = useState([]);     // List of MRT/office locations (displayed in dropdown)
//     const [selectedLocation, setSelectedLocation] = useState("");                 // Location participant selects

//     let chosenSession = selectedSession;
//     let chosenLocation = selectedLocation;


//     useEffect(() => {
//         getEventData();
//         getLocations();
//     }, []);

//     // Fetch event data //
//     const getEventData = () => {

//         console.log("Fetching event data...")

//         new LoggedInUser().get("/events/" + event_id).then(
//             (res) => {
//                 console.log("NORMAL USER VIEW")

//                 console.log("EVENT ID: " + event_id)
//                 const event = res.data.event;
//                 console.log("EVENT DATA:")
//                 console.log(event)

//                 console.log("Getting session info...")

//                 const sessions = res.data.sessions;
//                 console.log("SESSIONS:")
//                 console.log(sessions)

//                 setAllSessions(sessions)

//                 // Session display list
//                 const sessionOptions = sessions.map(s => ({
//                     "value": s.session_id,
//                     "label": createSessionName(s)
//                 }))

//                 console.log("SESSION DISPLAY STRINGS: ")
//                 console.log(sessionOptions)

//                 setImageUrl(event.image_url);
//                 setInfo(event.info);
//                 setLocation(event.location);
//                 setName(event.name);
//                 setRegCloseDate(event.registration_closes_on);
//                 setRegOpenDate(event.registration_opens_on);

//                 setOptions(sessionOptions);

//                 console.log("OPTIONS");
//                 console.log(options);
//                 setRegClosedFlag(new Date(regCloseDate) < dateNow);
//                 // console.log(regClosedFlag)
//                 // const test = new Date(regCloseDate);
//                 // console.log(test);
//                 // console.log(new Date(regCloseDate));
//                 console.log(dateNow);

//             })
//             .catch((err) => {
//                 console.log(err);
//             });
//     }

//     function createSessionName(s) {
//         const start = new Date(s.start_time)
//         const end = new Date(s.end_time)

//         var weekday = start.toLocaleDateString('en-US', { weekday: 'short' })
//         var day = start.toLocaleDateString('en-US', { day: '2-digit' })
//         var month = start.toLocaleDateString('en-US', { month: 'short' })
//         var year = start.toLocaleDateString('en-US', { year: 'numeric' })

//         var start_time = start.toLocaleString('en-US', { hour: 'numeric', minute: 'numeric', hour12: true })
//         var end_time = end.toLocaleString('en-US', { hour: 'numeric', minute: 'numeric', hour12: true })

//         const fill = s.fill
//         const capacity = s.capacity
//         var slots = capacity - fill

//         if (slots == 1) {
//             return `${weekday}, ${day} ${month} ${year}, ${start_time} - ${end_time} (${slots} slot)`;
//         } else {
//             return `${weekday}, ${day} ${month} ${year}, ${start_time} - ${end_time} (${slots} slots)`;
//         }
//     }

//     const getLocations = () => {
//         console.log("Getting pick-up locations...")
//         console.log(locations)
//         const locOptions = locations.map(location => ({
//             "value": location["Station Name"],
//             "label": `${location["Station Name"]} (${location.Station})`
//         }))
//         console.log("LOCATION DISPLAY STRINGS: ")
//         console.log(locOptions)

//         setLocationOptions(locOptions)
//     }

    
//     function handleSessionChange(e) {
//         console.log("CHANGING SESSION:")
//         const thisSession = allSessions.find(s => s.session_id === e.value)
//         console.log(thisSession)

//         chosenSession = thisSession;
//         setSelectedSession(thisSession)
//         console.log(chosenSession)

//         avail = thisSession.capacity - thisSession.fill
//         setAvailability(avail)
//         console.log(avail)
//     }

//     function handleLocationChange(e) {
//         console.log("CHANGING LOCATION:")
//         chosenLocation = e.value;
//         setSelectedLocation(e.value);
//         console.log(chosenLocation)
//         setEnteredLocation(true);
//     }

//     const handleSubmit = (e) => {
//         e.preventDefault();
//         console.log(event_id);
//         console.log(chosenLocation);

//         new LoggedInUser()
//             .post("/events/" + event_id + "/" + chosenSession.session_id, {
//                 point: chosenLocation
//             })
//             .then((res) => {
//                 console.log("SUBMITTED")
//                 console.log(res);
//                 console.log(chosenLocation);
//             })
//             .catch((err) => {
//                 console.log(err);
//             })
//     }


//     return (
//         <form>
//             <div className="flex justify-center pt-32">
//                 <div className="flex-col max-w-5xl">
//                     <div className="flex">
//                         <div className="grid grid-row-4 grid-col-3 bg-purple-300">
//                             <div className="row-span-1 col-span-3 mb-6 text-center font-mont text-[#431903] uppercase text-4xl font-extrabold">{name}</div>
                            
//                             <div className="relative row-span-1 col-span-2 py-2 h-80 w-full">
//                                 <div className="absolute w-full h-full bg-pink-500">

//                                 </div>
//                             </div>

//                             {/* <img className="row-span-1 col-span-2 py-2 object-cover h-96 w-full" src={imageUrl} /> */}
//                             <div className="row-span-1 col-span-1 py-2 px-4 pl-8 flex flex-col text-gray-700 text-lg font-bold">
//                                 <div className="text-gray-700 text-lg font-bold">Location: {location}</div>
//                                 <div className="mt-6 mb-2">
//                                     Select Session:
//                                 </div>
//                                 <Select className="rounded-md text-sm font-medium" options={options}
//                                     onChange={handleSessionChange.bind()}
//                                 />
//                                 <div className="mt-6 mb-2">
//                                     Preferred Pick-Up Location:
//                                 </div>
//                                 <Select className="rounded-md text-sm font-medium" options={locationOptions}
//                                     onChange={handleLocationChange.bind()}
//                                 />

//                                 <button type="submit"
//                                     className={availability > 0 & enteredLocation === true ? "mt-6 bg-blueGray-800 text-white active:bg-blueGray-600 text-sm font-bold uppercase px-6 py-3 rounded shadow hover:shadow-lg outline-none focus:outline-none mr-1 mb-1 w-full ease-linear transition-all duration-150"
//                                         : "hidden"}
//                                     onClick={handleSubmit.bind()}
//                                 >
//                                     Volunteer!
//                                 </button>

//                                 <div className={availability === -1 ? "cursor-not-allowed mt-6 bg-blueGray-200 text-center text-white text-sm tfont-bold uppercase px-6 py-3 rounded shadow outline-none mr-1 mb-1 w-full ease-linear transition-all duration-150"
//                                         : "hidden"}
//                                 >
//                                     Please select a session
//                                 </div>

//                                 <div className={availability > 0 & enteredLocation === false ? "cursor-not-allowed mt-6 bg-blueGray-200 text-center text-white text-sm tfont-bold uppercase px-6 py-3 rounded shadow outline-none mr-1 mb-1 w-full ease-linear transition-all duration-150"
//                                         : "hidden"}
//                                 >
//                                     Please select a Pick-Up Location
//                                 </div>

//                                 <div className={availability === 0 ? "cursor-not-allowed mt-6 bg-blueGray-200 text-center text-white text-sm tfont-bold uppercase px-6 py-3 rounded shadow outline-none mr-1 mb-1 w-full ease-linear transition-all duration-150"
//                                         : "hidden"}
//                                 >
//                                     Session filled
//                                 </div>
//                             </div>
//                             <div className="row-span-1 col-span-3 mt-4 text-justify text-gray-700 text-md font-bold">{info}</div>
//                         </div>
//                     </div>
//                 </div>
//             </div>
//         </form>
//     )
// }

// export default UserEventPage;