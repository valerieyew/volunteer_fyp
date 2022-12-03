import EditDT from './EditDT';
import { useState, useEffect } from 'react';
import TextField from '@mui/material/TextField';
import Stack from '@mui/material/Stack';

function EditSessions({ session: { session_id, start_time, end_time, capacity, fill } , onStartDateChange, onEndDateChange, onCapacityChange, removeSessionChange}) {
    // console.log("TESTASDAS", session_id);
    console.log("START TIME", start_time)
  return (
    <div>
        {/* To label which session it is */}
        {/* <label class="inline-block uppercase tracking-wide text-gray-700 text-xs font-bold mb-4" for="grid-last-name">
            Session 
        </label> */}
        {/* <label class="inline-block uppercase tracking-wide text-gray-700 text-xs font-bold mb-4" for="grid-last-name">
            {sessionNo}
        </label> */}

        {/* The inputs for this particular session */}
        <div class="flex flex-wrap items-center mb-10">
            <div class="inline-block uppercase font-roboto">
                <EditDT dataFromProposeNewEvent = "Start date" currentValue={start_time} onChange={onStartDateChange} />
            </div>

            <div class="inline-block ml-5 uppercase font-roboto">
                <EditDT dataFromProposeNewEvent = "End date" currentValue={end_time} onChange={onEndDateChange} />
            </div>

            <div class="inline-block ml-5">
                <input onChange={onCapacityChange} 
                class="appearance-none block bg-gray-200 font-roboto text-gray-700 border border-gray-200 rounded py-4 px-4 leading-tight focus:outline-none focus:bg-white focus:border-gray-500" 
                placeholder="Capacity" 
                defaultValue={capacity}
                type="text" />
            </div>

            <button class="inline-block bg-red-400 hover:bg-red-600 rounded-xl font-oswald uppercase font-bold px-3 text-white ml-4 h-11" 
                onClick={removeSessionChange} 
            >
                Remove &times;
            </button>
        </div>
    </div>
  );
}
export default EditSessions;