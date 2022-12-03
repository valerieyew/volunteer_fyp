import React from "react";
import { NavLink, Link } from "react-router-dom";

function AdminHeader({togglePending, toggleApproved, toggleRejected, pendingSelected, approvedSelected, rejectedSelected }) {

    return (
        <div>
            {/* Navbar for logo */}
            <nav className="fixed z-50 flex flex-col h-24 px-6 bg-gradient-to-r from-[#2a7cc0] to-[#90abf6] w-full">
                <div className="flex flex-row">
                    <div className="self-center mr-2">
                        <a href="/admin/home"><img className="h-10 w-10 absolute left-4 top-6" src={process.env.PUBLIC_URL + '/CS Logoooo.PNG'} alt="Credit Suisse Logo" /></a>
                    </div>
                    <div>
                        {/* relative for nav and absolute for the individual texts to set their positions */}
                        <a href="/admin/home" className="text-2xl no-underline text-[#013156] font-bold absolute left-16 top-4">Credit Suisse</a><br />
                        <a href="/admin/home" className="text-s text-[#013156] absolute left-24 top-12">Volunteer</a>
                    </div>
                </div>

                <div className="sm:mb-0 self-end pt-1 pr-5">
                <Link to="/admin/home" className={pendingSelected ? "shadow-md text-lg no-underline text-[#013156] ml-8 px-4 py-2 mt-2 rounded-lg bg-gray-200/[0.6] hover:bg-gray-200 hover:text-[#013156]" 
                :"text-lg no-underline text-[#013156] ml-8 px-4 py-2 mt-2 rounded-lg hover:bg-gray-200 hover:text-[#013156]"} onClick={togglePending}>Pending</Link>
                <Link to="/admin/approved" className={approvedSelected ? "shadow-md text-lg no-underline text-[#013156] ml-8 px-4 py-2 mt-2 rounded-lg bg-gray-200 hover:bg-gray-200 hover:text-[#013156]" 
                : "text-lg no-underline text-[#013156] ml-8 px-4 py-2 mt-2 rounded-lg hover:bg-gray-200 hover:text-[#013156]"} onClick={toggleApproved}>Approved</Link>
                <Link to="/admin/rejected" className={rejectedSelected ? "shadow-md text-lg no-underline text-[#013156] ml-8 px-4 py-2 mt-2 rounded-lg bg-gray-200 hover:bg-gray-200 hover:text-[#013156]" 
                : "text-lg no-underline text-[#013156] ml-8 px-4 py-2 mt-2 rounded-lg hover:bg-gray-200 hover:text-[#013156]"} onClick={toggleRejected}>Rejected</Link>
                    <button className="bg-[#c5e6ff] hover:bg-[#81c6fa] text-[#013156] font-bold ml-8 py-2 px-4 rounded-full">+ New</button>
                    <a href="/login" className="text-lg no-underline text-[#013156] ml-8 px-4 py-2 mt-2 rounded-lg hover:bg-gray-200 hover:text-[#013156]">Log out</a>
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

export default AdminHeader;
