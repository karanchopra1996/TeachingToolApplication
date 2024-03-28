import React, { useState, useEffect } from "react";
//import Box from '@mui/material/Box';
import Button from '@mui/material/Button';

function DownloadAssignments(courseId) {
   const [responseMessage, setResponse] = useState("")
   
   const handleSubmission = (e)=> {
      e.preventDefault()//prevent refreashing page
      setResponse("Submitted, please wait for a response.")
      //no error, send to flask
      fetch("/exportAssignments",{
            method:'POST',
            headers : {
            'Content-Type':'application/json'
        },
        body:JSON.stringify({
          "courseID": courseId.courseId.toString()
        })
      })
      .then(response => response.json()).then(data => {
        setResponse(data['Response'])
      });  
   }
  
   return (
   <div style={{textAlign: "center", color: "#4A2E83"}}>
      <h1 style={{paddingTop: "60px", fontSize: 60}}>Download All Assignments</h1>
      <p>
         In this function, the user can download all the assignments for the selected course and will be saved
         as an excel file on their local machine.
      </p>
      <div>
         <Button onClick={handleSubmission} style={{margin: "20px", position: "relative" , justifyContent: "center", alignItems: "center", backgroundColor:'#4A2E83'}} type="submit" variant="contained">Download Assignments</Button>
      </div>
      <div>
        <p style={{margin: "20px", position: "relative" , justifyContent: "center", alignItems: "center", color: "#4A2E83", fontSize: 40}}>{responseMessage}</p>
      </div>
   </div>
   )
}

export default DownloadAssignments