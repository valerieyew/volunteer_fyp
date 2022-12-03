import React, { useState, useEffect } from "react";
// import { Map, GoogleApiWrapper } from '@react-google-maps/api';
import EventApi from "../../../apis/EventApi";
import LoggedInUser from "../../../apis/LoggedInUser";
import { useHistory, useParams } from "react-router-dom";
import EditSessions from "./EditSessions";
import EditDT from "./EditDT";
import EditRegDT from "./EditRegDT";

function EditEvent() {

  let { id } = useParams();    
  let history = useHistory();

  console.log("EventID", id);

  const [name, setName] = useState(""); // in the form
  const [location, setLocation] = useState(""); // in the form
  const [postalCode, setPostalCode] = useState(""); // in the form
  const [fullAddress, setFullAddress] = useState("");
  const [proposalDetails, setProposalDetails] = useState(""); // in the form
  const [info, setInfo] = useState(""); // in the form
  const [registrationOpensOn, setRegistrationOpensOn] = useState(""); // in the form
  const [registrationClosesOn, setRegistrationClosesOn] = useState(""); // in the form
  const [images, setImages] = useState([]); // in the form
  const [tempImages, setTempImages] = useState([]); // in the form
  const [imagesCount, setImagesCount] = useState(0); // default image count is 0
  const [tags, setTags] = useState([]);  // in the form
  const [sessions, setSessions] = useState([]); // in the form
  const [sessionsCount, setSessionsCount] = useState(0); // default image count is 0
  const [invalidDetails, setInvalidDetails] = useState(false);
  const [submittedForm, setSubmittedForm] = useState(false);
  const [comments, setComments] = useState(false);


  // add the selected tag to the list
  const addTag = (event) => {
    setTags([...tags, String(event.target.value)]);
  }

  const removeTag = (tag) => {
    const array = [...tags]; // make a separate copy of the array
    const index = array.indexOf(tag);
    if (index !== -1) {
      array.splice(index, 1);
      setTags(array);
    }
  }

  // add an empty string to image list
  const addImage = (event) => {
    const newImage = { id: imagesCount + 1, image: "" }
    setTempImages([...tempImages, newImage]);
    setImagesCount(imagesCount + 1);
    // setTempImages([...images, String(event.target.value)]);
    event.preventDefault();
  }

  const handleImageChange = (image, event) => {
    // let imagesCopy = [...images];
    // imagesCopy = imagesCopy.map(img => img === image ? event.target.value : img);
    const imageItem = tempImages.find(element => element.id === image.id && element.image === image.image);
    imageItem.image = event.target.value;
    // const imageItem = images.filter(element => element === image);
    // const newImages = images.map(img => img === image ? event.target.value : img);
    // const latestImg = images.filter(element => element !== image);
    // setTempImages(i);
    // setImages([...images, String(event.target.value)]);

    // imageItem = event.target.value;
    // console.log("LATEST IMAGE URL ", imageItem);
    console.log("LATEST IMAGES ", tempImages);
  }

  const removeImage = (id, event) => {
    const newImages = tempImages.filter(element => element.id !== id);
    console.log("NEW TEST: ", newImages);
    setTempImages(newImages);
    event.preventDefault();
  }

  const addSession = (event) => {
    const newSession = { start_time: "Fri, 1 Apr 2022 00:00:00 GMT", end_time: "Fri, 1 Apr 2022 00:00:00 GMT", capacity: 0, fill: 0 };
    setSessions([...sessions, newSession]);
    event.preventDefault();


    // let updatedList = state.todos.map(item => 
    //     {
    //       if (item.id == id){
    //         return {...item, done: !item.done}; //gets everything that was already in item, and updates "done"
    //       }
    //       return item; // else return unmodified item 
    //     });

    //   setState({todos: updatedList}); // set state to new object with updated list
  }

  const handleSessionStartTimeChange = (sessionId, event) => {
    // let updateSessions = state.todos.map(element => {
    //     if (element.id == sessionId) {
    //         return {...element, start_time: event.target.value}; 
    //     }
    //     return element; // else return unmodified item 
    //     });
    //     setState({sessions: updateSessions});

    const sessionItem = sessions.find(element => element.session_id == sessionId);
    sessionItem.start_time = event.target.value;
    console.log("UPDATED", sessions);
  }
  // const  handleSessionStartTimeChange = (sessionId, event) => {
  //   let updatedSessions = sessions.map((element) => {
  //       if (element.id === event.target.value) {
  //       return { ...updatedSessions, start_time: event.target.value };
  //       }

  //       return { ...updatedSessions };
  //   });
  //   setSessions(updatedSessions); // not working // this should work now

  // }

  const handleSessionEndTimeChange = (sessionId, event) => {
    const sessionItem = sessions.find(element => element.session_id == sessionId);
    sessionItem.end_time = event.target.value;
    console.log("UPDATED", sessions);

  }

  const handleSessionCapacityChange = (sessionId, event) => {
    const sessionItem = sessions.find(element => element.session_id == sessionId);
    sessionItem.capacity = Number(event.target.value);
  }

  const removeSession = (sessionId, event) => {
    const newSessions = sessions.filter(element => element.session_id !== sessionId);
    setSessions(newSessions);
    event.preventDefault();
  }

  const handleInvalidDetails = () => {
    setInvalidDetails(true);
  };

  const concatenateAddresses = () => {
    setFullAddress(location + " Singapore " + postalCode);
  }

  const formatImages = () => {
    // const formattedImages = images.map((img) =>
    //   {return img.imageLink}
    // );
    // setImages(formattedImages);
    // console.log(images)
  }

  var useReducer = React.useReducer;
  const [_, forceUpdate] = useReducer((x) => x + 1, 0);

  const updateEvent = async (event) => {
    concatenateAddresses();
    formatImages();
    forceUpdate();
    event.preventDefault();
    console.log("LATEST SESS", sessions);

    let newImagesArray = []
    for (var i = 0; i < tempImages.length; i++) {
      newImagesArray[i] = tempImages[i]['image'];
    }
    console.log("NEW IMAGES ARRAY ", newImagesArray);

    await EventApi.patch("/events/" + id, {
      "name": name,
      "location": location,
      "proposal_details": "Proposal Details",
      "info": info,
      "registration_opens_on": registrationOpensOn,
      "registration_closes_on": registrationClosesOn,
      "image_url": newImagesArray,
      "sessions": sessions,
      "tags": tags
    })
      .then((res) => {
        console.log(res)
        // sessionStorage.setItem("jwtToken", res.data.token)
        history.push('/proposed');

        // if (res.status === 201) {
        //   setSubmittedForm(true);
        //   this.props.history.push("/new");
        // }
      }

      ).catch((err) => {
        console.log(err.response)
        console.log(images)
        console.log(sessions)
        handleInvalidDetails()
      })

  }
  // Fetch event data //
  const getEventData = () => {

    console.log("Fetching event data...")

    new LoggedInUser().get("/events/" + id).then(
      (res) => {
        console.log("EVENT ID: " + id)
        const event = res.data.event;
        console.log("EVENT DATA:")
        console.log(event)

        console.log("Getting session info...")

        const sessions = res.data.sessions;
        console.log("SESSIONS:")
        console.log(sessions);
        console.log(sessions.length);

        setSessions(
          sessions.map((session) => {
            return {
              ...session, start_time: new Date(session.start_time).toISOString().slice(0, - 5),
              end_time: new Date(session.end_time).toISOString().slice(0, - 5)
            };
          })
        );
        // setSessions(sessions);
        let start = new Date(sessions[0].start_time).toISOString().slice(0, - 5);
        // start = start.
        console.log("FORMATTED", start);

        // setSessions([
        //     {
        //         "event_id": 2,
        //         "session_id": 3,
        //         "start_time": "2022-05-01T12:00:00",
        //         "end_time": "2022-05-01T15:00:00",
        //         "capacity": 50,
        //         "fill": 0
        //     },
        //     {
        //         "event_id": 2,
        //         "session_id": 4,
        //         "start_time": "2022-06-01T12:00:00",
        //         "end_time": "2022-06-01T15:00:00",
        //         "capacity": 50,
        //         "fill": 0
        //     }]);

        console.log("Getting images...")
        const images = res.data.event.image_url;
        console.log("IMAGE URLS:")
        console.log(images)
        // Session display list
        //  const imagesFormat = images.map(img => ({
        //   "Value": s.session_id,
        //   "label": createSessionName(s)
        // }))
        let imagesFormat = [];
        let count = 0;
        for (var i = 0; i < images.length; i++) {
          count++;
          imagesFormat[i] = { id: count, image: images[i] };
        }
        setImagesCount(count);

        // setImages(images)
        setTempImages(imagesFormat);
        console.log("FORMATTED ARRAY: ", imagesFormat);
        console.log(images)

        const tags = res.data.event.tags;
        setTags(tags)
        setInfo(event.info);
        setLocation(event.location);
        setName(event.name);
        setProposalDetails(event.proposal_details)
        setRegistrationOpensOn(new Date(event.registration_opens_on).toISOString().slice(0, - 5));
        setRegistrationClosesOn(new Date(event.registration_closes_on).toISOString().slice(0, - 5));
        if (event.comments === "") {
          setComments("No comments");
        } else {
          setComments(event.comments);
        }

        // console.log(regClosedFlag)
        // const test = new Date(regCloseDate);
        // console.log(test);
        // console.log(new Date(regCloseDate));

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
      <div class="flex pt-32 mb-32 justify-center">
        <form class="w-full max-w-4xl">

          {/* Event Title */}
          <div class="flex flex-wrap -mx-3 mb-6">
            <div class="w-full px-3">
              <label class="block uppercase font-oswald tracking-wide text-[#652605] text-xl font-bold mb-2" for="grid-name-of-event">
                Event Title
              </label>
              <input class="appearance-none block w-full bg-gray-200 text-gray-700 border border-gray-200 rounded py-3 px-4 mb-3 leading-tight focus:outline-none focus:bg-white focus:border-gray-500"
                id="grid-name-of-event"
                type="text"
                name="name"
                defaultValue={name}
                onChange={(e) => {
                  setName(e.target.value);
                }}
              />
            </div>
          </div>

          {/* Address */}
          <div class="flex flex-wrap -mx-3 mb-10">
            <div class="w-full md:w-2/3 px-3 mb-6 md:mb-0">
              <label class="block uppercase font-oswald tracking-wide text-[#652605] text-xl font-bold mb-2" for="grid-city">
                Address of event
              </label>
              <input class="appearance-none block w-full bg-gray-200 text-gray-700 border border-gray-200 rounded py-3 px-4 leading-tight focus:outline-none focus:bg-white focus:border-gray-500"
                id="grid-city"
                type="text"
                defaultValue={location}
                onChange={(e) => {
                  setLocation(e.target.value);
                }}
              />
            </div>

            {/* <div class="w-full md:w-1/3 px-3 mb-6 md:mb-0">
              <label class="block uppercase tracking-wide text-gray-700 text-sm font-bold mb-2" for="grid-zip">
                Postal code
              </label>
              <input class="appearance-none block w-full bg-gray-200 text-gray-700 border border-gray-200 rounded py-3 px-4 leading-tight focus:outline-none focus:bg-white focus:border-gray-500" 
              id="grid-zip" 
              type="text" 
              onChange={(e) => {setPostalCode(e.target.value);}}
              />
            </div> */}


            {/* <Map
              google={this.props.google}
              zoom={14}
              style={mapStyles}
              initialCenter={
                {
                  lat: -1.2884,
                  lng: 36.8233
                }
              }
            />
            AIzaSyBWcbR4iX_PUyxg3V7IVaBFD-nJvG6Xj1o */}
          </div>

          {/* Details */}
          {/* <div class="flex flex-wrap -mx-3 mb-6">
            <div class="w-full px-3">
              <label class="block uppercase font-oswald tracking-wide text-[#652605] text-xl font-bold mb-2" for="grid-details">
                Details (to be displayed)
              </label>
              <input class="appearance-none block w-full bg-gray-200 font-roboto text-gray-700 border border-gray-200 rounded py-3 px-4 mb-3 leading-tight focus:outline-none focus:bg-white focus:border-gray-500"
                id="grid-details"
                type="text"
                defaultValue={proposalDetails}
                onChange={(e) => {
                  setInfo(e.target.value);
                }}
              />
            </div>
          </div> */}

          <div className="border-t mb-8"></div>

          {/* Registration dates */}
          <div>
            <label class="block uppercase font-oswald tracking-wide text-[#652605] text-xl font-bold mb-6" for="grid-last-name">
              Registration dates
            </label>

            <div class="flex flex-wrap justify-center mb-6">
              <div class="w-full md:w-1/3 px-3">
                {/* <input class="appearance-none block w-full bg-gray-200 text-gray-700 border border-gray-200 rounded py-3 px-4 mb-3 leading-tight focus:outline-none focus:bg-white" id="grid-first-name" type="text" /> */}
                <div class="mb-4 font-roboto uppercase">
                  <EditRegDT
                    dataFromProposeNewEvent="Opens on"
                    currentValue={registrationOpensOn}
                    onChange={(e) => { setRegistrationOpensOn(e.target.value) }}
                  />

                </div>
                {/* <p class="text-red-500 text-xs italic">Please fill out this field.</p> */}
              </div>

              <div class="w-full md:w-1/3 px-3">
                {/* <input class="appearance-none block w-full bg-gray-200 text-gray-700 border border-gray-200 rounded py-3 px-4 mb-3 leading-tight focus:outline-none focus:bg-white focus:border-gray-500" id="grid-last-name" type="text" /> */}
                <div class="mb-4 font-roboto uppercase">
                  <EditRegDT
                    dataFromProposeNewEvent="Closes on"
                    currentValue={registrationClosesOn}
                    onChange={(e) => { setRegistrationClosesOn(e.target.value) }}
                  />
                </div>
              </div>
            </div>
          </div>

          <div className="border-t mb-8"></div>

          {/* Sessions */}
          <div class="mb-2">
            <div class="flex items-center mb-8">
              <label class="inline-block uppercase font-oswald tracking-wide text-[#652605] text-xl font-bold" for="grid-last-name">
                Sessions
              </label>
              {/* Add session button */}
              <button class="inline-block bg-[#f69d6e] hover:bg-[#f26f2a] rounded-xl font-oswald uppercase font-bold px-3 py-2 text-white ml-4" onClick={(e) => addSession(e)}>
                add a session
              </button>
            </div>

            {/* This div is for one session */}
            <div class="ml-3">
              {sessions.map((session) => {
                return <EditSessions
                  session={session}
                  key={session.session_id}
                  onStartDateChange={(e) => handleSessionStartTimeChange(session.session_id, e)}
                  onEndDateChange={(e) => handleSessionEndTimeChange(session.session_id, e)}
                  onCapacityChange={(e) => handleSessionCapacityChange(session.session_id, e)}
                  removeSessionChange={(e) => removeSession(session.session_id, e)}
                />
              })}
            </div>
          </div>

          <div className="border-t mb-8"></div>

          {/* Images */}
          <div class="flex flex-wrap -mx-3 mb-8">
            <div class="w-full px-3">
              <div class="flex items-center">
                <label class="inline-block uppercase font-oswald tracking-wide text-[#652605] text-xl font-bold">
                  Images
                </label>
                {/* Add image button */}
                <button class="inline-block bg-[#f69d6e] hover:bg-[#f26f2a] rounded-xl font-oswald uppercase font-bold px-3 py-2 text-white ml-4" onClick={(e) => addImage(e)} >
                  Add an image
                </button>
              </div>

              {/* Add image link */}
              <div>
                {tempImages.map(img => {
                  return <div>
                    <input class="appearance-none inline-block w-9/12 font-roboto bg-gray-200 mt-6 text-gray-700 border border-gray-200 rounded py-3 px-4 mb-3 leading-tight focus:outline-none focus:bg-white focus:border-gray-500"
                      key={img.id}
                      defaultValue={img.image}
                      type="text"
                      placeholder="Image link"
                      onChange={(e) => handleImageChange(img, e)}
                    ></input>
                    <button class="inline-block bg-red-400 hover:bg-red-600 rounded-xl font-oswald uppercase font-bold px-3 text-white ml-4 h-11" onClick={(e) => removeImage(img.id, e)} >
                      Remove &times;
                    </button>
                  </div>
                })}
              </div>

              {/* Commented off block to upload picture and use links currently */}
              {/* <input class="block w-full text-sm text-gray-900 bg-gray-200 rounded border border-gray-200 cursor-pointer focus:outline-none focus:bg-white focus:border-gray-500" aria-describedby="user_avatar_help" id="user_avatar" type="file" /> */}

            </div>
          </div>

          <div className="border-t mb-8"></div>

          {/* Tags */}
          <div class="flex flex-wrap -mx-3 mb-16">
            <div class="w-full px-3 mb-6 md:mb-0">
              <label class="block uppercase font-oswald tracking-wide text-[#652605] text-xl font-bold mb-2" for="grid-tags">
                Tags
              </label>
              <div class="relative mb-4">
                <select onChange={addTag} class="block appearance-none w-full bg-gray-200 border border-gray-200 text-gray-900 py-3 px-4 pr-8 rounded leading-tight focus:outline-none focus:bg-white focus:border-gray-500" id="grid-state">
                  <option>Physical</option>
                  <option>Virtual</option>
                  <option>Outdoor</option>
                  <option>Indoor</option>
                  <option>Interactive</option>
                  <option>Behind the scenes</option>
                  <option>Children</option>
                  <option>Elderly</option>
                  <option>Special needs</option>
                  <option>Donation drive</option>
                  <option>Charity walk</option>
                  <option>Marathon</option>
                  <option>Blood donation</option>
                  <option>Mentoring/Tuition</option>
                  <option>Coaching</option>
                </select>
              </div>

              {/* Display all the selected tags in the tags list, with a cross "button" to remove selected tags */}
              <ul>
                {tags.map(item => {
                  return <div class="bg-[#ec5a0d] text-white font-roboto font-bold rounded-lg inline-block py-1 px-4 ml-4">
                    <li class="inline-block">{item}</li> <p class="inline-block cursor-pointer text-white pl-3" onClick={() => removeTag(item)} > &times;</p>
                  </div>;
                })}
              </ul>
            </div>
          </div>

          <p className={submittedForm ? "mb-5" : "hidden"}>You have successfully submitted.</p>

          <div className="flex w-full justify-center">
            <button class="block bg-[#ec5a0d] hover:bg-[#ca4d0b] rounded-xl font-oswald uppercase font-bold text-4xl p-4 px-8 text-white ml-4" onClick={(e) => updateEvent(e)} >
              RESUBMIT
            </button>
          </div>
        </form>
      </div>
    </div>
  )
}

export default EditEvent;
