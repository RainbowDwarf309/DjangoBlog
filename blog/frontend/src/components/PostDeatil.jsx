import React, {useState, useEffect} from 'react';
import {useParams} from 'react-router-dom';

const API_URL = 'http://localhost:8000';

export function PostDetail() {
    const {slug} = useParams();
    const url = `${API_URL}/post_detail/${slug}/`;
    const [post, setPost] = useState(null);
    useEffect(() => {
        fetch(url)
            .then(response => response.json())
            .then(post => setPost(post))
            .catch(error => console.error('Ошибка при получении данных:', error));
    }, []);

    if (!post) {
        return <div>Загрузка...</div>;
    }

    return (
        <div>
            <div className="max-w-screen-lg mx-auto p-10 mb-4 overflow-hidden">
                <img className="object-contain max-w-full max-h-128 w-full h-auto rounded-lg" src={post.photo} alt=""/>
                <h1 className="text-4xl font-bold mt-4">{post.category_slug}</h1>
            </div>
            <div className="max-w-screen-lg mx-auto p-10 mb-4 overflow-hidden">
                <p className={"my-3 text-justify"}>{post.content}</p>
            </div>
        </div>
    )
}

export default PostDetail