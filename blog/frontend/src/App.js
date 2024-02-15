import React from "react";
import './App.css';
import {Route, Routes} from 'react-router-dom'
import {Navigation} from "./components/Navigation";
import Posts from "./components/Posts";
import Categories from "./components/Categories";
import PostDetail from "./components/PostDeatil"
import CategoryDetail from "./components/CategoryDetail"
import LoginForm from "./components/forms/LoginForm";
import RegistrationForm from "./components/forms/RegistrationForm";
import TagDetail from "./components/TagDetail";
import CreatePostForm from "./components/forms/CreatePostForm";


function App() {
    return (
        <div className="App">
            <Navigation/>
            <Routes>
                <Route path="/" element={<Posts url={'/posts/'}/>}/>
                <Route path="/post/:slug" element={<PostDetail/>}/>
                <Route path="/categories" element={<Categories/>}/>
                <Route path="/create_post" element={<CreatePostForm/>}/>
                <Route path="/category/:slug" element={<CategoryDetail/>}/>
                <Route path="/tag/:slug" element={<TagDetail/>}/>
                <Route path="/login" element={<LoginForm/>}/>
                <Route path="/registration" element={<RegistrationForm/>} />
            </Routes>
        </div>
    );
}

export default App;
