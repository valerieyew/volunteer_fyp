import React, { useState, useEffect } from "react";
import TextField from '@mui/material/TextField';
import Stack from '@mui/material/Stack';


function EditRegDT({currentValue, dataFromProposeNewEvent, onChange}) {
  
  return (
    <Stack component="form" noValidate spacing={3}>
      <TextField
        // id="datetime-local"
        label={dataFromProposeNewEvent}
        type="datetime-local"
        // defaultValue={currentValue}
        value={currentValue}
        sx={{ width: 250 }}
        InputLabelProps={{
          shrink: true,
        }}
        onChange={onChange}
      />
    </Stack>
  );
}

export default EditRegDT;
