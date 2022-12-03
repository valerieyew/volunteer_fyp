import React, { useState, useEffect } from "react";
import { BrowserRouter as Router, Switch, Route, Link, useParams, useHistory } from "react-router-dom";
import LoggedInUser from "../../../apis/LoggedInUser";
import LoginApi from "../../../apis/LoginApi";
import Select from 'react-select';
import locations from "../../../data/locations.json";
import MapContainer from "./MapContainer";
import LoggedInTest from "../../../apis/LoggedInTest";
import axios from "axios";
import UserEventPage from "./UserEventPage";
import OrgEventPage from "./OrgEventPage";
import LoggedInUserCommunity from "../../../apis/LoggedInUserCommunity";

function EventPage() {

    let { id } = useParams();
    const [posts, setPosts] = useState([]);

    // LOGGED IN USER DETAILS //
    const [userId, setUserId] = useState(0)
    let user_id = userId

    // EVENT DETAILS //
    const [employeeId, setEmployeeId] = useState(-1);
    let employee_id = employeeId;

    // SESSION DETAILS //
    // const dateNow = new Date();
    // const [regClosedFlag, setRegClosedFlag] = useState(false);

    // const [locationOptions, setLocationOptions] = useState([]);     // List of MRT/office locations (displayed in dropdown)
    // const [selectedLocation, setSelectedLocation] = useState("");                 // Location participant selects

    const [isOrganiser, setIsOrganiser] = useState(false);
    let organiser = isOrganiser;
    // let alreadyEnrolled = false;

    // Check if user is admin/organiser //
    const getUser = () => {
        console.log("getting user type...")
        new LoggedInTest().get("/accounts/0")
            .then((res) => {
                user_id = res.data.data.account.employee_id
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
    }

    // Fetch event data //
    const getEventData = () => {
        console.log("Fetching event data...")
        new LoggedInUser().get("/events/" + id).then(
            (res) => {
                // const event = res.data.event;
                employee_id = res.data.event.employee_id;
                setEmployeeId(res.data.event.employee_id);
                console.log("employeeId")
                console.log(employeeId)
            })
            .catch((err) => {
                console.log(err);
            });

    }

    // fetch post data
    const getPostsData = () => {
        console.log("Fetching post data...")
        new LoggedInUserCommunity().get("/posts/" + id).then(
            (res) => {
                const all_posts = res.data.data.posts;
                console.log("ALL POSTS " + all_posts);
                
                setPosts(all_posts.reverse());

            })
            .catch((err) => {
                console.log(err);
            });
        }

    const checkUser = () => {
        console.log("USER'S ID: " + userId)
        console.log("ORG's ID: " + employeeId)
        if (user_id === employee_id) {
            return true
        } else {
            return false
        }
    }

    useEffect(() => {
        getEventData();
        getUser();
        getPostsData();
        // checkUser();
    }, []);


    return (
        <div>
            {checkUser() ?
                <OrgEventPage event_id={id} all_posts={posts} />
                : <UserEventPage event_id={id} all_posts={posts}/>
            }
            
        </div>
    )
}

export default EventPage;