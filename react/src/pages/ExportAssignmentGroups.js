import React, { useState, useEffect } from "react";
import Button from '@mui/material/Button';
import Select, { SelectChangeEvent } from '@mui/material/Select';
import FormControl from '@mui/material/FormControl';
import InputLabel from '@mui/material/InputLabel';
import MenuItem from '@mui/material/MenuItem';
import { purple, grey } from '@mui/material/colors';
import { brown } from '@mui/material/colors';
import Chip from '@mui/material/Chip';
import { styled } from '@mui/material/styles';
import Paper from '@mui/material/Paper';
import Alert from '@mui/material/Alert';
import Stack from '@mui/material/Stack';
import CircularProgress from '@mui/material/CircularProgress';
import IconButton from '@mui/material/IconButton';
import CloseIcon from '@mui/icons-material/Close';

function ExportAssignmentGroups(courseId) {
   console.log(courseId)
  /* required to populate assignmnet and contributor drop down */
  const [assignmentList, setAssignmentList] = useState([])
  const [chosenAssignment, setChosenAssignment] = useState("")
  const [progress, setProgress] = useState(false)

  const [success_flag, set_success_flag] = useState(null)
  const [action_completion, set_action_completion] = useState(false)
  const [alert_message, set_alert_message] = useState("")
   
  useEffect(() => {
    setAssignmentList([])
    fetch("/getAssignments",
      {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({
          "courseId": courseId.courseId.toString()
        })
      }).then(response => response.json()).then(data => {
        console.log(" Assignmnets =>", data.response)
        setAssignmentList(data.response)
      }).catch(error => {
        console.error('There was an error!', error);
      });
    }, [courseId.courseId])

    const changeAssignment = (event) => {
    resetData()
    console.log("Chosen assignment", event.target.value)
    setChosenAssignment(event.target.value);
    }

    /* get the contributors that groups tohgether to complete this assignmnet */
   const exportTeamData = (event) => {
    resetData()
    if (chosenAssignment == "")
    {
      set_alert_message(" Assignment is not selected !!")
      set_action_completion(true)
      return 
    }

    setProgress(true)
    fetch("/getGrpfromComments",
    {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body:JSON.stringify({
        "courseId": courseId.courseId.toString(),
        "assignId": chosenAssignment.toString()
      })
    }).then(response => response.json()).then(data => {

      if (data.response['errors']) {
            set_alert_message(data.response['errors'][0]['message'])
            set_success_flag(false)
            set_action_completion(true)
            setProgress(false)
          }
          else {
            
            set_action_completion(true)
            set_success_flag(true)
            set_alert_message("Contributor data for the assignment is exported ")
            setProgress(false)
          }
    }).catch(error => {
      setProgress(false)
      console.error('There was an error!', error);
      set_action_completion(true)
      set_alert_message("Error encountered while exporting the contriutor details")
    });

   }

   
  const resetData = () => {
    set_action_completion(false)
    set_success_flag(false)
  }
 
  
   return (
   <div style={{textAlign: "center", color: "#4A2E83"}}>
      <h1 style={{paddingTop: "60px", fontSize: 60}}>Export Assignment Groups</h1>
      <p style={{ fontSize: 20 }}>
         In this page, instructors or graders can export the report on assignment groups having submitter and contributor details 
      </p>
      <div>
          <FormControl sx={{ marginTop: 3, marginLeft: 2, width: 400, outlineColor: brown }}>
            <InputLabel id="permissions-select" sx={{ color: "balck", outline: purple }}>Select the Assignment</InputLabel>
            <Select
              labelId="permissions-select"
              id="permissions-simple-select"
              value={chosenAssignment}
              label="Choose an Assignment"
              onChange={changeAssignment}
            >
              {assignmentList.map(assigment => (
                <MenuItem
                  key={assigment.name}
                  value={assigment.id}>
                  {assigment.name}
                </MenuItem>
              ))}
            </Select>
          </FormControl>
          <FormControl sx={{ marginLeft: 4, marginTop: 3, width: 250, backgroundColor: "4A2E83", color: "white" }}>
            <Button onClick={exportTeamData}
              variant="contained"
              sx={{ width: 250, '&:hover': { backgroundColor: "#4A2E83", color: 'white', }, height: 50, backgroundColor: "#4A2E83", color: "white" }}>
              Export Groups
            </Button>
          </FormControl>
          {
              action_completion ?
              
              <Alert variant="filled" severity={success_flag ? "success" : "error"} 
                action = {
                            <IconButton
                              aria-label="close"
                              color="inherit"
                              size="small"
                              onClick={() => {
                                set_action_completion(false);
                              }}>  
                              <CloseIcon fontSize="inherit" />
                              </IconButton> 
                          } sx={{ marginLeft: 30, marginTop: 5,width: 700 }}>
                          {alert_message}
              </Alert> : <p></p> 
          }
          <FormControl sx={{ marginLeft: 4, marginTop: 3, width: 250, backgroundColor: "4A2E83", color: "gray" }}>
          <div>
            {progress ?
              <div>
                <p><b>Wait..Export action is in progress!! </b></p>
                <CircularProgress />
              </div>
              :
              <p></p>
            }
            {/* <p ><span sx={{ borderBlock: 'white',  float:"left" }}>{fileName}</span></p> */}
          </div>
          </FormControl>
         
        </div>
   </div>
   )
}

export default ExportAssignmentGroups