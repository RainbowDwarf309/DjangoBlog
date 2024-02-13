import React, {useState} from 'react';
import {HeartIcon} from "@heroicons/react/24/solid";


export function AddToFavoriteButton() {
    const [favorite, setFavorite] = useState(false);


    return (
        <button className={"bg-teal-500 rounded-full h-8 w-8 flex justify-center items-center"}
                onClick={() => setFavorite(!favorite)}>
            <span className={`h-4 w-4 border-b-black ${favorite ? 'text-pink-500' : 'text-white'}`}><HeartIcon/></span>
        </button>
    )
}

export default AddToFavoriteButton;
