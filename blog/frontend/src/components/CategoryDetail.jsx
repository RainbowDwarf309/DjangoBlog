import React, {useState, useEffect} from 'react';
import {useParams} from 'react-router-dom';
import Posts from './Posts';
import {getCategoryDetail} from "../apiDRF";

export function CategoryDetail() {
    const {slug} = useParams();
    const [posts, setPosts] = useState(null);

    useEffect(() => {
        getCategoryDetail(slug, setPosts)
    }, []);

    if (!posts) {
        return <div>Загрузка...</div>;
    }

    return (
        <div>
            <Posts url={`/category_detail/${slug}/`}/>
        </div>
    )
}

export default CategoryDetail