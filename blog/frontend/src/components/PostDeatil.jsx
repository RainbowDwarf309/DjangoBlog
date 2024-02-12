import React, {useState, useEffect} from 'react';
import {useParams} from 'react-router-dom';
import {HOST_URL} from '../constants';

export function PostDetail() {
    const {slug} = useParams();
    const url = `${HOST_URL}/post_detail/${slug}/`;
    const [post, setPost] = useState(null);
    useEffect(() => {
        fetch(url)
            .then(response => response.json())
            .then(postData => {
                if (postData.created_at) {
                    postData.date = new Date(postData.created_at);
                }
                setPost(postData);
            })
            .catch(error => console.error('Ошибка при получении данных:', error));
    }, [url]);

    function formatDate(date) {
        return date.toLocaleDateString('ru-RU', {
            year: 'numeric',
            month: 'numeric',
            day: 'numeric'
        });
    }

    if (!post) {
        return <div>Загрузка...</div>;
    }

    return (
        <div>
            <div className="max-w-screen-lg mx-auto p-10 mb-4 overflow-hidden">
                <img className="object-contain max-w-full max-h-128 w-full h-auto rounded-lg" src={post.photo} alt=""/>
            </div>
            <small className={"small text-muted"}>
                <a href={"#"} className={"text-muted"}>{post.author.username}</a>
                <span className="px-2">·</span>
                <span>{formatDate(post.date)}</span>
                <span className="px-2">·</span>
                <span id="views"><i className="ti-eye"></i> Views: {post.views}</span>
                <span className="px-2">·</span>
                <a href="#" className="text-muted">{post.comments} Comments</a>
                <span className="px-2">·</span>
                {/*<LikeButton post={post}/>*/}
                <span className="px-2">{post.likes - post.dislikes}</span>
                {/*<DislikeButton post={post}/>*/}
                <span className="px-2">·</span>
                {/*<AddToFavoriteButton post={post}/>*/}
            </small>
            <div className="max-w-screen-lg mx-auto p-10 mb-4 overflow-hidden">
                <p className={"my-3 text-justify"}>{post.content}</p>
            </div>
        </div>
    )
}

export default PostDetail