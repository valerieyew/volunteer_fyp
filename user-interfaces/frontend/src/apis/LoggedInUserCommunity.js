import axios from 'axios'
axios.defaults.withCredentials = true

class LoggedInUserCommunity {
    constructor() {
        return axios.create({
            withCredentials: true,
            baseURL: "https://api.teamvision.link"
        });
    }
}

export default LoggedInUserCommunity;