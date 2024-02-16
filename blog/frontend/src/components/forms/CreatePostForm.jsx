import React, {useEffect, useState} from 'react';
import {Formik, Form, Field, ErrorMessage} from 'formik';
import Select from 'react-select';
import {getCategories, getTags} from "../../apiDRF";
import {HOST_URL} from "../../constants";
import * as Yup from 'yup';

// Схема валидации с помощью Yup
const PostSchema = Yup.object().shape({
  title: Yup.string()
    .required('Заголовок обязателен'),
  content: Yup.string()
    .required('Текст поста обязателен'),
  category: Yup.mixed()
      .required('Категория обязательна'),
  tags: Yup.mixed()
      .required('Тэг обязателен'),
  photo: Yup.mixed()
    .required('Фотография обязательна')
});

const initialValues = {
    title: '',
    content: '',
    category: null,
    tags: null,
    link: '',
    photo: null
};

const CreatePostForm = () => {
    const [categories, setCategories] = useState(null);
    const [tags, setTags] = useState(null);
    useEffect(() => {
        getCategories(setCategories)
        getTags(setTags)
    }, []);

    const categoriesData = categories ? categories.map(item => ({
        value: item.id,
        label: item.title
    })) : null;
    const tagsData = tags ? tags.map(item => ({
        value: item.id,
        label: item.title
    })) : null;

    const handleSubmit = (values, {setSubmitting, resetForm}) => {
        const token = localStorage.getItem('token');
        const formData = new FormData();
        values['author'] = token

        for (const key in values) {
            if (key !== 'photo') {
                formData.append(key, values[key]);
            }
        }

        if (values.photo) {
            formData.append('photo', values.photo);
        }

        fetch(`${HOST_URL}/posts_create/`, {
            method: 'POST',
            headers: token ? {
                'Authorization': `Token ${token}`,
            } : {},
            body: formData,
        })
            .then(response => {
                // Обратите внимание, не каждый ответ будет в формате JSON.
                if (response.ok) {
                    return response;
                }
                throw new Error('Network response was not ok.');
            })
            .then(data => {
                console.log(data);
                setSubmitting(false);
            })
            .catch(error => {
                console.error('Ошибка при отправке данных:', error);
                setSubmitting(false);
            });
    };

    return (
        <div className="flex justify-center items-center h-screen bg-white">
            <Formik initialValues={initialValues} onSubmit={handleSubmit} validationSchema={PostSchema}>
                {({isSubmitting, setFieldValue}) => (
                    <Form className="bg-teal-500 p-8 rounded shadow-md" encType={"multipart/form-data"}>
                        <div className={"mb-4"}>
                            <label htmlFor="title">Title:</label>
                            <Field type="text" name="title"/>
                            <ErrorMessage name="title" component="div" className={"text-white"}/>
                        </div>
                        <div className={"mb-4"}>
                            <label htmlFor="content">Content:</label>
                            <Field as="textarea" name="content"/>
                            <ErrorMessage name="content" component="div" className={"text-white"}/>
                        </div>
                        <div className={"mb-4"}>
                            <label htmlFor="category">Category:</label>
                            <Select
                                options={categoriesData}
                                onChange={option => setFieldValue('category', option ? option.value : null)}
                            />
                            <ErrorMessage name="category" component="div" className={"text-white"}/>
                        </div>
                        <div className={"mb-4"}>
                            <label htmlFor="tags">Tags:</label>
                            <Select
                                options={tagsData}
                                onChange={option => setFieldValue('tags', option ? option.value : null)}
                            />
                        </div>
                        <div className={"mb-4"}>
                            <label htmlFor="content">Link:</label>
                            <Field type="text" name="link"/>
                            <ErrorMessage name="link" component="div" className={"text-white"}/>
                        </div>
                        <div className={"mb-4"}>
                            <label htmlFor="photo">Photo:</label>
                            <input
                                type="file"
                                name="photo"
                                onChange={event => setFieldValue('photo', event.currentTarget.files[0])}
                            />
                            <ErrorMessage name="photo" component="div" className={"text-white"}/>
                        </div>
                        <button type="submit" disabled={isSubmitting}
                                className="bg-white text-teal-500 py-2 px-4 rounded">
                            Submit
                        </button>
                    </Form>
                )}
            </Formik>
        </div>
    );
};

export default CreatePostForm;
