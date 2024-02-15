import React from 'react';
import {Link} from "react-router-dom";


export function LogoutButton() {
    function logout() {
        // Удаление токена из localStorage
        localStorage.removeItem('token');

        // Осуществление дополнительных действий при выходе пользователя, например, редирект.
    }

    return (
        <Link to="/logout" onClick={logout} className="bg-black p-2 h-5 w-5">
            <button>
                Log out
            </button>
        </Link>

    )
}
