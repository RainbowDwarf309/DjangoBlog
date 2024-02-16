import {HOST_URL} from "./constants";


export async function getPosts(url, setData) {
    const host_url = `${HOST_URL}${url.url}`
    try {
        const response = await fetch(host_url);
        if (!response.ok) {
            throw new Error('Ошибка при получении данных');
        }
        const data = await response.json();
        setData(data);
    } catch (error) {
        console.error('Ошибка при получении данных:', error);
    }
}

export async function getCategories(setData) {
    const url = `${HOST_URL}/categories/`;
    try {
        const response = await fetch(url);
        if (!response.ok) {
            throw new Error('Ошибка при получении данных');
        }
        const data = await response.json();
        setData(data);
    } catch (error) {
        console.error('Ошибка при получении данных:', error);
    }
}


export async function getTags(setData) {
    const url = `${HOST_URL}/tags/`;
    try {
        const response = await fetch(url);
        if (!response.ok) {
            throw new Error('Ошибка при получении данных');
        }
        const data = await response.json();
        setData(data);
    } catch (error) {
        console.error('Ошибка при получении данных:', error);
    }
}

export async function getCategoryDetail(slug, setData) {
    const url = `${HOST_URL}/category_detail/${slug}/`
    try {
        const response = await fetch(url);
        if (!response.ok) {
            throw new Error('Ошибка при получении данных');
        }
        const data = await response.json();
        setData(data);
    } catch (error) {
        console.error('Ошибка при получении данных:', error);
    }
}

export async function getPostDetail(slug, setData) {
    const url = `${HOST_URL}/post_detail/${slug}/`;
    try {
        const response = await fetch(url);
        if (!response.ok) {
            throw new Error('Ошибка при получении данных');
        }
        const data = await response.json();
        if (data.created_at) {
            data.date = new Date(data.created_at);
        }
        setData(data);
    } catch (error) {
        console.error('Ошибка при получении данных:', error);
    }
}

export async function getTagDetail(slug, setData) {
    const url = `${HOST_URL}/tag_detail/${slug}/`;
    try {
        const response = await fetch(url);
        if (!response.ok) {
            throw new Error('Ошибка при получении данных');
        }
        const data = await response.json();
        setData(data);
    } catch (error) {
        console.error('Ошибка при получении данных:', error);
    }
}
