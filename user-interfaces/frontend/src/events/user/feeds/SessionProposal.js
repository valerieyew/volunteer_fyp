import ProposalDT from './ProposalDT';

function SessionProposal(props) {
  return (
    <div>
        {/* To label which session it is */}
        {/* <label class="inline-block uppercase tracking-wide text-gray-700 text-xs font-bold mb-4" for="grid-last-name">
            Session 
        </label> */}
        <label class="inline-block uppercase tracking-wide text-gray-700 text-xs font-bold mb-4" for="grid-last-name">
            {/* {props.sessionId} */}
        </label>

        {/* The inputs for this particular session */}
        <div class="flex flex-wrap items-center mb-10">
            <div class="inline-block uppercase font-roboto">
                <ProposalDT dataFromProposeNewEvent = "Start date" onChange={props.onStartDateChange} />
            </div>

            <div class="inline-block ml-5 uppercase font-roboto">
                <ProposalDT dataFromProposeNewEvent = "End date" onChange={props.onEndDateChange} />
            </div>

            <div class="inline-block ml-5">
                <input onChange={props.onCapacityChange} 
                class="appearance-none block bg-gray-200 font-roboto text-gray-700 border border-gray-200 rounded py-4 px-4 leading-tight focus:outline-none focus:bg-white focus:border-gray-500" 
                placeholder="Capacity" 
                type="text" />
            </div>

            <button class="inline-block bg-red-400 hover:bg-red-600 rounded-xl font-oswald uppercase font-bold px-3 text-white ml-4 h-11" 
                onClick={props.removeSessionChange} 
            >
                Remove
            </button>
        </div>
    </div>
  );
}
export default SessionProposal;