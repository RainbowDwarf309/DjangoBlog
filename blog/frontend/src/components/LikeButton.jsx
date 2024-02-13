import React, {useState} from 'react';
import {HandThumbUpIcon} from "@heroicons/react/24/solid";


export function LikeButton() {
    const [like, setLike] = useState(false);


    return (
        <button className={"bg-teal-500 rounded-full h-8 w-8 flex justify-center items-center"}
                onClick={() => setLike(!like)}>
            <span className={`h-4 w-4 ${like ? 'text-black' : 'text-white'}`}><HandThumbUpIcon/></span>
        </button>
    )
}

export default LikeButton;
