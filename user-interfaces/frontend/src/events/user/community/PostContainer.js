
   
import React, { useEffect, useState } from 'react';
import Post from './Post';
import LoggedInUserCommunity from '../../../apis/LoggedInUserCommunity';

function PostContainer({all_posts}) {
// const [posts, setPosts] = useState([]);
    // let all_posts = []
    // useEffect(() => {
    //     getPostData();
    // }, []);

  // Fetch event data //
//   const getPostData = () => {
//     console.log("Fetching event data...")
//     new LoggedInUserCommunity().get("/posts/" + event_id).then(
//         (res) => {
//             // const all_posts = res.data.data;
//             // setPosts(all_posts);
//             all_posts = res.data.data;
//             console.log("ALL POSTS" + all_posts);
//         })
//         .catch((err) => {
//             console.log(err);
//         });

//     }
// let posts = [
//           {
//             "post_id": 1,
//             "post_title": "Important updates on wet weather",
//             "post_message": "Announcement to all participants, in the event of a wet weather, this activity may be cancelled.", 
//             "event_id" : 1,
//             "posted_on": "2022-03-29T12:22:00"
//           },
//           {
//             "post_id": 2,
//             "post_title": "New requirements for volunteers",
//             "post_message": "Announcement to all volunteers, you are required to have a valid first-aid certification for this event.", 
//             "event_id" : 1,
//             "posted_on": "2022-03-29T15:21:00"
//           }
//         ];

  return (
    <div className="flex flex-col flex-wrap">
        {all_posts.map((post) => (
            <Post post={post} key={post.post_id} />
          ))}
      {/* <Post />
      <Post />
      <Post /> */}
    </div>
  );
};

export default PostContainer;