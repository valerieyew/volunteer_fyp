import axios from 'axios'

export default axios.create({
    baseURL: "https://api.teamvision.link",
    withCredentials: true,
})
