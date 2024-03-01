import {UserProfileSideBar} from "./UI/UserProfileSideBar";
import React, {useEffect, useState} from "react";
import {getUserProfile} from "../apiDRF";

export function ProfilePage() {
	const [profile, setProfile] = useState(null);
	const user_token = localStorage.getItem('token');
	console.log(profile)
	useEffect(() => {
		getUserProfile(user_token, setProfile)
	}, []);

	if (!profile) {
		return <div>Загрузка...</div>;
	}


	return (
		<div className={"bg-teal-200"}>
			<UserProfileSideBar/>
			<div className="p-4 sm:ml-64">
				<div className="p-4 border-2 border-gray-200 border-dashed rounded-lg dark:border-gray-700">
					<div className="flex h-80 w-72 mb-4 rounded-2xl bg-gray-50 dark:bg-gray-900">
						<div className="justify-items-stretch">
							<img src={profile.avatar} className="p-2 ml-12 mt-12 w-48 h-48 rounded-2xl" alt=""/>
							<h5 className="ml-12 text-white">{profile.user.username}</h5>
						</div>

					</div>
					<div className="mb-4 w-28">
						<h4 className="text-start text-gray-700 text-3xl font-bold font-sans">Karma</h4>
					</div>
					<div className="grid grid-cols-6 gap-72 mb-4">
						<div className="block items-start h-44 w-72 mb-4 rounded-2xl bg-gray-50 dark:bg-gray-900">
							<h4 className="text-start ml-4 mb-4 mt-4 text-white text-3xl font-medium font-sans">Total</h4>
							<h5 className="text-start ml-4 text-white text-3xl">{profile.karma}</h5>
							<h6 className="text-start ml-4 mb-4 mt-4 text-white text-xl font-medium font-sans">Position
								in rating: </h6>
						</div>
						<div className="block items-start h-44 w-72 mb-4 rounded-2xl bg-gray-50 dark:bg-gray-900">
							<h4 className="text-start ml-4 mb-4 mt-4 text-white text-3xl font-medium font-sans">Monthly</h4>
							<h5 className="text-start ml-4 text-white text-3xl">{profile.monthly_karma}</h5>
							<h6 className="text-start ml-4 mb-4 mt-4 text-white text-xl font-medium font-sans">Position
								in rating: </h6>
						</div>
					</div>
					<div className="mb-4">
						<h4 className="text-start text-gray-700 text-3xl font-bold font-sans">Publication
							statistics</h4>
						<p className="text-start text-gray-500 text-lg font-medium font-sans">Total statistics created
							for all time</p>
					</div>
					<div className="grid grid-cols-3 gap-4 mb-4">
						<div className="flex items-start h-48 mb-4 rounded-2xl bg-gray-50 dark:bg-gray-900">

						</div>
						<div className="flex items-start h-48 mb-4 rounded-2xl bg-gray-50 dark:bg-gray-900">

						</div>
						<div className="flex items-start h-48 mb-4 rounded-2xl bg-gray-50 dark:bg-gray-900">

						</div>
						<div className="flex items-start h-48 mb-4 rounded-2xl bg-gray-50 dark:bg-gray-900">

						</div>
						<div className="flex items-start h-48 mb-4 rounded-2xl bg-gray-50 dark:bg-gray-900">

						</div>
						<div className="flex items-start h-48 mb-4 rounded-2xl bg-gray-50 dark:bg-gray-900">

						</div>
						<div className="flex items-start h-48 mb-4 rounded-2xl bg-gray-50 dark:bg-gray-900">

						</div>
						<div className="flex items-start h-48 mb-4 rounded-2xl bg-gray-50 dark:bg-gray-900">

						</div>
						<div className="flex items-start h-48 mb-4 rounded-2xl bg-gray-50 dark:bg-gray-900">

						</div>
					</div>
				</div>
			</div>
		</div>
	)
}