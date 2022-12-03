import React, { useState } from "react";
import { Transition } from "@headlessui/react";
import { NavLink, useHistory } from "react-router-dom";
import LoginApi from "../../apis/LoginApi";
import CSLogo from "../../assets/img/CSLogo.png"


function Nav({ togglePending, toggleApproved, toggleRejected, pendingSelected, approvedSelected, rejectedSelected }) {
  const [isOpen, setIsOpen] = useState(false);
  const history = useHistory();

  function handleLogout(e) {
    LoginApi.post("/logout", {
    })
      .then((res) => {
        console.log("ADMIN LOGOUT CLEARED");
        localStorage.clear();
        history.push('/');
        window.location.reload();
      })
      .catch((err) => {
        console.log(err);
      })
  }

  return (
    <div>
      <nav className="fixed w-full z-50 bg-[#75a7cc]">
        <div className="w-full mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex items-center justify-between h-20">
          <div className="flex flex-col justify-start">
                <a href="/browse"><img className="h-8 w-auto" src={CSLogo} alt="Credit Suisse Logo" /></a>
                <a href="/browse" className="pt-2 mr-6 text-center font-spectral uppercase text-xs text-[#013156]">Volunteer</a>
            </div>
            <div className="flex items-center">
              <div className="hidden md:block">
                <div className="ml-10 flex gap-x-10 items-baseline text-right">

                  <NavLink
                    to="/admin/home"
                    className={pendingSelected ?
                      "font-oswald font-bold text-xl text-[#1c394e] uppercase"
                      : "font-oswald font-bold text-xl text-white uppercase hover:text-[#1c394e]"}
                    onClick={togglePending}
                  > Pending
                  </NavLink>

                  <NavLink to="/admin/approved" className={approvedSelected ?
                    "font-oswald font-bold text-xl text-[#1c394e] uppercase"
                    : "font-oswald font-bold text-xl text-white uppercase hover:text-[#1c394e]"}
                    onClick={toggleApproved}
                  > Approved
                  </NavLink>

                  <NavLink to="/admin/rejected" className={rejectedSelected ?
                    "font-oswald font-bold text-xl text-[#1c394e] uppercase"
                    : "font-oswald font-bold text-xl text-white uppercase hover:text-[#1c394e]"}
                    onClick={toggleRejected}
                  > Rejected
                  </NavLink>

                  <button
                    className="font-oswald font-normal text-md text-white uppercase underline underline-offset-2 hover:text-[#1c394e]"
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
                className="bg-gray-100/[0.2] inline-flex items-center justify-center p-2 rounded-md text-white hover:text-white hover:bg-gray-500 focus:outline-none focus:ring-white"
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
              <div ref={ref} className="px-2 pt-2 pb-3 space-y-1 sm:px-3 text-center">
                <NavLink
                  to="/admin/home"
                  className={pendingSelected ? "drop-shadow-md text-md no-underline block text-[#013156] px-4 py-2 mt-2 mx-2 rounded-lg font-bold"
                    : "text-md no-underline text-[#013156] block px-4 py-2 mt-2 mx-2 rounded-lg"} onClick={togglePending}
                >Pending
                </NavLink>

                <NavLink to="/admin/approved" className={approvedSelected ? "drop-shadow-md text-md no-underline block text-[#013156] px-4 py-2 mt-2 mx-2 rounded-lg font-bold"
                  : "text-md no-underline text-[#013156] block px-4 py-2 mt-2 mx-2 rounded-lg"} onClick={toggleApproved}
                >Approved</NavLink>

                <NavLink to="/admin/rejected" className={rejectedSelected ? "drop-shadow-md text-md no-underline block text-[#013156] px-4 py-2 mt-2 mx-2 rounded-lg font-bold"
                  : "text-md no-underline text-[#013156] block px-4 py-2 mt-2 mx-2 rounded-lg"} onClick={toggleRejected}
                >Rejected</NavLink>

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

export default Nav;