import React, { useState } from 'react';
import LoggedInUserCommunity from '../../../apis/LoggedInUserCommunity';
import { useHistory } from 'react-router-dom';
function CreatePostBox({event_id}) {
    const [post, setPost] = useState("");
    const [title, setTitle] = useState("");
    const inputEntry = React.useRef();
    const inputTitle = React.useRef();

    let history = useHistory();

    function handlePostChange(e) {
        const post = e.target.value;
        console.log(post)

        setPost(post);

        
    }
    function handleTitleChange(e) {
        const title = e.target.value;
        console.log(title)
        setTitle(title);
        
    }
    const handleSubmit = (e) => {
        e.preventDefault();

        new LoggedInUserCommunity()
            .post("/posts/" + event_id, {
                post_title: title,
                post_message: post
            })
            .then((res) => {
                console.log("SUBMITTED")
                console.log(res);
                inputTitle.current.value = "";
                inputEntry.current.value = "";
                window.location.reload(false);

            })
            .catch((err) => {
                console.log(err);
            })
    }

  return (
    <form onSubmit={handleSubmit}>
    <div className="flex flex-col">

    <div className="rounded-lg bg-white flex flex-col p-6 pt-4 border border-[#873307] mt-8 w-5/6 self-center">
    <span className="mb-2 text-2xl font-oswald font-extrabold uppercase text-[#873307]">Upload a New Post: </span>
      <div className=" items-center pb-3 mb-2">
        {/* <div className="w-10 h-10">
          <img
            src="https://picsum.photos/200"
            className="w-full h-full rounded-full"
            alt="dp"
          />
        </div> */}
        <input className="block w-full mt-2 mb-4 border border-gray-400 focus:bg-white focus:outline-none focus:ring-2 focus:ring-gray-400/[0.3] flex-grow bg-gray-100/[0.3] placeholder-gray-400 text-gray-500 text-left rounded h-10 pl-5 text-sm"
        placeholder='Title' onChange={handleTitleChange.bind()} ref={inputTitle}>
        </input>
        <textarea name="body" rows="3" placeholder="What&apos;s on your mind?" className="w-full pl-5 rounded border border-gray-400 bg-gray-100/[0.3] dark:border-gray-400 text-gray-600 dark:text-gray-800 focus:bg-white focus:outline-none focus:ring-2 focus:ring-gray-400/[0.3] focus:border-transparent placeholder-gray-400 text-sm h-auto" maxlength="500" 
         onChange={handlePostChange.bind()} ref={inputEntry}>
        </textarea>
      </div>
      <button
        type="submit"
        className=
             "rounded-md font-oswald font-extrabold text-xl text-white uppercase bg-[#a84009] active:bg-blueGray-600 text-md py-2 hover:bg-[#873307]" 
        onClick={handleSubmit.bind()}
        >
        Post
      </button>
      
      
      {/* <div className="flex space-x-3 font-thin text-sm text-gray-600 -mb-1">
        <button className="flex-1 flex items-center h-8 focus:outline-none focus:bg-gray-200 justify-center space-x-2 hover:bg-gray-100 rounded-md">
          <div>
            <i className="fab fa-youtube text-red-400"></i>
          </div>
          <div>
            <p className="font-semibold">Create Video</p>
          </div>
        </button>
        <button className="flex-1 flex items-center h-8 focus:outline-none focus:bg-gray-200 justify-center space-x-2 hover:bg-gray-100 rounded-md">
          <div>
            <i className="fas fa-images text-green-500"></i>
          </div>
          <div>
            <p className="font-semibold">Photos/Video</p>
          </div>
        </button>
        <button className="flex-1 flex items-center h-8 focus:outline-none focus:bg-gray-200 justify-center space-x-2 hover:bg-gray-100 rounded-md">
          <div>
            <i className="far fa-smile text-yellow-500"></i>
          </div>
          <div>
            <p className="font-semibold">Feeling/Activity</p>
          </div>
        </button>
      </div> */}
    </div>
    </div>
    </form>
  );
};

export default CreatePostBox;