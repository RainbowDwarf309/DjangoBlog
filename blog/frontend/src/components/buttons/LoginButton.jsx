import React from 'react';
import {Link} from "react-router-dom";


export function LoginButton() {


    return (
        <Link to="/login" className="bg-black p-2 h-5 w-5">
            <button>
                Log in
            </button>
        </Link>

    )
}
