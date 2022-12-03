// import React, { useState, useEffect } from "react";
// import { BrowserRouter as Router, Switch, Route, Link, useParams, useHistory } from "react-router-dom";
// import LoggedInUser from "../../../apis/LoggedInUser";
// import LoginApi from "../../../apis/LoginApi";
// import Select from 'react-select';
// import locations from "../../../data/locations.json";
// import MapContainer from "./MapContainer";
// import LoggedInTest from "../../../apis/LoggedInTest";
// import axios from "axios";

// function EventPage() {

//     let { id } = useParams();

//     // LOGGED IN USER DETAILS //
//     const [userId, setUserId] = useState(0)
//     let user_id = userId

//     // EVENT DETAILS //
//     const [state, setState] = useState({});
//     const [eventId, setEventId] = useState(0);
//     const [name, setName] = useState("");
//     const [info, setInfo] = useState("");
//     const [location, setLocation] = useState("");
//     const [imageUrl, setImageUrl] = useState("");
//     const [status, setStatus] = useState("");
//     const [regOpenDate, setRegOpenDate] = useState("");
//     const [regCloseDate, setRegCloseDate] = useState("");
//     const [employeeId, setEmployeeId] = useState(0);
//     const [proposalDetails, setProposalDetails] = useState("");

//     // SESSION DETAILS //
//     const [allSessions, setAllSessions] = useState([]);
//     const [selectedSession, setSelectedSession] = useState([]);
//     const [options, setOptions] = useState([]);         // List of sessions (displayed in dropdown)

//     const dateNow = new Date();
//     const [regClosedFlag, setRegClosedFlag] = useState(false);

//     const [locationOptions, setLocationOptions] = useState([]);     // List of MRT/office locations (displayed in dropdown)
//     const [selectedLocation, setSelectedLocation] = useState("");                 // Location participant selects

//     let chosenSession = selectedSession;
//     let chosenLocation = selectedLocation;

//     let isAdmin = false;
//     let isOrganiser = false;
//     let alreadyEnrolled = false;

//     const [availability, setAvailability] = useState(-1); 
//     let avail = availability;

    
//     // Check if user is admin/organiser //
//     const checkUser = () => {
//         console.log("getting user type...")
//         new LoggedInTest().get("/accounts/0")
//             .then((res) => {
//                 user_id = res.data.data.account.employee_id
//                 setUserId(res.data.data.account.employee_id)
//                 console.log("USER'S ID: " + user_id)

//                 if (userId == employeeId) {
//                     isOrganiser = true
//                     console.log("IS ORGANISER")
//                 } 
//             })
//             .catch((err) => {
//                 console.log(err);
//             });
//     }


//     // const locations = [
//     //     {
//     //       id: 1,
//     //       name: "Jurong East MRT Station (NS1/EW24)",
//     //       location: { 
//     //         lat: 41.3954,
//     //         lng: 2.162 
//     //       },
//     //     },
//     //     {
//     //       id: 2,
//     //       name: "Pioneer MRT Station (EW28)",
//     //       location: { 
//     //         lat: 41.3917,
//     //         lng: 2.1649
//     //       },
//     //     },
//     //     {
//     //       id : 3,
//     //       name: "Clementi MRT Station (EW23)",
//     //       location: { 
//     //         lat: 41.3773,
//     //         lng: 2.1585
//     //       },
//     //     },
//     //     {
//     //       id: 4,
//     //       name: "Buona Vista MRT Station (CC22)",
//     //       location: { 
//     //         lat: 41.3797,
//     //         lng: 2.1682
//     //       },
//     //     },
//     //     {
//     //       id: 5,
//     //       name: "Paya Lebar MRT Station (EW7)",
//     //       location: { 
//     //         lat: 41.4055,
//     //         lng: 2.1915
//     //       },
//     //     }
//     //   ];
//     // const locationsList = locations.map((location) =>  
//     //   <li>{location.name}</li>  
//     // );  

//     // Fetch event data //
//     const getEventData = () => {

//         console.log("Fetching event data...")

//         new LoggedInUser().get("/events/" + id).then(
//             (res) => {
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

//                 setEmployeeId(event.employee_id);
//                 setEventId(event.event_id);
//                 setImageUrl(event.image_url);
//                 setInfo(event.info);
//                 setLocation(event.location);
//                 setName(event.name);
//                 setProposalDetails(event.proposal_details);
//                 setRegCloseDate(event.registration_closes_on);
//                 setRegOpenDate(event.registration_opens_on);
//                 setStatus(event.status);

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

//     useEffect(() => {
//         checkUser();
//         getEventData();
//         getLocations();
//     }, []);


//     function handleSessionChange(e) {
//         console.log("CHANGING SESSION:")
//         const thisSession = allSessions.find(s => s.session_id == e.value)
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
//     }

//     const handleSubmit = (e) => {
//         e.preventDefault();
//         console.log(id);
//         console.log(chosenLocation);

//         new LoggedInUser()
//             .post("/events/" + id + "/" + chosenSession.session_id, {
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
//                         <div className="grid grid-row-4 grid-col-3">
//                             <div className="row-span-1 col-span-3 mb-6 text-center text-gray-700 capitalize text-4xl font-extrabold">{name}</div>
//                             <img className="row-span-1 col-span-2 py-2 object-cover h-96 w-full" src={imageUrl} />
//                             <div className="row-span-1 col-span-1 py-2 px-4 flex flex-col text-gray-700 text-lg font-bold">
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
//                                     className={ availability > 0 ? "mt-6 bg-blueGray-800 text-white active:bg-blueGray-600 text-sm font-bold uppercase px-6 py-3 rounded shadow hover:shadow-lg outline-none focus:outline-none mr-1 mb-1 w-full ease-linear transition-all duration-150"
//                                     : "hidden"}
//                                     onClick={handleSubmit.bind()}
//                                 >
//                                     Volunteer!
//                                 </button>

//                                 <div
//                                     className={ availability === -1 ? "cursor-not-allowed mt-6 bg-blueGray-200 text-center text-white text-sm tfont-bold uppercase px-6 py-3 rounded shadow outline-none mr-1 mb-1 w-full ease-linear transition-all duration-150" 
//                                     : "hidden" }
//                                 >
//                                     Please select a session
//                                 </div>

//                                 <div
//                                     className={ availability === 0 ? "cursor-not-allowed mt-6 bg-blueGray-200 text-center text-white text-sm tfont-bold uppercase px-6 py-3 rounded shadow outline-none mr-1 mb-1 w-full ease-linear transition-all duration-150" 
//                                     : "hidden" }
//                                 >
//                                     Session filled
//                                 </div>


//                             </div>
//                             <div className="row-span-1 col-span-3 mt-4 text-justify text-gray-700 text-md font-bold">{info}</div>
//                         </div>
//                     </div>

//                     <div className={`${new Date(regCloseDate) < new Date() ? "rounded-md text-sm font-medium mt-5" : "hidden"}`}>
//                         Route:
//                         <ol className="list-decimal">
//                             {locations.map(location => <li>{location.name}</li>)}
//                         </ol>

//                     </div>
//                     <MapContainer />
//                 </div>
//             </div>
//         </form>
//     )
// }

// export default EventPage;