import React, {useState} from 'react'
import {Link} from 'react-router-dom'
import {ArrowLeftEndOnRectangleIcon, ArrowLeftStartOnRectangleIcon} from "@heroicons/react/24/solid";

export function Navigation() {
    const [logIn, useLogIn] = useState(false)

    return (
        <nav className="h-[50px] flex justify-between px-5 bg-teal-500 items-center text-white sticky top-0 z-50">
            <span className="font-bold">Django Blog</span>

            <span>
        <Link to="/" className="mr-8">Posts</Link>
        <Link to="/categories" className="mr-8">Categories</Link>
        <Link to="/create_post" className="mr-8">Create Post</Link>
        {logIn ? <Link to="/login" className="mr-8">Log in</Link> :
            <Link to="/logout"><a className="bg-black p-2 h-5 w-5">Log out</a></Link>}
      </span>
        </nav>
    )
}