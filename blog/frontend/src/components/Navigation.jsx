import React, {useState, useEffect} from 'react'
import {Link} from 'react-router-dom'
import {ArrowLeftEndOnRectangleIcon, ArrowLeftStartOnRectangleIcon} from "@heroicons/react/24/solid";
import DropDownButton from "./buttons/DropDownButton"
import {LogoutButton} from "./buttons/LogoutButton";
import {LoginButton} from "./buttons/LoginButton";


export function Navigation() {
    const [logIn, setLogIn] = useState(false)

    function isAuthenticated() {
        const token = localStorage.getItem('token');
        return !!token;
    }


    useEffect(() => {
        setLogIn(isAuthenticated)
    }, []);

    return (
        <nav className="h-[50px] flex justify-between px-5 bg-teal-500 items-center text-white sticky top-0 z-50">
            <span className="font-bold">Django Blog</span>

            <span>
        <Link to="/"
              className="mr-8 rounded-md px-3 py-2 text-sm font-semibold text-white ring-inset ring-teal-900 hover:bg-teal-700">Posts</Link>
        <Link to="/categories"
              className="mr-8 rounded-md px-3 py-2 text-sm font-semibold text-white ring-inset ring-teal-900 hover:bg-teal-700">Categories</Link>
        <Link to="/create_post"
              className="mr-8 rounded-md px-3 py-2 text-sm font-semibold text-white ring-inset ring-teal-900 hover:bg-teal-700">Create Post</Link>
        <DropDownButton/>
                {logIn ? <LogoutButton/> : <LoginButton/>}
      </span>
        </nav>
    )
}