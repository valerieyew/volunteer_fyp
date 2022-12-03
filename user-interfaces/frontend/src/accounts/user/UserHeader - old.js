import React from "react";
import { NavLink, Link } from "react-router-dom";

function UserHeader({toggleBrowse, toggleEnrolled, toggleProposed, toggleProposeNew, browseSelected, enrolledSelected, proposedSelected, proposeNewSelected}) {

    return (
        <div>
            {/* Navbar for logo */}
            <nav className="fixed z-50 flex flex-col h-20 px-6 bg-gradient-to-r from-[#ffa53b] to-[#f6c790] w-full">
                <div className="flex flex-row">
                    <div className="self-center mr-2">
                        <a href="/home"><img className="h-10 w-10 absolute left-4 top-4" src={process.env.PUBLIC_URL + '/CS Logoooo.PNG'} alt="Credit Suisse Logo" /></a>
                    </div>
                    <div>
                        {/* relative for nav and absolute for the individual texts to set their positions */}
                        <a href="/home" className="text-xl no-underline text-[#013156] font-bold absolute left-16 top-4">Credit Suisse</a><br />
                        <a href="/home" className="text-s text-[#013156] absolute left-24 top-10">Volunteer</a>
                    </div>
                </div>

                <div className="sm:mb-0 self-end pr-5 pt-1">
                    <Link to="/browse" className={browseSelected ? "font-bold drop-shadow-md text-md no-underline text-[#013156] ml-8 mt-2 px-4 py-1 rounded-lg hover:text-[#013156]" 
                    :"text-md no-underline text-[#013156] hover:text-[#b27329] ml-8"} onClick={toggleBrowse}>Browse</Link>
                    <Link to="/enrolled" className={enrolledSelected ? "font-bold drop-shadow-md text-md no-underline text-[#013156] ml-8 px-4 py-1 rounded-lg hover:text-[#013156]" 
                    : "text-md no-underline text-[#013156] hover:text-[#b27329] ml-8"} onClick={toggleEnrolled}>Enrolled</Link>
                    <Link to="/proposed" className={proposedSelected ? "font-bold drop-shadow-md text-md no-underline text-[#013156] ml-8 px-4 py-1 rounded-lg hover:text-[#013156]" 
                    : "text-md no-underline text-[#013156] hover:text-[#b27329] ml-8"} onClick={toggleProposed}>Proposed</Link>
                    <Link to="/new" className={proposeNewSelected? "bg-[#ffa53b] text-[#013156] font-bold text-md ml-8 py-1 px-4"
                    : "bg-[#e2b988] hover:bg-[#ffa53b] text-[#013156] font-bold text-md ml-8 py-1 px-4"} onClick={toggleProposeNew}>+ New</Link>
                    <a href="/login" className="text-md no-underline text-[#013156] hover:text-[#b27329] ml-8">Log out</a>
                </div>
               
            </nav>

            {/* Search bar
            <div className="flex mt-10 justify-center items-center">
                <div className="relative"> <input type="text" className="h-14 w-96 pl-5 rounded z-0 focus:shadow focus:outline-none" placeholder="Search anything..." />
                    <div className="absolute top-4 right-3"> <i className="fa fa-search text-gray-400 z-20 hover:text-gray-500 pr-3"></i> </div>
                </div>
            </div> */}
        </div>)
}

export default UserHeader;
