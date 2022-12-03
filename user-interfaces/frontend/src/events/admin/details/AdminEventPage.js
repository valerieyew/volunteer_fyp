import React, { useState, useEffect } from "react";
import { BrowserRouter as Router, Switch, Route, Link, useParams, useHistory } from "react-router-dom";
import LoggedInUser from "../../../apis/LoggedInUser";
import LoginApi from "../../../apis/LoginApi";
import Select from 'react-select';
import locations from "../../../data/locations.json";
import MapContainer from "../../user/details/MapContainer";
import LoggedInTest from "../../../apis/LoggedInTest";
import axios from "axios";
import LoggedInAdmin from "../../../apis/LoggedInAdmin";

function AdminEventPage({ event_id }) {

    let history = useHistory();

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
    const [adminRemarks, setAdminRemarks] = useState("");
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
    const [btnClicked, setBtnClicked] = useState("");
    const [displayConfirmBtn, setDisplayConfirmBtn] = useState(false);
    const [displayApprovRejectBtn, setDisplayApprovRejectBtn] = useState(true);
    const [displayCommentsTextbox, setDisplayCommentsTextbox] = useState(false);
    const [comments, setComments] = useState(false);

    const [displayConfirmDialog, setDisplayConfirmDialog] = useState(false);

    // IMAGES // 
    const [allImages, setAllImages] = useState([]);
    const [displayImage, setDisplayImage] = useState(0);

    useEffect(() => {
        getEventData();
    }, []);

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

                setImageUrl(event.image_url);
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
                console.log(event.commments)
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

                console.log("Getting images...")
                const images = res.data.event.image_url;
                console.log("IMAGE URLS:")
                console.log(images)
                setAllImages(images)
                console.log(allImages)
            })
            .catch((err) => {
                console.log(err);
            });
    }

    const listOfSessions = options.map((s) =>
        <li key={s.label}> {s.label} </li>);

    const listOfApprovedSessions = allSessions.map((s) =>
        <li key={s.label}> {createSessionName(s)}
            <button className="mx-4 font-medium font-roboto text-[#305f82] hover:text-[#5b96c2]"
                onClick={handleGenerateMap(s.session_id)}> (Generate map) </button>
        </li>);

    function createSessionName(s) {
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

        if (status === 'Approved') {
            return `${weekday}, ${day} ${month} ${year}, ${start_time}-${end_time} (${fill}/${capacity} slots filled)`;
        } else {
            return `${weekday}, ${day} ${month} ${year}, ${start_time}-${end_time} (${capacity} slots)`;
        }
    }

    function handleSessionChange(e) {
        if (status === 'Approved') {
            console.log("CHANGING SESSION:")
            const thisSession = allSessions.find(s => s.session_id === e.value)
            console.log(thisSession)

            chosenSession = thisSession;
            setSelectedSession(thisSession)
            console.log(chosenSession)

            setFill(thisSession.fill)
            setCapacity(thisSession.capacity)

            setCanGenerateMap(true)
        }
    }
    function handleCommentsChange(e) {
        const comments = e.target.value;
        console.log(comments)
        setAdminRemarks(comments);
    }

    function handleApprovedBtnClicked() {
        setBtnClicked("approve");
        // setDisplayApprovRejectBtn(false);
        // setDisplayCommentsTextbox(true);
        setDisplayConfirmDialog(true);
    }

    function handleRejectedBtnClicked() {
        setBtnClicked("reject");
        // setDisplayApprovRejectBtn(false);
        // setDisplayCommentsTextbox(true);
        setDisplayConfirmDialog(true);
    }

    function handleCancelClicked() {
        setBtnClicked("");
        // setDisplayApprovRejectBtn(true);
        // setDisplayCommentsTextbox(false);
        setDisplayConfirmDialog(false);
    }

    function handleGenerateMap(s) {
        console.log("GENERATING MAP")
        console.log(s)
        // NEED TO CALL TRANSPORT ALGO
    }

    const generateMap = () => {
        if (status === 'approve') {
            setShowMap(true);
        }
    }

    function handleApproveReject() {
        if (btnClicked === 'approve') {
            new LoggedInAdmin().patch(`/events/${event_id}/approve`, {
                comments: adminRemarks
            })
                .then(
                    (res) => {
                        console.log(res)
                        console.log(event_id)
                        history.push('/admin/home')
                    })
        } else {
            new LoggedInAdmin().patch(`/events/${event_id}/reject`, {
                comments: adminRemarks
            })
                .then(
                    (res) => {
                        console.log(res)
                        console.log(event_id)
                        history.push('/admin/home')
                    })
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
        <div className="flex justify-center pt-32">
            <div className="flex flex-wrap gap-y-2 w-11/12 max-w-6xl">
                <div className="w-full mb-8">
                    <div className="p-3 pl-5 bg-[#a9c8df] rounded-t-xl text-md font-roboto font-extrabold  text-[#1c394e]"> Last reviewed by: {lastAdminActionBy} </div>
                    <div className="p-2 pl-4 bg-white rounded-b-xl border border-[#a9c8df] text-lg font-kalam text-[#1c394e]"> {comments} </div>
                </div>

                <div className="w-full mb-4 md:mb-8 lg:mb-10 text-center font-oswald text-[#132634] uppercase text-6xl font-extrabold">{name}</div>

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
                        <div className="px-6 py-3 bg-[#305f82] rounded-t-xl text-2xl font-oswald font-extrabold uppercase text-white"> Event Information </div>
                        <div className="px-6 py-4 bg-[#305f82] bg-opacity-20 rounded-b-xl text-md text-justify font-roboto text-[#1c394e]">{info}</div>
                    </div>

                    <div className="w-11/12 h-auto mb-8">
                        <div className="px-6 py-3 bg-[#305f82] rounded-t-xl text-2xl font-oswald font-extrabold uppercase text-white"> Location </div>
                        <div className="px-6 py-4 bg-[#305f82] bg-opacity-20 rounded-b-xl text-md font-bold text-justify font-roboto text-[#1c394e]">{location}</div>
                    </div>

                    {/* For PENDING/REJECTED EVENTS */}
                    <div className={`${status === 'Approved' ? "hidden" : "w-11/12 h-auto mb-14"}`}>
                        <div className="px-6 py-3 bg-[#305f82] rounded-t-xl text-2xl font-oswald font-extrabold uppercase text-white"> Sessions </div>
                        <div className="px-6 py-4 bg-[#305f82] bg-opacity-20 rounded-b-xl text-md text-justify font-roboto text-[#1c394e]"> {listOfSessions} </div>
                    </div>

                    {/* For APPROVED EVENTS */}
                    <div className={`${status === 'Approved' ? "w-11/12 h-auto mb-14" : "hidden"}`}>
                        <div className="px-6 py-3 bg-[#305f82] rounded-t-xl text-2xl font-oswald font-extrabold uppercase text-white"> Sessions </div>
                        <div className="px-6 py-4 bg-[#305f82] bg-opacity-20 rounded-b-xl text-md text-justify font-roboto text-[#1c394e]"> {listOfApprovedSessions} </div>
                    </div>
                </div>

                <div className={`${status === 'Pending' ? "flex flex-wrap w-full justify-center" : "hidden"}`}>
                    <div className="w-full border-t border-[#a9b9c5]"></div>
                    <div className="w-11/12 pt-14 mb-2 text-lg font-roboto font-extrabold uppercase text-[#264c68]"> Admin Comments (if any):</div>
                    <textarea type="text" class="form-textarea w-11/12 mb-6 px-4 py-3 border-[#4385b6] rounded-md focus:border-2 focus:border-[#4385b6]"
                        onChange={handleCommentsChange.bind()} />

                    <div className="flex flex-wrap w-full gap-12 justify-center mb-12">
                        <button className="w-1/4 p-4 rounded-2xl font-oswald font-extrabold text-2xl text-white uppercase bg-red-600 hover:bg-red-700"
                            onClick={handleRejectedBtnClicked}> Reject </button>
                        <button className="w-1/4 p-4 rounded-2xl font-oswald font-extrabold text-2xl text-white uppercase bg-green-600 hover:bg-green-700"
                            onClick={handleApprovedBtnClicked}> Approve </button>
                    </div>
                </div>

                <div className={displayConfirmDialog ? "fixed inset-0 z-49 overflow-auto bg-black bg-opacity-80 flex" : "hidden"}>
                    <div className="relative p-8 bg-white w-full max-w-xl m-auto flex-col flex rounded-lg">
                        <div className="text-2xl font-roboto font-bold mb-4"> You are about to {btnClicked} this proposal. </div>
                        <div className="text-xl font-roboto mb-8"> Are you sure you want to proceed? </div>
                        <span className="absolute top-0 right-0 p-4">
                            <button className="focus:outline-none focus:border-none hover:bg-gray-400 hover:bg-opacity-25 p-2 rounded-full inline-flex items-center"
                                onClick={handleCancelClicked}>
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
                        <div className="flex w-full justify-end">
                            <button className=" w-1/6 mx-4 text-white text-center bg-red-600 active:bg-red-700 text-md font-extrabold uppercase px-4 py-3 rounded shadow ease-linear transition-all duration-150"
                                onClick={handleCancelClicked}>
                                No
                            </button>
                            <button className=" w-1/6 text-white text-center bg-green-600 active:bg-green-700 text-md font-bold uppercase px-4 py-3 rounded shadow ease-linear transition-all duration-150"
                                onClick={handleApproveReject}>
                                Yes
                            </button>
                        </div>
                    </div>
                </div>








                {/* <div
                    className={canGenerateMap === true ? "mt-2 mb-10 bg-blueGray-800 text-white text-center  active:bg-blueGray-600 text-sm font-bold uppercase px-6 py-3 rounded shadow hover:shadow-lg outline-none focus:outline-none mr-1 w-full ease-linear transition-all duration-150"
                        : "hidden"}
                    onClick={generateMap}
                >
                    Generate Map
                </div> */}
            </div>

            {/* <div className={showMap ? "col-span-3 text-justify text-gray-700 uppercase text-lg font-bold"
                : "hidden"}>
                Pick-Up Map
            </div>
            <div className={showMap ? "col-span-3 mt-2 mb-10" : "hidden"}>
                <MapContainer />
            </div> */}



            {/* {displayApprovRejectBtn && <div className="col-span-3 my-5 justify-center">
                            <button class={`${status === 'Pending' ? "bg-green-400 hover:bg-blue-700 text-white font-bold py-2 px-4 mt-5 rounded-full w-1/5" : "hidden"}`}
                                onClick={handleApprovedBtnClicked} >
                                Approve
                            </button>
                            <button class={`${status === 'Pending' ? "bg-red-500 hover:bg-blue-700 text-white font-bold py-2 px-4 mt-5 ml-3 rounded-full w-1/5" : "hidden"}`}
                                onClick={handleRejectedBtnClicked} >

                                Reject
                            </button>

                        </div>}
                        {displayCommentsTextbox && <div className="col-span-3 my-4 justify-center">
                            <label className="block text-blueGray-600 text-s font-bold mb-2">Enter Remarks for Event Organiser:</label>
                            <textarea name="body" cols="32" rows="3" placeholder="Please enter your remarks." class="p-2 rounded border border-gray-8 bg-white dark:border-gray-700 text-gray-600 dark:text-gray-800 focus:bg-white focus:outline-none focus:ring-2 focus:ring-teal-400 focus:border-transparent placeholder-gray-400 text-sm h-auto" maxlength="500"
                                onChange={handleCommentsChange.bind()}>
                            </textarea>
                        </div>}
                        {displayCommentsTextbox && <div className="col-span-3 justfiy-center">
                            <button className=" w-1/7 mt-2 mr-2 mb-4 bg-blueGray-800 text-white text-center  active:bg-blueGray-600 text-sm font-bold uppercase px-6 py-3 rounded shadow hover:shadow-lg outline-none focus:outline-none ease-linear transition-all duration-150"
                                onClick={handleCancelClicked}>
                                Cancel
                            </button>
                            <button className=" w-1/7 ml-2 b-10 bg-blueGray-800 text-white text-center  active:bg-blueGray-600 text-sm font-bold uppercase px-6 py-3 rounded shadow hover:shadow-lg outline-none focus:outline-none mr-1 ease-linear transition-all duration-150"
                                onClick={handleApproveReject}>
                                Confirm
                            </button>
                        </div>}
 */}


            {/* <div className="col-span-2">
                            <div
                                className={canGenerateMap === true ? "mt-2 mb-10 bg-blueGray-800 text-white text-center  active:bg-blueGray-600 text-sm font-bold uppercase px-6 py-3 rounded shadow hover:shadow-lg outline-none focus:outline-none mr-1 w-full ease-linear transition-all duration-150"
                                    : "hidden"}
                                onClick={generateMap}
                            >
                                Generate Map
                            </div>
                        </div> */}

        </div>

    )
}

export default AdminEventPage;