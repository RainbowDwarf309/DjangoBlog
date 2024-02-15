import React, {useState, useEffect} from 'react';
import {getCategories} from "../apiDRF";
import {ArrowLongRightIcon} from '@heroicons/react/24/solid'
import {HeartIcon} from '@heroicons/react/24/solid'


export function Categories() {

    const [categories, setCategories] = useState(null);
    useEffect(() => {
        getCategories(setCategories)
    }, []);

    if (!categories) {
        return <div>Загрузка...</div>;
    }

    return (
        <div>
            <div className="max-w-screen-lg mx-auto p-10 sm:p-8 md:p-10">
                <div className="grid md:grid-cols-2 sm:grid-cols-2 gap-x-1 gap-y-10">
                    {categories.map(item => (
                        <div
                            className="cursor-pointer bg-white max-w-lg sm:max-w-sm rounded-lg shadow overflow-hidden relative group"
                            key={item.id}>
                            <img className="w-full h-full object-fill rounded-lg "
                                 src={item.photo}
                                 alt=""/>
                            <h5 className="absolute bottom-2 left-2 p-2 text-3xl font-sans tracking-tight text-gray-900
                             transition delay-150 duration-500 dark:text-white  group-hover:-translate-y-16">{item.title}</h5>
                            <a href={item.get_absolute_url}
                               className="absolute opacity-70 bottom-4 left-2 p-2 text-xl font-sans tracking-tight text-gray-900 dark:text-white flex invisible group-hover:visible delay-500">
                                View all posts <span><ArrowLongRightIcon
                                className="h-6 w-6 text-gray-900 dark:text-white ml-2"/></span>
                                <span><HeartIcon className="justify-items-end opacity-100 ml-44 h-6 w-6 text-gray-900 dark:text-teal-500"/></span>
                            </a>
                        </div>
                    ))}
                </div>
            </div>
        </div>
    )

}

export default Categories