import React, {useState, useEffect} from 'react';

const API_URL = 'http://localhost:8000';

export function Categories() {
    const url = `${API_URL}/categories/`;
    const [data, setData] = useState(null);
    useEffect(() => {
        // Замените 'ВАШ_API_ЭНДПОИНТ' на адрес вашего API
        fetch(url)
            .then(response => response.json())
            .then(data => setData(data))
            .catch(error => console.error('Ошибка при получении данных:', error));
    }, []);

    if (!data) {
        return <div>Загрузка...</div>;
    }

    return (
        <div>
            <div className="max-w-screen-lg mx-auto p-10 sm:p-8 md:p-10">
                <div className="grid md:grid-cols-2 sm:grid-cols-2 gap-x-1 gap-y-10">
                    {data.map(item => (
                        <div
                            className="cursor-pointer bg-white max-w-lg sm:max-w-sm rounded-lg shadow overflow-hidden relative group"
                            key={item.id}>
                            <img className="w-full h-full object-fill rounded-lg "
                                 src={item.photo}
                                 alt=""/>
                            <h5 className="absolute bottom-2 left-2 p-2 text-3xl font-sans tracking-tight text-gray-900
                             transition delay-150 duration-500 dark:text-white  group-hover:-translate-y-16">{item.title}</h5>
                        </div>
                    ))}
                </div>
            </div>
        </div>
    )

}

export default Categories