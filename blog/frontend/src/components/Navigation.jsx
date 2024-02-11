import React, {useState} from 'react'
import {Link} from 'react-router-dom'

export function Navigation() {
    const [logIn, useLogIn] = useState(false)

    return (
        <nav className="h-[50px] flex justify-between px-5 bg-teal-500 items-center text-white">
            <span className="font-bold">Django Blog</span>

            <span>
        <Link to="/" className="mr-2">Posts</Link>
        <Link to="/categories" className="mr-2">Categories</Link>
        <Link to="/create_post" className="mr-2">Create Post</Link>
        {logIn ? <Link to="/login" className="mr-2">Log in</Link> : <Link to="/logout" className="mr-2">Log out</Link>}
        <Link to="/about">About</Link>
      </span>
        </nav>
    )
}