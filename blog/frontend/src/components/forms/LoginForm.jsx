import React, {useState} from 'react';
import {HOST_URL} from "../../constants";
import {LockClosedIcon, UserCircleIcon} from "@heroicons/react/24/solid";

const LoginForm = () => {
    const [username, setUsername] = useState('');
    const [password, setPassword] = useState('');

    const handleUsernameChange = (event) => {
        setUsername(event.target.value);
    };

    const handlePasswordChange = (event) => {
        setPassword(event.target.value);
    };

    const handleSubmit = (event) => {
        event.preventDefault();
        fetch(`${HOST_URL}/logins/`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({username, password}),
        })
            .then(response => response.json())
            .then(data => {
                console.log(data.token)
                // Сохраняем полученный токен в localStorage
                localStorage.setItem('token', data.token);
            })
            .catch(error => console.error('Ошибка при аутентификации:', error));
        console.log('Submitted:', {username, password});
    }


    return (
        <div className="flex justify-center items-center h-screen bg-white">
            <form onSubmit={handleSubmit} className="bg-teal-500 p-8 rounded shadow-md">
                <div className="mb-4">
                    <label htmlFor="username" className="block text-gray-700">Username:</label>
                    <div className={"flex justify-center items-center"}><UserCircleIcon className={"h-8 w-8 mr-2 text-white"}/>
                        <input
                            type="text"
                            id="username"
                            value={username}
                            onChange={handleUsernameChange}
                            required
                            className="form-input mt-1 text-center block w-full rounded bg-white focus:bg-white focus:border-teal-500"
                        />
                    </div>
                </div>
                <div className="mb-4">
                    <label htmlFor="password" className="block text-gray-700">Password:</label>
                    <div className={"flex justify-center items-center"}><LockClosedIcon className={"h-8 w-8 mr-2 text-white"}/>
                        <input
                            type="password"
                            id="password"
                            value={password}
                            onChange={handlePasswordChange}
                            required
                            className="form-input mt-1 text-center block w-full rounded bg-white focus:bg-white focus:border-teal-500"
                        />
                    </div>
                </div>
                <button type="submit" onSubmit={handleSubmit}
                        className="bg-white text-teal-500 py-2 px-4 rounded">Login
                </button>
            </form>
        </div>
    );
};

export default LoginForm;
