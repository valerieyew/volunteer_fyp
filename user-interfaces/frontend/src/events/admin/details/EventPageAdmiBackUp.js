// import React, { useState, useEffect } from "react";
// import { BrowserRouter as Router, Switch, Route, Link, useParams, useHistory } from "react-router-dom";
// import LoggedInAdmin from "../../../apis/LoggedInAdmin";
// import Select from 'react-select';

// function EventPageAdmin() {

//     let { id } = useParams();
//     let history = useHistory();

//     const [sessionsLoaded, setSessionsLoaded] = useState(false);

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

//     const [sessions, setSessions] = useState([]);
//     const [options, setOptions] = useState([]);
//     const [chosenId, setChosenId] = useState("");
//     const [chosenDate, setChosenDate] = useState("");

//     // const [sessionId, setSessionId] = useState(0);
//     // const [startTime, setStartTime] = useState("");
//     // const [endTime, setEndTime] = useState("");
//     const [capacity, setCapacity] = useState(0);
//     const [fill, setFill] = useState(0);

//     const getEventData = () => {
//         console.log("getting event data")
//         new LoggedInAdmin().get("/events/" + id).then(
//             (res) => {
//                 console.log(res)
//                 const event = res.data.event;

//                 setSessions(res.data.sessions);
//                 // const sessions = res.data.sessions;
//                 console.log(sessions);
//                 const sessionOptions = sessions.map(s => ({
//                     "value" : s.session_id,
//                     "label" : s.end_time
//                 }))

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
//             })
//             .catch((err) => {
//                 console.log(err);
//             });

//     }

//     useEffect(() => {
//         getEventData();
//         return () => {
//             setState({}); // This worked for me
//         };
//     }, []);

//     function handleChange(e) {
//         setChosenId(e.value);
//         setChosenDate(e.label);
//         updateSelectedSession(findSession(sessions, e.value));
//     }

//     function findSession(sessions, id) {
//         return sessions.find((e) => {
//             return e.session_id === id;
//         })
//     }

//     function updateSelectedSession(s) {
//         setCapacity(s.capacity);
//         setFill(s.fill);
//     }

//     function handleApprove() {
//         new LoggedInAdmin().patch(`/events/${eventId}/approve`).then(
//           (res) => {
//             console.log(res)
//             console.log(eventId)
//             history.push('/admin/home')
//           })
//       }

//     return (
//       // <form onSubmit={this.handleSubmit}>
//       <div className="flex justify-center pt-32">
//         <div className="flex-col max-w-5xl">
//           <div className="flex">
//             <div className="grid grid-row-4 grid-col-3">
//               <div className="row-span-1 col-span-3 mb-6 text-center text-gray-700 capitalize text-4xl font-extrabold">
//                 {name}
//               </div>
//               <img
//                 className="row-span-1 col-span-2 py-2 object-cover h-96 w-full"
//                 src={imageUrl}
//               />
//               <div className="row-span-1 col-span-1 py-2 px-4 flex flex-col text-gray-700 text-lg font-bold">
//                 <div className="text-gray-700 text-lg font-bold">
//                   Location: {location}
//                 </div>
//                 <div className="mt-6 mb-2">Select Session:</div>
//                 <Select
//                   className="rounded-md  font-medium"
//                   options={options}
//                   onChange={handleChange.bind()}
//                 />
//                 <div className="mt-6 text-gray-700 text-lg font-bold">
//                   Vacancies: {fill}/{capacity}
//                 </div>
//               </div>
//               <div className="row-span-1 col-span-3 mt-4 text-justify text-gray-700 text-md font-bold">
//                 {info}
//               </div>
//             </div>
//           </div>
    
//           <button class={`${status === 'Pending' ? "bg-green-400 hover:bg-blue-700 text-white font-bold py-2 px-4 mt-5 ml-4 rounded-full w-1/5" : "hidden"}`} 
//               onClick={handleApprove} > 
//                 Approve
//           </button>
//               <button class={`${status === 'Pending' ? "bg-red-500 hover:bg-blue-700 text-white font-bold py-2 px-4 mt-5 ml-4 rounded-full w-1/5" : "hidden"}`} >
//                 Reject
//               </button>
//         </div>
//       </div>
//       // </form>
//     );
// }

// export default EventPageAdmin;