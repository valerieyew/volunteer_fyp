import React, { useState, useEffect } from "react";
import { BrowserRouter as Router, Switch, Route, Link, useParams, useHistory } from "react-router-dom";
import LoggedInUser from "../../../apis/LoggedInUser";
import LoginApi from "../../../apis/LoginApi";
import Select from 'react-select';
import locations from "../../../data/locations.json";
import MapContainer from "./MapContainer";
import LoggedInTest from "../../../apis/LoggedInTest";
import axios from "axios";
import PostContainer from "../community/PostContainer";

function UserEventPage({ event_id, all_posts }) {
    // console.log("USER: ", userId);
    const [userId, setUserId] = useState("");
    // let user_id = String(userId);
    // LOGGED IN USER DETAILS //
    // const userId = userId
    // let userId = user_id;
    // EVENT DETAILS //
    const [name, setName] = useState("");
    const [info, setInfo] = useState("");
    const [location, setLocation] = useState("");
    // const [imageUrl, setImageUrl] = useState("");
    const [regOpenDate, setRegOpenDate] = useState("");
    const [regCloseDate, setRegCloseDate] = useState("");
    const [isParticipant, setIsParticipant] = useState(false);


    // SESSION DETAILS //
    const [allSessions, setAllSessions] = useState([]);
    const [selectedSession, setSelectedSession] = useState([]);
    const [options, setOptions] = useState([]);         // List of sessions (displayed in dropdown)
    const [availOptions, setAvailOptions] = useState([]);         // List of sessions (displayed in dropdown)
    const [enrolledIds, setEnrolledIds] = useState([]);
    const [enrolledSessions, setEnrolledSessions] = useState([]);
    const [enrolledStrings, setEnrolledStrings] = useState([]);

    // ATTENDANCE DETAILS //
    const [myAttendance, setMyAttendance] = useState([]);


    const dateNow = new Date();
    const [regClosedFlag, setRegClosedFlag] = useState(false);

    const [availability, setAvailability] = useState(-1);
    let avail = availability;

    const [enteredLocation, setEnteredLocation] = useState(false);

    let alreadyEnrolled = false;

    // LOCATION DETAILS //
    const [locationOptions, setLocationOptions] = useState([]);     // List of MRT/office locations (displayed in dropdown)
    const [selectedLocation, setSelectedLocation] = useState("");                 // Location participant selects

    let chosenSession = selectedSession;
    let chosenLocation = selectedLocation;

    // IMAGES // 
    const [allImages, setAllImages] = useState([]);
    const [displayImage, setDisplayImage] = useState(0);


    useEffect(() => {
        getEventData();
        getLocations();
        checkIsParticipant();
    }, []);

    let this_user = userId;


    // Fetch event data //
    const getEventData = async () => {

        let user_id = "";
        await new LoggedInTest().get("/accounts/0")
            .then((res) => {
                user_id = res.data.data.account.employee_id
                console.log(user_id);
                setUserId(res.data.data.account.employee_id)
                // console.log("USER'S ID: " + user_id)
                // console.log("ORG's ID: " + employee_id)

                // if (userId == employee_id) {
                //     organiser = true
                //     setIsOrganiser(true)
                //     console.log("IS ORGANISER")
                // } else {
                //     organiser = false
                //     setIsOrganiser(false)
                //     console.log("IS NOT ORGANISER")
                // }

                // console.log(organiser)
            })
            .catch((err) => {
                console.log(err);
            });


        console.log("Fetching event data...")

        new LoggedInUser().get("/events/" + event_id).then(
            (res) => {
                console.log("NORMAL USER VIEW")

                console.log("EVENT ID: " + event_id)
                const event = res.data.event;
                console.log("EVENT DATA:")
                console.log(event)

                console.log("Getting session info...")

                const sessions = res.data.sessions;
                console.log("SESSIONS:")
                console.log(sessions)

                setAllSessions(sessions)

                // Session display list
                const sessionOptions = sessions.map(s => ({
                    "value": s.session_id,
                    "label": createSessionName(s)
                }))
                setOptions(sessionOptions);

                console.log("Getting images...")
                const images = res.data.event.image_url;
                setAllImages(images)

                setInfo(event.info);
                setLocation(event.location);
                setName(event.name);
                setRegCloseDate(event.registration_closes_on);
                setRegOpenDate(event.registration_opens_on);




                // GET LIST OF ALREADY ENROLLED SESSIONS //
                console.log("GETTING ENROLLED SESSIONS")
                console.log("user_id is " + user_id)

                const enrolled_sessions = []
                for (var i = 0; i < sessions.length; i++) {
                    const this_session_attendees = sessions[i].attendees
                    for (var j = 0; j < this_session_attendees.length; j++) {
                        console.log(this_session_attendees[j].employee_id)
                        if (this_session_attendees[j].employee_id === user_id) {
                            console.log("yay")
                            const thisSession = sessions.find(s => s.session_id === sessions[i].session_id)
                            enrolled_sessions.push(thisSession)
                            // enrolled_sessions.push(sessions[i].session_id)
                            break;
                        }
                    }
                }
                console.log("enrolled:")
                console.log(enrolled_sessions)
                setEnrolledSessions(enrolled_sessions)

                const enrolled_strings = enrolled_sessions.map(s => ({
                    "value": s.session_id,
                    "label": createEnrolledSessionName(s)
                }))
                setEnrolledStrings(enrolled_strings);
                console.log("enrolled_strings")
                console.log(enrolled_strings)


                // DISPLAY ONLY AVAILABLE (slots > 0) AND YET-TO-ENROLLED OPTIONS //
                const avail_options = []
                for (var i = 0; i < sessions.length; i++) {
                    if (sessions[i].capacity - sessions[i].fill > 0) {
                        console.log(sessions[i].session_id + " has slots")
                        var avail = true
                        for (var j = 0; j < enrolled_sessions.length; j++) {
                            console.log(enrolled_sessions[j])
                            if (enrolled_sessions[j].session_id === sessions[i].session_id) {
                                console.log(sessions[i].session_id + " is already enrolled")
                                avail = false
                                break
                            }
                        }
                        if (avail) {
                            console.log(sessions[i].session_id + " is available")
                            avail_options.push(sessionOptions[i])
                        }
                    }
                }
                setAvailOptions(avail_options)

                setRegClosedFlag(new Date(regCloseDate) < dateNow);
                // console.log(regClosedFlag)
                // const test = new Date(regCloseDate);
                // console.log(test);
                // console.log(new Date(regCloseDate));
                console.log(dateNow);


            })
            .catch((err) => {
                console.log(err);
            });
    }




    // function createEnrolledSessionName(s_id) {
    //     console.log("creating")
    //     const thisSession = allSessions.find(s => s.session_id === s_id)
    //     // console.log(thisSession)
    //     // const start = new Date(thisSession.start_time)
    //     // const end = new Date(thisSession.end_time)

    //     // var weekday = start.toLocaleDateString('en-US', { weekday: 'short' })
    //     // var day = start.toLocaleDateString('en-US', { day: '2-digit' })
    //     // var month = start.toLocaleDateString('en-US', { month: 'short' })
    //     // var year = start.toLocaleDateString('en-US', { year: 'numeric' })

    //     // var start_time = start.toLocaleString('en-US', { hour: 'numeric', minute: 'numeric', hour12: true })
    //     // var end_time = end.toLocaleString('en-US', { hour: 'numeric', minute: 'numeric', hour12: true })

    //     // return `${weekday}, ${day} ${month} ${year}, ${start_time} - ${end_time}`;
    //     return "hello"

    // }

    // Fetch participants data //
    const checkIsParticipant = async () => {
        let user_id = "";
        await new LoggedInTest().get("/accounts/0")
            .then((res) => {
                user_id = res.data.data.account.employee_id
                console.log(user_id);
                setUserId(res.data.data.account.employee_id)
                // console.log("USER'S ID: " + user_id)
                // console.log("ORG's ID: " + employee_id)

                // if (userId == employee_id) {
                //     organiser = true
                //     setIsOrganiser(true)
                //     console.log("IS ORGANISER")
                // } else {
                //     organiser = false
                //     setIsOrganiser(false)
                //     console.log("IS NOT ORGANISER")
                // }

                // console.log(organiser)
            })
            .catch((err) => {
                console.log(err);
            });

        new LoggedInUser().get("/events/" + event_id + "/participants").then(
            (res) => {
                const participantsList = res.data.data.participants;
                console.log("PART LST : " + participantsList);
                console.log("USERRR", user_id);
                if (participantsList.includes(user_id)) {
                    console.log("IS PARTICIPANTS TRUE");
                    setIsParticipant(true);
                } else {
                    console.log("IS PARTICIPANTS FALSE");
                    setIsParticipant(false);
                }

            })
            .catch((err) => {
                console.log(err);
            });
    }

    function createSessionName(s) {
        console.log("CREATING")
        const start = new Date(s.start_time)
        const end = new Date(s.end_time)

        var weekday = start.toLocaleDateString('en-US', { weekday: 'short' })
        var day = start.toLocaleDateString('en-US', { day: '2-digit' })
        var month = start.toLocaleDateString('en-US', { month: 'short' })
        var year = start.toLocaleDateString('en-US', { year: 'numeric' })

        var start_time = start.toLocaleString('en-US', { hour: 'numeric', minute: 'numeric', hour12: true })
        var end_time = end.toLocaleString('en-US', { hour: 'numeric', minute: 'numeric', hour12: true })

        const fill = s.fill
        const capacity = s.capacity
        var slots = capacity - fill

        var enrolledAlready = false
        // console.log("checkking enrollment")

        // const ids = enrolledIds
        // console.log(ids)
        // for (var i = 0; i < ids.length; i++) {
        //     if (ids[i] === s.session_id) {
        //         enrolledAlready = true
        //     }
        // }

        if (enrolledAlready) {
            return `[ENROLLED] ${weekday}, ${day} ${month} ${year}, ${start_time} - ${end_time}`;
        } else if (slots == 1) {
            return `${weekday}, ${day} ${month} ${year}, ${start_time} - ${end_time} (${slots} slot left)`;
        } else {
            return `${weekday}, ${day} ${month} ${year}, ${start_time} - ${end_time} (${slots} slots left)`;
        }
    }

    function createEnrolledSessionName(s) {
        const start = new Date(s.start_time)
        const end = new Date(s.end_time)

        var weekday = start.toLocaleDateString('en-US', { weekday: 'long' })
        var day = start.toLocaleDateString('en-US', { day: '2-digit' })
        var month = start.toLocaleDateString('en-US', { month: 'short' })
        var year = start.toLocaleDateString('en-US', { year: 'numeric' })

        var start_time = start.toLocaleString('en-US', { hour: 'numeric', minute: 'numeric', hour12: true })
        var end_time = end.toLocaleString('en-US', { hour: 'numeric', minute: 'numeric', hour12: true })

        return `${weekday}, ${day} ${month} ${year}, ${start_time} - ${end_time}`;
    }

    const getLocations = () => {
        const locOptions = locations.map(location => ({
            "value": location["Station Name"],
            "label": `${location["Station Name"]} (${location.Station})`
        }))

        setLocationOptions(locOptions)
    }

    const listOfEnrolled = enrolledStrings.map((s) =>
        <li key={s.label}> {s.label} </li>);


    const listOfSessions = allSessions.map((s) =>
        <div>
            <button className="bg-blue-200 mb-2"
                onClick={() => { clickSession(s) }}>
                <li key={s.label}> {createSessionName(s)} </li>
            </button>
        </div>);

    function clickSession(s) {
        console.log("CLICKED SESSION")
        console.log(s)
    }

    function handleSessionChange(e) {
        console.log("CHANGING SESSION:")
        const thisSession = allSessions.find(s => s.session_id === e.value)

        chosenSession = thisSession;
        setSelectedSession(thisSession)

        avail = thisSession.capacity - thisSession.fill
        setAvailability(avail)
        console.log(avail)
    }

    function handleLocationChange(e) {
        console.log("CHANGING LOCATION:")
        chosenLocation = e.value;
        setSelectedLocation(e.value);
        console.log(chosenLocation)
        setEnteredLocation(true);
    }

    const handleSubmit = (e) => {
        console.log(event_id);
        console.log(chosenLocation);

        new LoggedInUser()
            .post("/events/" + event_id + "/" + chosenSession.session_id, {
                point: chosenLocation
            })
            .then((res) => {
                console.log("SUBMITTED")
                console.log(res);
                console.log(chosenLocation);
            })
            .catch((err) => {
                console.log(err);
            })
    }

    const nextImage = (e) => {
        e.preventDefault();
        console.log("CLICKED NEXT");
        if (displayImage === allImages.length - 1) {
            console.log("REACHED LAST IMAGE")
            setDisplayImage(0)
        } else {
            let index = displayImage + 1
            console.log(index)
            setDisplayImage(index)
        }
    }

    const prevImage = (e) => {
        e.preventDefault();
        console.log("CLICKED PREV");
        if (displayImage === 0) {
            setDisplayImage(allImages.length - 1)
        } else {
            let index = displayImage - 1
            console.log(index)
            setDisplayImage(index)
        }
    }

    return (
        <form>
            <div className="flex justify-center pt-32">
                <div className="flex flex-wrap gap-y-2 w-11/12 max-w-6xl">
                    <div className="w-full mb-8 text-center font-oswald text-[#431903] uppercase text-6xl font-extrabold">{name}</div>

                    <div className="flex flex-wrap mb-6 md:mb-10 lg:mb-12 w-full justify-center items-center">
                        <svg xmlns="http://www.w3.org/2000/svg" class="h-10 w-10 cursor-pointer" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="4"
                            onClick={prevImage.bind()}>
                            <path stroke-linecap="round" stroke-linejoin="round" d="M15 19l-7-7 7-7" />
                        </svg>
                        <div className="flex w-3/4 h-60 md:h-72 lg:h-96 justify-items-center">
                            <img className="object-contain w-full h-full px-12" src={allImages[displayImage]}></img>
                        </div>
                        <svg xmlns="http://www.w3.org/2000/svg" class="h-10 w-10 cursor-pointer" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="4"
                            onClick={nextImage.bind()}>
                            <path stroke-linecap="round" stroke-linejoin="round" d="M9 5l7 7-7 7" />
                        </svg>
                    </div>

                    <div className="flex flex-wrap w-full justify-center">
                        <div className="w-11/12 mb-8">
                            <div className="px-6 py-3 bg-[#f4864c] rounded-t-xl text-2xl font-oswald font-extrabold uppercase text-white"> Event Information </div>
                            <div className="px-6 py-4 bg-[#ffeee5] bg-opacity-20 rounded-b-xl text-md text-justify font-roboto text-[#1c394e]">{info}</div>
                        </div>

                        <div className="w-11/12 h-auto mb-14">
                            <div className="px-6 py-3 bg-[#f4864c] rounded-t-xl text-2xl font-oswald font-extrabold uppercase text-white"> Location </div>
                            <div className="px-6 py-4 bg-[#ffeee5] bg-opacity-20 rounded-b-xl text-md font-bold text-justify font-roboto text-[#1c394e]">{location}</div>
                        </div>


                        <div className={enrolledSessions.length > 0 ? "flex flex-wrap w-full justify-center" : "hidden"}>
                            <div className="w-full border-t border-[#f1cfbd] mb-12"></div>
                            <div className="w-11/12 mb-6 text-2xl font-oswald font-extrabold uppercase text-[#873307] text-center"> You are currently enrolled in the following sessions: </div>
                            <div className="w-11/12 pl-8 mb-12 text-xl font-oswald font-medium uppercase text-[#431903]"> {listOfEnrolled} </div>

                            <div className={availOptions.length > 0 ? "flex flex-wrap w-full justify-center" : "hidden"}>
                                <div className="w-11/12 mb-6 text-2xl font-oswald font-extrabold uppercase text-[#873307] text-center"> Volunteer for another session: </div>
                                <div className="w-8/12 mb-2 text-xl font-oswald font-extrabold uppercase text-[#873307]"> (Select a session) </div>
                                <div className="w-8/12 mb-4">
                                    <Select className="rounded-md border text-[#431903] border-[#bfa191] text-md font-medium font-roboto" options={availOptions}
                                        onChange={handleSessionChange.bind()} />
                                </div>
                                <div className="w-8/12 mb-2 text-xl font-oswald font-extrabold uppercase text-[#873307]"> (Select a pick-up point) </div>
                                <div className="w-8/12 mb-8">
                                    <Select className="rounded-md border text-[#431903] border-[#bfa191] text-md font-medium font-roboto" options={locationOptions}
                                        onChange={handleLocationChange.bind()} />
                                </div>
                                <div className="flex w-full justify-center">
                                    <button type="submit"
                                        className={availability > 0 & enteredLocation === true ? "w-1/5 mb-12 p-4 rounded-md font-oswald font-extrabold text-xl text-white uppercase bg-[#f4864c] text-md px-6 py-3 hover:bg-[#ec5a0d]"
                                            : "cursor-not-allowed mb-12 w-1/5 p-4 rounded-md font-oswald font-extrabold text-xl text-white uppercase bg-[#ffdcc9] text-md px-6 py-3"}
                                        onClick={handleSubmit.bind()}
                                    >
                                        Volunteer!
                                    </button>
                                </div>

                            </div>
                        </div>

                        <div className={enrolledSessions.length === 0 & availOptions.length > 0 ? "flex flex-wrap w-full justify-center" : "hidden"}>
                            <div className="w-full border-t border-[#f1cfbd] mb-12"></div>
                            <div className="w-11/12 mb-12 text-4xl text-center font-oswald font-extrabold uppercase text-[#873307]"> Volunteer for this event </div>

                            <div className="w-10/12 mb-4 text-2xl font-oswald font-extrabold uppercase text-[#873307]"> (Select a session) </div>
                            <div className="w-10/12 mb-10">
                                <Select className="rounded-md border text-[#431903] border-[#bfa191] text-xl font-medium font-roboto" options={availOptions}
                                    onChange={handleSessionChange.bind()} />
                            </div>

                            <div className="w-10/12 mb-4 text-2xl font-oswald font-extrabold uppercase text-[#873307]"> (Select a pick-up point) </div>
                            <div className="w-10/12 mb-10">
                                <Select className="rounded-md border text-[#431903] border-[#bfa191] text-xl font-medium font-roboto" options={locationOptions}
                                    onChange={handleLocationChange.bind()} />
                            </div>

                            <button type="submit"
                                className={availability > 0 & enteredLocation === true ? "w-1/4 mb-8 p-4 rounded-md font-oswald font-extrabold text-2xl text-white uppercase bg-[#f4864c] text-md px-6 py-3 hover:bg-[#ec5a0d]"
                                    : "cursor-not-allowed mb-8 w-1/4 p-4 rounded-md font-oswald font-extrabold text-2xl text-white uppercase bg-[#ffdcc9] text-md px-6 py-3"}
                                onClick={handleSubmit.bind()}
                            >
                                Volunteer!
                            </button>
                        </div>

                        <div className={enrolledSessions.length === 0 & availOptions.length === 0 ? "flex flex-wrap w-full mb-8 justify-center" : "hidden"}>
                            <div className="w-full border-t border-[#f1cfbd] mb-8"></div>
                            No available sessions now.
                        </div>
                    </div>

                    <div className="w-full border-t border-[#f1cfbd] pt-12 mb-8">
                        <div className={isParticipant ? "col-span-3" : "hidden"}>
                            <PostContainer all_posts={all_posts} />
                        </div>
                    </div>
                </div>
            </div >
        </form >
    );
}

export default UserEventPage;