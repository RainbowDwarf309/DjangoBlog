import React, {useState, useEffect} from 'react';
import {useParams} from 'react-router-dom';
import Posts from './Posts';

import {HOST_URL} from '../constants';

export function CategoryDetail() {
    const {slug} = useParams();
    const url = `${HOST_URL}/category_detail/${slug}/`;
    const [posts, setPosts] = useState(null);
    useEffect(() => {
        fetch(url)
            .then(response => response.json())
            .then(posts => setPosts(posts))
            .catch(error => console.error('Ошибка при получении данных:', error));
    }, [url]);

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