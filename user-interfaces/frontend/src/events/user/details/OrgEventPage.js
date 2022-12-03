import React, { useState, useEffect } from "react";
import { BrowserRouter as Router, Switch, Route, Link, useParams, useHistory } from "react-router-dom";
import LoggedInUser from "../../../apis/LoggedInUser";
import LoginApi from "../../../apis/LoginApi";
import Select from 'react-select';
import MapContainer from "./MapContainer";
import LoggedInTest from "../../../apis/LoggedInTest";
import axios from "axios";
import PostContainer from "../community/PostContainer";
import CreatePost from "../community/CreatePost"
import { useCallback } from "react";
import GenerateMapButton from "./GenerateMapButton";
import locations from '../../../data/output_locations.json';

function OrgEventPage({ event_id, all_posts }) {

    // LOGGED IN USER DETAILS //
    // const userId = userId


    // EVENT DETAILS //
    const [name, setName] = useState("");
    const [info, setInfo] = useState("");
    const [location, setLocation] = useState("");
    const [imageUrl, setImageUrl] = useState("");
    const [status, setStatus] = useState("");
    const [regOpenDate, setRegOpenDate] = useState("");
    const [regCloseDate, setRegCloseDate] = useState("");
    const [employeeId, setEmployeeId] = useState(0);
    const [proposalDetails, setProposalDetails] = useState("");
    const [comments, setComments] = useState(false);
    const [rejected, setRejected] = useState(false);
    const [lastAdminActionBy, setLastAdminActionBy] = useState("");



    // SESSION DETAILS //
    const [allSessions, setAllSessions] = useState([]);
    const [selectedSession, setSelectedSession] = useState([]);
    const [options, setOptions] = useState([]);         // List of sessions (displayed in dropdown)

    const dateNow = new Date();
    const [regClosedFlag, setRegClosedFlag] = useState(false);

    const [fill, setFill] = useState(0)
    const [capacity, setCapacity] = useState(0)

    let chosenSession = selectedSession;

    const [canGenerateMap, setCanGenerateMap] = useState(false);
    const [showMap, setShowMap] = useState(false);

    // IMAGES // 
    const [allImages, setAllImages] = useState([]);
    const [displayImage, setDisplayImage] = useState(0);


    useEffect(() => {
        getEventData();
    }, []);
    const history = useHistory();

    const handleOnClick = useCallback(() => history.push(`/edit/${event_id}`), [history]);


    // Fetch event data //
    const getEventData = () => {

        console.log("Fetching event data...")

        new LoggedInUser().get("/events/" + event_id).then(
            (res) => {
                console.log("ORGANISER VIEW")
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

                console.log("SESSION DISPLAY STRINGS: ")
                console.log(sessionOptions)

                console.log("Getting images...")
                const images = res.data.event.image_url;
                console.log("IMAGE URLS:")
                console.log(images)
                setAllImages(images)
                console.log(allImages)

                setInfo(event.info);
                setLocation(event.location);
                setName(event.name);
                setStatus(event.status);
                setRegCloseDate(event.registration_closes_on);
                setRegOpenDate(event.registration_opens_on);
                if (event.comments === "") {
                    setComments("No comments");
                } else {
                    setComments(event.comments);
                }
                if (event.status === "Rejected") {
                    setRejected(true);
                } else {
                    setRejected(false);
                }
                console.log(rejected);

                setLastAdminActionBy(event.last_admin_action_by);

                setOptions(sessionOptions);

                console.log("OPTIONS");
                console.log(options);
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

    const listOfSessions = options.map((s) =>
        <li key={s.label}> {s.label} </li>);


    const handleGenerateMap = (s_id) => {
        // e.preventDefault();
        console.log("GENERATING MAP")
        console.log("this is the selected session: " + s_id)
        setSelectedSession(s_id)
        setShowMap(true);

        // CALL TRANSPORT ALGO

    }

    const closeMap = (e) => {
        e.preventDefault();
        setShowMap(false);
    }


    const listOfApprovedSessions = allSessions.map((s) =>
        <li className="flex flex-wrap" key={s.label}> {createSessionName(s)}
            <div className="mx-4 font-medium font-roboto text-[#305f82] hover:text-[#5b96c2] cursor-pointer" onClick={() => { handleGenerateMap(s.session_id) }}>
                Generate map
            </div>

            {/* <div
            className="mx-4 font-medium font-roboto text-[#305f82] hover:text-[#5b96c2] cursor-pointer"
            // onClick={handleGenerateMap}
            onClick={generate(s.session_id)}
            >
            Generate map
            </div> */}
        </li>);


    function createSessionName(s) {
        console.log("creating session name for")
        console.log(s)

        const start = new Date(s.start_time)
        const end = new Date(s.end_time)

        var weekday = start.toLocaleDateString('en-US', { weekday: 'short' })
        var day = start.toLocaleDateString('en-US', { day: '2-digit' })
        var month = start.toLocaleDateString('en-US', { month: 'short' })
        var year = start.toLocaleDateString('en-US', { year: 'numeric' })

        var start_time = start.toLocaleString('en-US', { hour: 'numeric', minute: 'numeric', hour12: true })
        var end_time = end.toLocaleString('en-US', { hour: 'numeric', minute: 'numeric', hour12: true })

        if (status === 'Approved') {
            return `${weekday}, ${day} ${month} ${year}, ${start_time}-${end_time} (${s.fill}/${s.capacity} slots filled)`;
        } else {
            return `${weekday}, ${day} ${month} ${year}, ${start_time}-${end_time} (${s.capacity} slots)`;
        }
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
                <div className="flex flex-wrap justify-center gap-y-2 w-11/12 max-w-6xl">

                    <div className={`${status === 'Approved' ? "flex flex-wrap w-11/12 mb-8 justify-between" : "hidden"}`}>
                        <div className="w-3/5">
                            <div className="flex flex-wrap self-center">
                                <div className="w-full p-3 pl-5 bg-green-600 rounded-t-xl text-xl font-roboto font-extrabold  text-white"> Approved by: {lastAdminActionBy} </div>
                                <div className="w-full p-2 pl-4 bg-white rounded-b-xl border border-green-600 text-xl font-kalam text-black"> {comments} </div>
                            </div>
                        </div>
                        <div className="flex w-2/5 gap-1 items-baseline justify-end font-oswald font-semibold text-lg text-white">
                            <button type="button" class="flex flex-row gap-3 self-center items-center rounded-md bg-[#f4864c] font-oswald uppercase font-extrabold text-white p-4 text-lg md:text-2xl"
                                onClick={handleOnClick} >
                                <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6 md:h-8 md:w-8" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="3">
                                    <path stroke-linecap="round" stroke-linejoin="round" d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z" />
                                </svg>
                                <div> Edit this event </div>
                            </button>

                        </div>
                    </div>

                    <div className={`${status === 'Rejected' ? "flex flex-wrap w-11/12 mb-8 justify-between" : "hidden"}`}>
                        <div className="w-3/5">
                            <div className="flex flex-wrap self-center">
                                <div className="w-full p-3 pl-5 bg-red-500 rounded-t-xl text-xl font-roboto font-extrabold  text-white"> Rejected by: {lastAdminActionBy} </div>
                                <div className="w-full p-2 pl-4 bg-white rounded-b-xl border border-red-500 text-xl font-kalam text-black"> {comments} </div>
                            </div>
                        </div>
                        <div className="flex w-2/5 gap-1 items-baseline justify-end font-oswald font-semibold text-lg text-white">
                            <button type="button" class="flex flex-row gap-3 self-center items-center rounded-md bg-[#f4864c] font-oswald uppercase font-extrabold text-white p-4 text-lg md:text-2xl"
                                onClick={handleOnClick} >
                                <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6 md:h-8 md:w-8" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="3">
                                    <path stroke-linecap="round" stroke-linejoin="round" d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z" />
                                </svg>
                                <div> Edit this event </div>
                            </button>

                        </div>
                    </div>


                    <div className="w-full mb-4 md:mb-8 lg:mb-10 text-center font-oswald text-[#431903] uppercase text-6xl font-extrabold">{name}</div>

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
                            <div className="px-6 py-3 bg-[#f69d6e] rounded-t-xl text-2xl font-oswald font-extrabold uppercase text-white"> Event Information </div>
                            <div className="px-6 py-3 bg-[#f69d6e] bg-opacity-20 rounded-b-xl text-md font-roboto text-[#1c394e]">{info}</div>
                        </div>

                        <div className="w-11/12 mb-8">
                            <div className="px-6 py-3 bg-[#f69d6e] rounded-t-xl text-2xl font-oswald font-extrabold uppercase text-white"> Location </div>
                            <div className="px-6 py-3 bg-[#f69d6e] bg-opacity-20 rounded-b-xl text-md font-roboto text-[#1c394e]">{location}</div>
                        </div>

                        {/* For PENDING/REJECTED EVENTS */}
                        <div className={`${status === 'Approved' ? "hidden" : "w-11/12 h-auto mb-14"}`}>
                            <div className="px-6 py-3 bg-[#f69d6e] rounded-t-xl text-2xl font-oswald font-extrabold uppercase text-white"> Sessions </div>
                            <div className="px-6 py-3 bg-[#f69d6e] bg-opacity-20 rounded-b-xl text-md font-roboto font-bold text-[#1c394e]"> {listOfSessions} </div>
                        </div>

                        {/* For APPROVED EVENTS */}
                        <div className={`${status === 'Approved' ? "w-11/12 h-auto mb-14" : "hidden"}`}>
                            <div className="px-6 py-3 bg-[#f69d6e] rounded-t-xl text-2xl font-oswald font-extrabold uppercase text-white"> Sessions </div>
                            <div className="px-6 py-3 bg-[#f69d6e] bg-opacity-20 rounded-b-xl text-md font-roboto font-bold text-[#1c394e]"> {listOfApprovedSessions} </div>
                        </div>


                        <div className={showMap ? "fixed inset-0 z-49 px-32 pb-12 overflow-auto bg-black bg-opacity-80 flex" : "hidden"}>
                            <div className="relative p-12 px-0 mt-32 bg-white w-full m-auto flex-col flex rounded-lg">
                                <span className="absolute top-0 right-0 p-4">
                                    <button type="button" className="focus:outline-none focus:border-none hover:bg-gray-400 hover:bg-opacity-25 p-2 rounded-full inline-flex items-center"
                                        onClick={(e) => closeMap(e)}>
                                        <svg
                                            className="h-6 w-6 fill-current text-grey hover:text-grey-darkest"
                                            role="button"
                                            xmlns="http://www.w3.org/2000/svg"
                                            viewBox="0 0 20 20"
                                        >
                                            <path d="M14.348 14.849a1.2 1.2 0 0 1-1.697 0L10 11.819l-2.651 3.029a1.2 1.2 0 1 1-1.697-1.697l2.758-3.15-2.759-3.152a1.2 1.2 0 1 1 1.697-1.697L10 8.183l2.651-3.031a1.2 1.2 0 1 1 1.697 1.697l-2.758 3.152 2.758 3.15a1.2 1.2 0 0 1 0 1.698z" />
                                        </svg>
                                    </button>
                                </span>
                                <div className="text-center font-oswald text-[#873307] uppercase text-6xl font-bold mb-6">
                                    Bus Route
                                </div>
                                <div className="text-center font-oswald text-[#652605] uppercase text-3xl font-bold mb-4">
                                    <div>Estimated Cost: ${locations[0][0].total_cost}</div>
                                    <div>Total Number of Buses: {locations[0][0].no_of_clusters}</div>
                                </div>
                                <div className="">
                                    <MapContainer locations={locations}/>
                                </div>
                            </div>
                        </div>


                        <div className="w-full border-t border-[#f1cfbd] mb-12"></div>

                        <div className={`${status === 'Approved' ? "flex flex-wrap w-full justify-center" : "hidden"}`}>
                            <div className="w-11/12 mb-4 text-4xl text-center font-oswald font-extrabold uppercase text-[#873307]"> Important updates </div>

                            <div className={rejected ? "hidden" : "w-11/12 mb-12"}>
                                <CreatePost event_id={event_id} />
                            </div>
                            <div className="w-11/12">
                                <PostContainer all_posts={all_posts} />
                            </div>
                        </div>

                        {/* <div className="w-10/12 mb-4 text-2xl font-oswald font-extrabold uppercase text-[#873307]"> (Select a session) </div>
                        <div className="w-10/12 mb-10">
                            <Select className="rounded-md border text-[#431903] border-[#bfa191] text-xl font-medium font-roboto" options={options}
                                onChange={handleSessionChange.bind()} />
                        </div>

                        <div className="w-10/12 mb-4 text-2xl font-oswald font-extrabold uppercase text-[#873307]"> (Select a pick-up point) </div>
                        <div className="w-10/12 mb-10">
                            <Select className="rounded-md border text-[#431903] border-[#bfa191] text-xl font-medium font-roboto" options={locationOptions}
                                onChange={handleLocationChange.bind()} />
                        </div> */}

                        {/* <button type="submit"
                            className={availability > 0 & enteredLocation === true ? "w-1/4 mb-8 p-4 rounded-md font-oswald font-extrabold text-2xl text-white uppercase bg-[#f4864c] active:bg-blueGray-600 text-md px-6 py-3 hover:bg-[#ec5a0d]"
                                : "cursor-not-allowed mb-8 w-1/4 p-4 rounded-md font-oswald font-extrabold text-2xl text-white uppercase bg-[#ffdcc9] text-md px-6 py-3"}
                            onClick={handleSubmit.bind()}
                        >
                            Volunteer!
                        </button> */}
                    </div>





                    {/* <div className="w-full mt-10 text-justify text-gray-700 text-md font-bold">Admin Comments:</div>

                        <div className="col-span-3 my-5 w-full text-justify text-gray-500 text-md italic">
                        
                            <span className="inline-block align-text-bottom py-2.5">{comments}</span>
                            <button type="button" class=" float-right text-white bg-gradient-to-r from-blue-500 via-blue-600 to-blue-700 hover:bg-gradient-to-br focus:ring-4 focus:ring-blue-300 dark:focus:ring-blue-800 font-medium rounded-lg text-sm px-5 py-2.5 text-center"
                            onClick={handleOnClick} >Edit</button>
                           
                        </div> */}




                    <div className="mt-10 w-full border-t-2 pt-8">
                        {/* <div className="text-justify text-gray-700 uppercase text-lg font-bold">Sessions</div>
                        <Select className="w-96 rounded-md text-md mt-2 font-medium" options={options}
                            onChange={handleSessionChange.bind()}
                        /> */}

                        {/* <div className={canGenerateMap ? "col-span-3 mt-2 ml-2 mb-6 text-justify text-gray-700 text-md" : "hidden"}>Session fill: {fill} / {capacity} </div> */}


                        {/* <div>
                            <div
                                className={canGenerateMap === true ? "w-96 mt-2 mb-10 bg-blueGray-800 text-white text-center  active:bg-blueGray-600 text-sm font-bold uppercase px-6 py-3 rounded shadow hover:shadow-lg outline-none focus:outline-none mr-1 ease-linear transition-all duration-150"
                                    : "hidden"}
                                onClick={generateMap}
                            >
                                Generate Map
                            </div>
                        </div> */}

                    </div>
                </div>
            </div>
        </form>

    )
}

export default OrgEventPage;