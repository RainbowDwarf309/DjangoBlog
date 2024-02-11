import './App.css';
import {Route, Routes} from 'react-router-dom'
import {Navigation} from "./components/Navigation";
import Posts from "./components/Posts";
import Categories from "./components/Categories";


function App() {
    return (
        <div className="App">
            <Navigation/>
            <Routes>
                <Route path="/" element={<Posts/>}/>
                <Route path="/categories" element={<Categories/>}/>
            </Routes>
            {/*<Posts/>*/}
        </div>
    );
}

export default App;
