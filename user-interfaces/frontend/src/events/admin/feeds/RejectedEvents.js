import React, { Component } from "react";
import AdminEventCard from "./AdminEventCard";
import LoggedInUser from "../../../apis/LoggedInUser";
// import EventsApi from "../../../apis/EventsApi";

class RejectedEvents extends Component {
  constructor(props) {
    super(props);
    console.log(this.props); // props will get logged.
    this.state = {
      all_events: [],
    };
  }
  
  componentDidMount() {
    console.log("mounting");
    this.loadEvents();
    console.log(this.state.all_events);
  }

  loadEvents() {
    console.log("pressed");
    new LoggedInUser().get("/events/rejected").then(
      (res) => {
        console.log(res)
        this.setState({
          all_events: res.data.data.events
        })
      }
    )
    console.log(this.state.all_events)

  }

  render() {
    return (
      <div>
        {/* Search bar */}
        <div class="flex flex-col gap-4 pt-32 h-full justify-center items-center">
          <div class="relative">
            <input type="text" class="h-14 w-96 pl-5 rounded z-0 focus:shadow focus:outline-none" placeholder="Search anything..." />
            <div class="absolute top-4 right-3">
              <i class="fa fa-search text-gray-400 z-20 hover:text-gray-500 pr-3"></i>
            </div>
          </div>
        </div>
        <div className="flex flex-row flex-wrap justify-center gap-10 mt-10 mb-12">
          {this.state.all_events.map((event) => (
            <AdminEventCard event={event} key={event.event_id} />
          ))}
        </div>
      </div>
    );
  }
}

export default RejectedEvents;