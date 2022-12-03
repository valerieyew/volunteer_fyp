import React, { Component } from "react";
import ProposedEventCard from "./ProposedEventCard";
import LoggedInUser from "../../../apis/LoggedInUser";

class ProposedEvents extends Component {
  constructor(props) {
    super(props);
    console.log(this.props); // props will get logged.
    this.state = {
      all_events: [],
    };
  }
  componentDidMount() {
    console.log("mounting");
    // console.log(all_events);
    this.loadEvents();
  }

  // loadEvents() {
    //   // axios.get(
    //   //   "http://localhost:5000/enrolled").then((res) => {
    //   //     this.setState({
    //   //       all_events: res.data.reverse(),
    //   //     });
    //   //   });

  //   this.setState({
  //     all_events: [
  //       {
  //         id: 4,
  //         organizer_employee_id: "jane.doe",
  //         name: "Butterfly Habitat Enhancement@ Bishan Park",
  //         date: "26/06/2022",
  //         time: "09:00 AM– 11:00 AM",
  //         location:
  //           "1384 Ang Mo Kio Avenue 1 Pet & Koi Centre Singapore 569932",
  //         info: "The event will be cancelled in the event of wet weather. Please do not attend the event if you are feeling unwell. ",
  //         registration_opens_on: "2021-05-25T00:00:00",
  //         registration_closes_on: "2021-06-25T00:00:00",
  //         image: "https://images.unsplash.com/photo-1484704193309-27eaa53936a7?ixlib=rb-1.2.1&ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&auto=format&fit=crop&w=2070&q=80",
  //         tags: [
  //           {
  //             tag: "outdoor",
  //           },
  //         ],
  //         status: "Rejected",
  //         proposal_details:
  //           "In collaboration with National Parks Board (NParks)",
  //       },
  //       {
  //         id: 5,
  //         organizer_employee_id: "jane.doe",
  //         name: "Volunteering Activity @ Credit Counselling Singapore",
  //         date: "26/06/2022",
  //         time: "09:00 AM– 11:00 AM",
  //         location: "51 Cuppage Road #07-06 Singapore 229469",
  //         info: "Volunteers can educate adults about the use of their CPF Accounts and practical techniques on using credit responsibly and where to seek help for debt problems. They could also be educating youths about prioritizing their spending needs and the basic money concepts through games and videos.",
  //         registration_opens_on: "2021-05-25T00:00:00",
  //         registration_closes_on: "2021-06-25T00:00:00",
  //         image:"https://www.cdac.org.sg/wp-content/uploads/2019/06/Financial-Literacy-Day-1.jpg",
  //         tags: [
  //           {
  //             tag: "education",
  //           },
  //         ],
  //         status: "Pending",
  //         proposal_details:
  //           "In collaboration with Citibank, Citi-SMU, Credit Counselling Singapore, e2i, Institute for Financial Literacy, JA Singapore, SkillsFuture SG, and Southwest CDC.",
  //       },
  //       {
  //         id: 6,
  //         organizer_employee_id: "jane.doe",
  //         name: "Volunteering Activity @ St. Andrews Elderly Home",
  //         date: "1/07/2022",
  //         time: "09:00 AM– 12:00 PM",
  //         location: "51 Cuppage Road #07-06 Singapore 229469",
  //         info: "Volunteers can socialise with the elderly and play games with them.",
  //         registration_opens_on: "2021-05-25T00:00:00",
  //         registration_closes_on: "2021-06-25T00:00:00",
  //         image:"https://images.unsplash.com/photo-1513159446162-54eb8bdaa79b?ixlib=rb-1.2.1&ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&auto=format&fit=crop&w=2370&q=80",
  //         tags: [
  //           {
  //             tag: "education",
  //           },
  //         ],
  //         status: "Approved",
  //         proposal_details:
  //           "In collaboration with Citibank, Citi-SMU, Credit Counselling Singapore, e2i, Institute for Financial Literacy, JA Singapore, SkillsFuture SG, and Southwest CDC.",
  //       },
  //     ],
  //   });
  //   console.log(this.state.all_events);
  // }
  loadEvents() {
    console.log("pressed");
    new LoggedInUser().get("/events/proposed").then(
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
            {" "}
            <input
              type="text"
              class="h-14 w-96 pl-5 rounded z-0 focus:shadow focus:outline-none"
              placeholder="Search anything..."
            />
            <div class="absolute top-4 right-3">
              {" "}
              <i class="fa fa-search text-gray-400 z-20 hover:text-gray-500 pr-3"></i>{" "}
            </div>
          </div>
        </div>
        <div className="flex flex-row flex-wrap justify-center gap-10 mt-4 mb-12">
          {this.state.all_events.map((event) => (
            <ProposedEventCard event={event} key={event.id} />
          ))}
        </div>
      </div>
    );
  }
}

export default ProposedEvents;
