import axios from 'axios'
axios.defaults.withCredentials = true

class LoggedInTest {
    constructor() {
        return axios.create({
            withCredentials: true,
            baseURL: "https://api.teamvision.link"
        });
    }
}

export default LoggedInTest;