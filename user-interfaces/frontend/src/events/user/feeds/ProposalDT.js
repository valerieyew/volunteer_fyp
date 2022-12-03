import React, { useState } from "react";
import TextField from '@mui/material/TextField';
import Stack from '@mui/material/Stack';

function ProposalDT(props) {

  return (
    <Stack component="form" noValidate spacing={3}>
      <TextField
        // id="datetime-local"
        label={props.dataFromProposeNewEvent}
        type="datetime-local"
        defaultValue="2022-04-01T00:00"
        sx={{ width: 250 }}
        InputLabelProps={{
          shrink: true,
        }}
        onChange={props.onChange}
      />
    </Stack>
  );
}

export default ProposalDT;
