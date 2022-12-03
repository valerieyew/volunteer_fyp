import React from "react";
import { Switch } from '@headlessui/react'
import LoginApi from "../apis/LoginApi";
import CSLogo from "../assets/img/CSLogo.png"

class Login extends React.Component {

  // constructor(props) {
  //   super(props);
  //   this.state = {
  //     toggleAdmin: props.toggleAdmin,
  //     invalidDetails: props.invalidDetails,
  //     isNotAdmin: props.isNotAdmin
  //   }
  // }

  state = {
    email: "",
    password: "",
    toggleAdmin: false,
    invalidDetails: false,
    isNotAdmin: false
  };

  handleToggle = () => {
    this.setState({ toggleAdmin: !this.state.toggleAdmin })
  };

  handleInvalidDetails = () => {
    this.setState({ invalidDetails: true })
    this.setState({ isNotAdmin: false })
  };

  handleIsNotAdmin = () => {
    this.setState({ isNotAdmin: true })
    this.setState({ invalidDetails: false })
  };


  onSignIn = async (event) => {
    event.preventDefault();
    console.log("user sign in pressed");
    await LoginApi.get("/login", {
      auth: {
        username: this.state.email,
        password: this.state.password
      }
    })
      .then((res) => {
        console.log(res)
        if (res.status === 200) {
          if (this.state.toggleAdmin) {
            console.log("TOGGLED ADMIN")
            if (res.data.message.role === "admin") {
              localStorage.setItem("isAuthenticatedAdmin", "true");
              this.props.history.push("/admin/home")
            } else {
              this.handleIsNotAdmin()
            }
          } else {
            localStorage.setItem("isAuthenticated", "true");
            this.props.history.push("/browse")
          }
          this.setState({ flag: 0 });
        }
      }

      ).catch((err) => {
        this.setState({ flag: 1 });
        console.log(err.response)
        this.handleInvalidDetails()
      })
  }

  render() {
    return (
      <div className={`${this.state.toggleAdmin ? "bg-[#75a7cc]" : "bg-[#f4864c]"}
      absolute top-0 w-full h-full`}
      >

        {/* Navbar for logo */}
        <nav className="relative flex flex-col pt-2 px-6 bg-white/0 w-full">
          <div className="absolute flex flex-col justify-start mt-2">
            <a href="/browse"><img className="h-10 w-auto" src={CSLogo} alt="Credit Suisse Logo" /></a>
            <a href="/browse" className="pt-1 mr-6 text-center font-spectral uppercase text-s text-[#013156]">Volunteer</a>
            <div>
              {/* relative for nav and absolute for the individual texts to set their positions */}
              {/* <a href="/browse" className="font-spectral text-2xl no-underline text-[#013156] font-bold absolute left-16 top-4">Credit Suisse</a><br /> */}
            </div>
          </div>
        </nav>

        {/* Sign in form */}
        <div className="relative container mx-auto h-full">
          <div className="flex items-center justify-center h-full">
            <div className="lg:w-4/12 px-4">
              <div className="rounded-lg bg-white pt-8">

                {/* "Sign in with" and horizontal rule */}
                {/* <div className="rounded-t p-6 pb-3">
                  <h6 className="text-center font-oswald uppercase text-blueGray-500 text-lg font-bold">Sign in</h6>
                  <hr className="mt-4 border-b-1 border-blueGray-300" />
                </div> */}

                <div className={`${this.state.invalidDetails ? "mx-8 text-xs text-red-600" : "hidden"}`}
                >
                  The email or password that you have entered is invalid. Please try again.
                </div>

                <div className={`${this.state.isNotAdmin ? "mx-8 text-xs text-red-600" : "hidden"}`}
                >
                  You are not an authorised Administrator.
                </div>

                <div className="flex-auto px-4 lg:px-10 py-10 pt-0">

                  <div className="flex py-6 items-center">
                    <Switch
                      // checked={enabled}
                      onChange={this.handleToggle}
                      className={`${this.state.toggleAdmin ? 'bg-[#2a7cc0]' : 'bg-[#f4d1bd]'} 
                    relative inline-flex flex-shrink-0 h-[28px] w-[52px] border-2 border-transparent rounded-full cursor-pointer transition-colors ease-in-out duration-200 
                    focus:outline-none focus-visible:ring-2 focus-visible:ring-white focus-visible:ring-opacity-75`}
                    >
                      <span className="sr-only">Use setting</span>
                      <span
                        aria-hidden="true"
                        className={`${this.state.toggleAdmin ? 'translate-x-6' : 'translate-x-0'}
                      pointer-events-none inline-block h-[24px] w-[24px] rounded-full bg-white shadow-lg transform ring-0 transition ease-in-out duration-200`}
                      />
                    </Switch>

                    <div className={`${this.state.toggleAdmin ? 'text-blueGray-800 font-oswald text-base uppercase' : 'text-blueGray-300 font-oswald text-base uppercase'}
                    ml-3 text-sm font-bold`}>Admin Sign In</div>
                  </div>


                  <form className="flex flex-col pt-3 md:pt-3">
                    {/* Email Address  */}
                    <div className="relative w-full mb-3">
                      <label className="block text-blueGray-600 font-roboto text-xs font-bold mb-2">Email Address</label>
                      <input
                        className="border-0 px-3 py-3 placeholder-blueGray-300 font-roboto text-blueGray-600 bg-blueGray-100 rounded text-sm shadow focus:ring w-full ease-linear transition-all duration-150"
                        type="text"
                        name="email"
                        placeholder="john.doe@email.com"
                        onChange={(e) => {
                          this.setState({ email: e.target.value });
                        }}

                      />
                    </div>

                    {/* Password */}
                    <div className="relative w-full mb-3">
                      <label className="block text-blueGray-600 text-xs font-roboto font-bold mb-2">Password</label>
                      <input
                        className="border-0 px-3 py-3 placeholder-blueGray-300 font-roboto text-blueGray-600 bg-blueGray-100 rounded text-sm shadow focus:ring w-full ease-linear transition-all duration-150"
                        type="password"
                        name="email"

                        placeholder="yourpassword"
                        onChange={(e) => {
                          this.setState({ password: e.target.value });
                        }}
                      />
                    </div>

                    {/* Forgot password */}
                    <div className="text-right">
                      <a
                        href="#pablo"
                        onClick={(e) => e.preventDefault()}
                        className="text-blueGray-400 font-roboto"
                      >
                        <small>Forgot password?</small>
                      </a>
                    </div>

                    {/* Sign in button */}
                    <div className="text-center mt-6">
                      <button type="submit"
                        className="bg-[#013156] font-oswald text-white active:bg-blueGray-600 text-xl font-bold uppercase px-6 py-3 rounded shadow hover:shadow-lg outline-none focus:outline-none mr-1 mb-1 w-full ease-linear transition-all duration-150"
                        onClick={this.onSignIn}
                      >
                        Sign In
                      </button>
                    </div>
                  </form>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    );
  }
}

export default Login;
