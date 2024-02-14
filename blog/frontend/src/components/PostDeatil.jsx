import React, {useState, useEffect} from 'react';
import {useParams} from 'react-router-dom';
import {HOST_URL} from '../constants';
import {LikeButton} from './buttons/LikeButton';
import {DislikeButton} from './buttons/DislikeButton';
import {AddToFavoriteButton} from './buttons/AddToFavoriteButton';
import {EyeIcon} from "@heroicons/react/24/solid";
import {ChatBubbleLeftRightIcon} from "@heroicons/react/24/solid";

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
            <div className="max-w-screen-lg mx-auto p-10 mb-1 overflow-hidden">
                <h3 className="text-4xl mt-0 mb-4 text-start">{post.title}</h3>
                <h4 className="mt-0 mb-4 text-start">Post's tags: {post.tags.map(tag => (
                    <a href="#" key={tag.id}
                       className="text-start p-0.5 bg-teal-500 text-white">#{tag.title}</a>))}</h4>
                <h4 className="mt-0 mb-4 text-start">Category: <a href="#"
                                                                  className="p-0.5 text-start bg-teal-500 text-white">{post.category.title}</a>
                </h4>
                <img className="object-contain max-w-full max-h-128 w-full h-auto rounded-lg" src={post.photo} alt=""/>
            </div>
            <div className={"max-w-screen-lg mb-0 mx-auto text-start flex justify-center items-center"}>
                <a href={"#"} className={"text-muted"}>{post.author.username}</a>
                <span className="px-2">·</span>
                <span>{formatDate(post.date)}</span>
                <span className="px-2">·</span>
                <span className={"flex justify-center items-center"}><EyeIcon
                    className={"mr-1 h-4 w-4 text-gray-700"}/> Views: {post.views}</span>
                <span className="px-2">·</span>
                <a href="#" className="text-muted flex justify-center items-center"><ChatBubbleLeftRightIcon
                    className={"h-4 w-4 mr-1 text-gray-700"}/>{post.comments} Comments</a>
                <span className="px-2">·</span>
                <LikeButton/>
                <span className="px-2">{post.likes - post.dislikes}</span>
                <DislikeButton/>
                <span className="px-2">·</span>
                <AddToFavoriteButton post={post}/>
            </div>
            <div className="max-w-screen-lg mx-auto pr-10 pl-10 mt-4 overflow-hidden">
                <p className={"my-3 text-justify"}>{post.content}</p>
            </div>
        </div>
    )
}

export default PostDetail