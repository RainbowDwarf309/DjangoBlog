import React, {useState} from 'react';
import {HandThumbDownIcon} from "@heroicons/react/24/solid";


export function DislikeButton() {
    const [dislike, setDislike] = useState(false);


    return (
        <button className={"bg-teal-500 rounded-full h-8 w-8 flex justify-center items-center"}
                onClick={() => setDislike(!dislike)}>
            <span className={`h-4 w-4 ${dislike ? 'text-black' : 'text-white'}`}><HandThumbDownIcon/></span>
        </button>
    )
}

export default DislikeButton;
