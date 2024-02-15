import React, {useState, useEffect} from 'react';
import Moment from 'react-moment';
import {CalendarIcon} from "@heroicons/react/24/solid";
import {getPosts} from "../apiDRF";

export function Posts(url = '/posts/') {
    const [posts, setPosts] = useState(null);
    useEffect(() => {
        getPosts(url, setPosts)
    }, []);

    if (!posts) {
        return <div>Загрузка...</div>;
    }

    const getFirstSentences = (text, numSentences = 2) => {
        const sentences = text.split('.');
        return sentences.slice(0, numSentences).join('.') + (sentences.length > numSentences ? '...' : '');
    };

    return (
        <div>
            <div className="max-w-screen-xl mx-auto p-10 sm:p-8 md:p-12">
                <div className="grid grid-cols-1 md:grid-cols-3 sm:grid-cols-2 gap-0.5 gap-y-10">
                    {
                        posts.map(item => (
                            <div
                                className="max-w-sm bg-white w-80 rounded-lg shadow dark:bg-gray-800 dark:border-gray-700"
                                key={item.id}>
                                <a href="#">
                                    <img className="w-full items-center max-h-48 object-cover rounded-t-lg"
                                         src={item.photo} alt=""/>
                                </a>
                                <div className="p-5">
                                    <a href={item.get_absolute_url}>
                                        <h5 className="mb-0.5 text-2xl font-bold tracking-tight text-gray-900 dark:text-white">{item.title}</h5>
                                    </a>
                                    <span
                                        className={"mb-4 text-gray-600 flex justify-center items-center"}><CalendarIcon
                                        className={"w-4 h-4 mr-2"}/><Moment format={"MMM DD YYYY"}
                                                                            date={item.created_at} className={"mr-1"}/>  - By {item.author.username}</span>
                                    <p className="mb-3 m-0 font-normal text-gray-700 dark:text-gray-400">{getFirstSentences(item.content, 2)}</p>
                                    <a href={item.get_absolute_url}
                                       className="inline-flex items-center px-3 py-2 text-sm font-medium text-center text-white rounded-lg hover:bg-teal-300 focus:ring-4 focus:outline-none focus:ring-teal-300 dark:bg-teal-500 dark:hover:bg-teal-700 dark:focus:ring-teal-900">
                                        Read more
                                        <svg className="rtl:rotate-180 w-3.5 h-3.5 ms-2" aria-hidden="true"
                                             xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 14 10">
                                            <path stroke="currentColor" strokeLinecap="round" strokeLinejoin="round"
                                                  strokeWidth="2" d="M1 5h12m0 0L9 1m4 4L9 9"/>
                                        </svg>
                                    </a>
                                </div>
                            </div>
                        ))
                    }
                </div>
            </div>
        </div>
    )

}


export default Posts