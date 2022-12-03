import axios from 'axios'
axios.defaults.withCredentials = true

class LoggedInAdmin {
    constructor() {
        return axios.create({
            withCredentials: true,
            baseURL: "https://api.teamvision.link"
        });
    }
}

export default LoggedInAdmin;