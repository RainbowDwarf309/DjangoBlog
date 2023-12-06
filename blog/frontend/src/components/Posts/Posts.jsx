import axios from 'axios';

const API_URL = 'http://localhost:8000';

const Posts = () => {
    const url = `${API_URL}/posts/`;
    const data = axios.get(url).then(response => response.data);
    console.log(data)
}


export default Posts