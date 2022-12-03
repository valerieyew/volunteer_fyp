import React, { useState } from "react";
import { Transition } from "@headlessui/react";
import { NavLink, useHistory, Redirect } from "react-router-dom";
import createHistory from 'history/createBrowserHistory';
import LoginApi from "../../apis/LoginApi";
import { useStateManager } from "react-select";
import CSLogo from "../../assets/img/CSLogo.png"


function UserHeader({ toggleBrowse, toggleEnrolled, toggleProposed, toggleProposeNew, browseSelected, enrolledSelected, proposedSelected, proposeNewSelected }) {
  const [isOpen, setIsOpen] = useState(false);
  const history = useHistory();

  function handleLogout(e) {
    LoginApi.post("/logout", {
    })
      .then((res) => {
        console.log("LOGOUT CLEARED");
        localStorage.clear();
        window.location.pathname = '/';
      })
      .catch((err) => {
        console.log(err);
      })
  }
  return (
    <div>
      <nav className="fixed w-full z-50 bg-[#f4864c]">
        <div className="w-full mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex items-center justify-between h-20">
            <div className="flex flex-col justify-start">
                <a href="/browse"><img className="h-8 w-auto" src={CSLogo} alt="Credit Suisse Logo" /></a>
                <a href="/browse" className="pt-2 mr-6 text-center font-spectral uppercase text-xs text-[#013156]">Volunteer</a>
            </div>
            <div className="flex items-center">
              <div className="hidden md:block">
                <div className="ml-10 flex gap-x-10 items-baseline text-right">

                  <NavLink to="/browse"
                    className={browseSelected ?
                      "font-oswald font-bold text-xl text-[#652605] uppercase"
                      : "font-oswald font-bold text-xl text-white uppercase hover:text-[#652605]"}
                    onClick={toggleBrowse}
                  > Browse
                  </NavLink>

                  <NavLink to="/enrolled"
                    className={enrolledSelected ?
                      "font-oswald font-bold text-xl text-[#652605] uppercase"
                      : "font-oswald font-bold text-xl text-white uppercase hover:text-[#652605]"}
                    onClick={toggleEnrolled}
                  > Enrolled
                  </NavLink>

                  <NavLink to="/proposed"
                    className={proposedSelected ?
                      "font-oswald font-bold text-xl text-[#652605] uppercase"
                      : "font-oswald font-bold text-xl text-white uppercase hover:text-[#652605]"}
                    onClick={toggleProposed}
                  > Proposed
                  </NavLink>

                  {/* <NavLink to="/new"
                    className={proposeNewSelected ?
                      "font-oswald font-semibold text-xl text-[#652605] uppercase underline underline-offset-4 decoration-2"
                      : "font-oswald font-semibold text-xl text-white uppercase hover:text-[#652605] underline underline-offset-4 decoration-2"}
                    onClick={toggleProposeNew}
                  > + New
                  </NavLink> */}

                  <NavLink to="/new"
                    className={proposeNewSelected ?
                      "flex gap-1 items-baseline font-oswald font-semibold text-lg text-white uppercase p-2 px-4 rounded-2xl bg-[#a84009]"
                      : "flex gap-1 items-baseline font-oswald font-semibold text-lg text-white uppercase p-2 px-4 rounded-2xl  bg-[#ca4d0b] hover:bg-[#a84009]"}
                    onClick={toggleProposeNew}
                  >
                    <svg xmlns="http://www.w3.org/2000/svg" className="h-4 w-4" viewBox="0 0 20 20" fill="currentColor">
                      <path fillRule="evenodd" d="M10 3a1 1 0 011 1v5h5a1 1 0 110 2h-5v5a1 1 0 11-2 0v-5H4a1 1 0 110-2h5V4a1 1 0 011-1z" clipRule="evenodd" />
                    </svg>
                    <div> New </div>
                  </NavLink>

                  <button
                    className="font-oswald font-normal text-md text-white uppercase underline underline-offset-2 hover:text-[#652605]"
                    onClick={handleLogout}
                  > Logout
                  </button>
                </div>
              </div>
            </div>
            <div className="-mr-2 flex md:hidden">
              <button
                onClick={() => setIsOpen(!isOpen)}
                type="button"
                className=" inline-flex items-center justify-center p-2 rounded-md text-#013156 hover:text-[#013156] hover:bg-gray-200 focus:outline-none focus:ring-white"
                aria-controls="mobile-menu"
                aria-expanded="false"
              >
                <span className="sr-only">Open main menu</span>
                {!isOpen ? (
                  <svg
                    className="block h-6 w-6"
                    xmlns="http://www.w3.org/2000/svg"
                    fill="none"
                    viewBox="0 0 24 24"
                    stroke="currentColor"
                    aria-hidden="true"
                  >
                    <path
                      strokeLinecap="round"
                      strokeLinejoin="round"
                      strokeWidth="2"
                      d="M4 6h16M4 12h16M4 18h16"
                    />
                  </svg>
                ) : (
                  <svg
                    className="block h-6 w-6"
                    xmlns="http://www.w3.org/2000/svg"
                    fill="none"
                    viewBox="0 0 24 24"
                    stroke="currentColor"
                    aria-hidden="true"
                  >
                    <path
                      strokeLinecap="round"
                      strokeLinejoin="round"
                      strokeWidth="2"
                      d="M6 18L18 6M6 6l12 12"
                    />
                  </svg>
                )}
              </button>
            </div>
          </div>
        </div>

        <Transition
          show={isOpen}
          enter="transition ease-out duration-100 transform"
          enterFrom="opacity-0 scale-95"
          enterTo="opacity-100 scale-100"
          leave="transition ease-in duration-75 transform"
          leaveFrom="opacity-100 scale-100"
          leaveTo="opacity-0 scale-95"
        >
          {(ref) => (
            <div className="md:hidden" id="mobile-menu">
              <div ref={ref} className="px-2 pt-2 pb-3 space-y-1 sm:px-3 text-center justify-items-center">
                <NavLink
                  to="/browse"
                  className={browseSelected ? "drop-shadow-md text-md no-underline block text-[#013156] px-4 py-2 mt-2 mx-2 rounded-lg font-bold"
                    : "text-md no-underline text-[#013156] block px-4 py-2 mt-2 mx-2 rounded-lg"} onClick={toggleBrowse}
                >Browse
                </NavLink>

                <NavLink to="/enrolled" className={enrolledSelected ? "drop-shadow-md text-md no-underline block text-[#013156] px-4 py-2 mt-2 mx-2 rounded-lg font-bold"
                  : "text-md no-underline text-[#013156] block px-4 py-2 mt-2 mx-2 rounded-lg"} onClick={toggleEnrolled}
                >Enrolled</NavLink>

                <NavLink to="/proposed" className={proposedSelected ? "drop-shadow-md text-md no-underline block text-[#013156] px-4 py-2 mt-2 mx-2 rounded-lg font-bold"
                  : "text-md no-underline text-[#013156] block px-4 py-2 mt-2 mx-2 rounded-lg"} onClick={toggleProposed}
                >Proposed</NavLink>

                <NavLink to="/new" className={proposeNewSelected ? "block text-[#013156] font-bold text-md ml-8 py-1 px-4"
                  : "block text-[#013156] text-md py-1 px-4"} onClick={toggleProposeNew}>+ New</NavLink>
                <div className="block text-md no-underline text-[#013156] px-4 py-1 mt-2 rounded-lg"
                  onClick={handleLogout}
                >Log out</div>

              </div>
            </div>
          )}
        </Transition>
      </nav>
    </div>
  );
}

export default UserHeader;