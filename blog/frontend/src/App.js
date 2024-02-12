import './App.css';
import {Route, Routes} from 'react-router-dom'
import {Navigation} from "./components/Navigation";
import Posts from "./components/Posts";
import Categories from "./components/Categories";
import PostDetail from "./components/PostDeatil"


function App() {
    return (
        <div className="App">
            <Navigation/>
            <Routes>
                <Route path="/" element={<Posts/>}/>
                <Route path="/post/:slug" element={<PostDetail/>}/>
                <Route path="/categories" element={<Categories/>}/>
            </Routes>
        </div>
    );
}

export default App;
