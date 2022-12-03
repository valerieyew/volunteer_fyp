import LoggedInAdmin from "../../../apis/LoggedInAdmin";
import { useHistory } from 'react-router-dom';
import React, { useCallback } from 'react';

function AdminEventCard({ event: { event_id, name, date, time, info, image_url, status } }) {

  const history = useHistory();
  const handleOnClick = useCallback(() => history.push(`/admin/events/${event_id}`), [history]);

  // function handleApprove() {
  //   new LoggedInAdmin().patch(`/events/${event_id}/approve`).then(
  //     (res) => {
  //       console.log(res)
  //       console.log(event_id)
  //       history.push('/admin/home')
  //     })
  // }
  return (
    <div>
      <div className="flex">
        {/* <Link to={`/events/${id}`} /> only works in react v5 */} {/* TO BE ADDED LATER */}
        <div className="h-auto w-96 bg-white font-roboto text-gray-900 rounded-xl overflow-hidden border-2 border-gray-300 hover:border-gray-400">
          <img className="w-full h-48 object-cover" src={image_url[0]} alt="" />
          <div className="p-5">
            <h1 className="text-2xl text-left font-oswald font-extrabold uppercase line-clamp-2 h-16">{name}</h1>

            <p className="h-32 mt-2 text-md text-gray-500 text-left line-clamp-5 border-t-2 border-gray-300 py-2">{info}</p>
           
           <button type="button"
              className={`${status === 'Pending' ? "mt-4 w-full text-xl text-white font-oswald font-extrabold uppercase bg-[#39729c] p-2 rounded-lg hover:bg-[#264c68]"
              : "hidden"}`}
              onClick={handleOnClick}>
              Review Now
            </button>

            <button type="button"
              className={`${status === 'Approved' ? "mt-4 w-full text-xl text-white font-oswald font-extrabold uppercase bg-green-600 p-2 rounded-lg hover:bg-green-700"
              : "hidden"}`}
              onClick={handleOnClick}>
              View
            </button>


            <button type="button"
              className={`${status === 'Rejected' ? "mt-4 w-full text-xl text-white font-oswald font-extrabold uppercase bg-red-600 p-2 rounded-lg hover:bg-red-700"
              : "hidden"}`}
              onClick={handleOnClick}>
              View
            </button>



          </div>
        </div>
      </div>
    </div>
  );
}
export default AdminEventCard;

