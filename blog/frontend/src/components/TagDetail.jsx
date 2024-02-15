import React, {useState, useEffect} from 'react';
import {useParams} from 'react-router-dom';
import Posts from './Posts';
import {getTagDetail} from "../apiDRF";

export function TagDetail() {
    const {slug} = useParams();

    const [posts, setPosts] = useState(null);
    useEffect(() => {
        getTagDetail(slug, setPosts)
    }, []);

    if (!posts) {
        return <div>Загрузка...</div>;
    }

    return (
        <div>
            <Posts url={`/tag_detail/${slug}/`}/>
        </div>
    )
}

export default TagDetail