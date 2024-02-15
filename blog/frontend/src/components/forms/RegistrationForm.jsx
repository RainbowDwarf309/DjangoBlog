import React, {useState} from 'react';
import {HOST_URL} from "../../constants";
import {LockClosedIcon, UserCircleIcon, EnvelopeIcon} from "@heroicons/react/24/solid";

const RegistrationForm = () => {
    const [username, setUsername] = useState('');
    const [password, setPassword] = useState('');
    const [email, setEmail] = useState('');

    const handleUsernameChange = (event) => {
        setUsername(event.target.value);
    };

    const handlePasswordChange = (event) => {
        setPassword(event.target.value);
    };

    const handleEmailChange = (event) => {
        setEmail(event.target.value);
    };

    const handleSubmit = (event) => {
        event.preventDefault();
        fetch(`${HOST_URL}/registrations/`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({username, password, email}),
        })
            .catch(error => console.error('Ошибка при регистрации:', error));
    }


    return (
        <div className="flex justify-center items-center h-screen bg-white">
            <form onSubmit={handleSubmit} className="bg-teal-500 p-8 rounded shadow-md">
                <div className="mb-4">
                    <label htmlFor="username" className="block text-gray-700">Username:</label>
                    <div className={"flex justify-center items-center"}><UserCircleIcon
                        className={"h-8 w-8 mr-2 text-white"}/>
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
                    <div className={"flex justify-center items-center"}><LockClosedIcon
                        className={"h-8 w-8 mr-2 text-white"}/>
                        <input
                            type="password"
                            id="password_1"
                            value={password}
                            onChange={handlePasswordChange}
                            required
                            className="form-input mt-1 text-center block w-full rounded bg-white focus:bg-white focus:border-teal-500"
                        />
                    </div>
                </div>

                <div className="mb-4">
                    <label htmlFor="email" className="block text-gray-700">Email:</label>
                    <div className={"flex justify-center items-center"}><EnvelopeIcon
                        className={"h-8 w-8 mr-2 text-white"}/>
                        <input
                            type="email"
                            id="email"
                            value={email}
                            onChange={handleEmailChange}
                            required
                            className="form-input mt-1 text-center block w-full rounded bg-white focus:bg-white focus:border-teal-500"
                        />
                    </div>
                </div>
                <button type="submit" onSubmit={handleSubmit}
                        className="bg-white text-teal-500 py-2 px-4 rounded">Register
                </button>
                <a href="/login" className={"text-white block m-0 mt-4"}>Already have account? Log in</a>
            </form>
        </div>
    );
};

export default RegistrationForm;
