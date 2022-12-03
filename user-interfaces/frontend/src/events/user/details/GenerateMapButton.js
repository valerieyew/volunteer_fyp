import React, { useEffect, useState } from 'react';
import MapContainer from './MapContainer';
function GenerateMapButton({ event_id, session_id }) {
    const [showMap, setShowMap] = useState(false);

    function handleGenerateMap(e) {
        e.preventDefault();
        console.log("GENERATING MAP")
        console.log(event_id)
        console.log(session_id)
        // CALL TRANSPORT ALGO
        setShowMap(true);
    }

    return (
      <div>
        <button
          className="mx-4 font-medium font-roboto text-[#305f82] hover:text-[#5b96c2]"
          onClick={handleGenerateMap}
        >
          Generate map
        </button>

        <div
          className={
            showMap
              ? "text-justify text-gray-700 uppercase text-lg font-bold"
              : "hidden"
          }
        >
          Pick-Up Map
        </div>
        <div className={showMap ? "mt-2 mb-10" : "hidden"}>
          <MapContainer />
        </div>
      </div>
    );
};

export default GenerateMapButton;