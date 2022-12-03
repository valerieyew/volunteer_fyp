import React, { Component } from "react";
import EventCard from "./EventCard";
import LoggedInUser from "../../../apis/LoggedInUser";
import BeatLoader from "react-spinners/BeatLoader";

class BrowseEvents extends Component {
  constructor(props) {
    super(props);
    console.log(this.props); // props will get logged.
    this.state = {
      all_events: [],
      loading: false,
      tag: ""
    };
  }

  componentDidMount() {
    console.log("mounting");
    this.setState({loading: true});
    this.loadEvents();
    setTimeout(() => this.setState({ loading: false}), 1500)
    console.log(this.state.all_events);
  }

  // loadEvents = async () => {
  //   console.log("pressed");
  //   await EventsApi.get("/events")
  //     .then((res) => {
  //       console.log(res)
  //       if (res.status === 200) {
  //         console.log("YAY")
  //       }
  //     }
  //     ).catch((err) => {
  //       console.log(err.response)
  //     })
  // }

  loadEvents() {
    console.log("pressed");
    new LoggedInUser().get("/events").then(
      (res) => {
        console.log(res)
        this.setState({
          all_events: res.data.data.events
        })
      }
    )
    console.log(this.state.all_events)
  }
  loadTagEvents(e){
    console.log(e);
    if (e === ""){
      new LoggedInUser().get("/events").then(
        (res) => {
          console.log(res)
          this.setState({
            all_events: res.data.data.events
          })
        }
      )
    } else {
      new LoggedInUser().get("/events/" + e).then(
        (res) => {
          console.log(res)
          this.setState({
            all_events: res.data.data.events
          })
        }
      )
      console.log(this.state.all_events)
    }
   
  }

  // loadEvents() {
  //   // console.log("LOADING EVENTS");
  //   // axios.get(
  //   //   "http://localhost:31000/events",).then((res) => {
  //   //     this.setState({
  //   //       all_events: res.data.reverse(),
  //   //     });
  //   //   });
  //   console.log("getting mocked data");
  //   this.setState({
  //     all_events: [
  //       {
  //         "id": 1,
  //         "organizer_employee_id": "jane.doe",
  //         "name": "Volunteering Activity @ Sun Plaza Park",
  //         "date": "20/03/2021",
  //         "time": "09:00 AM– 11:00 AM",
  //         "location": "407 Tampines Street 41 Sun Plaza Green Singapore 520407",
  //         "info_for_participants": "The event will be cancelled in the event of wet weather. ",
  //         "registration_opens_on": "2021-03-10T00:00:00",
  //         "registration_closes_on": "2021-03-17T00:00:00",
  //         "capacity": 10,
  //         "fill": 2,
  //         "image": "https://pbs.twimg.com/media/Dap2TNXWAAAXn8i.jpg",
  //         "tags": "outdoor"
  //       },
  //       {
  //         "id": 2,
  //         "organizer_employee_id": "jane.doe",
  //         "name": "Morning Walk / Walk For Rice @ Kallang",
  //         "date": "16/01/2022",
  //         "time": "07:00 AM– 11:00 AM",
  //         "location": "8 Stadium Boulevard Home of Athletics (HOA) Singapore 397804",
  //         "info_for_participants": "Volunteers are required to assist the Kallang ActiveSG team in the following:",
  //         "registration_opens_on": "2021-12-29T00:00:00",
  //         "registration_closes_on": "2022-01-12T00:00:00",
  //         "capacity": 30,
  //         "fill": 1,
  //         "image": "https://pbs.twimg.com/media/Dap2TNXWAAAXn8i.jpg",
  //         "tags": "outdoor"
  //       },
  //       {
  //         "id": 3,
  //         "organizer_employee_id": "jane.doe",
  //         "name": "Dog Walking @ Pasir Ris Dog Shelter",
  //         "date": "30/01/2022",
  //         "time": "07:00 AM– 11:00 AM",
  //         "location": "Pasir Ris Park Singapore 397804",
  //         "info_for_participants": "Please join us to walk these cute dogs! ",
  //         "registration_opens_on": "2021-12-29T00:00:00",
  //         "registration_closes_on": "2022-01-12T00:00:00",
  //         "capacity": 30,
  //         "fill": 1,
  //         "image": "https://images.unsplash.com/photo-1582118315271-53d7fd6630e1?ixlib=rb-1.2.1&ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&auto=format&fit=crop&w=2370&q=80",
  //         "tags": "outdoor"
  //       }
  //     ],
  //   });
  //   console.log(this.state.all_events)
  // }
   // add the selected tag to the list
    // addTag() {
    //   this.setState({
    //     tags : String
    //   })
    // setTags([...tags, String(event.target.value)]);
    // }

  render() {
    return (
      <div>
        {this.state.loading ?
      <div className="flex flex-col gap-4 m-auto justify-center items-center h-screen">
      <BeatLoader size={40} color={"#ffa53b"} loading={this.state.loading} speedMultiplier={1.5} />
      </div>
          :

        <div class="flex flex-col gap-4 pt-32 h-full justify-center items-center">
          {/* <div class="relative">
            <input type="text" class="h-14 w-96 pl-5 rounded z-0 focus:shadow focus:outline-none" placeholder="Search anything..." />
            <div class="absolute top-4 right-3">
              <i class="fa fa-search text-gray-400 z-20 hover:text-gray-500 pr-3"></i>
            </div>
          </div> */}
          <div class="flex flex-wrap -mx-3 mb-16">
            <div class="w-full px-3 mb-6 md:mb-0">
              <label class="block uppercase text-gray-700 text-sm font-bold mb-2" for="grid-tags">
                Tags
              </label>
              <div class="relative mb-2">
                <select onChange={(e) => {
                          this.setState({ tag: e.target.value });
                          this.loadTagEvents(e.target.value);
                        }} class="block appearance-none w-full bg-gray-200 border border-gray-200 text-gray-900 py-3 px-4 pr-8 rounded leading-tight focus:outline-none focus:bg-white focus:border-gray-500" id="grid-state">
                  <option value="">--Select a tag--</option>
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
            
            </div>
          </div>
          <div className="flex flex-row flex-wrap justify-center gap-10 mt-4 mb-12">
            {this.state.all_events.map((event) => (
              <EventCard event={event} key={event.event_id} />
            ))}
          </div>
        </div>
        }
      </div>
    );
  }
}

export default BrowseEvents;