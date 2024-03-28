import React, { useState, useEffect } from "react";
//import Box from '@mui/material/Box';
import Button from '@mui/material/Button';

function DownloadSyllabus(courseId) {
   const [responseMessage, setResponse] = useState("")
   
   const toDrive = (e)=> {
      e.preventDefault()//prevent refreashing page
      setResponse("Submitted, please wait for a response.")
      //no error, send to flask
      fetch("/getSyllabus",{
            method:'POST',
            headers : {
            'Content-Type':'application/json'
        },
        body:JSON.stringify({
          "courseID": courseId.courseId.toString(),
          "toLocal": false
        })
      })
      .then(response => response.json()).then(data => {
        setResponse(data['Response'])
      });   
   }

   const locallyAndToDrive = (e)=> {
      e.preventDefault()//prevent refreashing page
      setResponse("Submitted, please wait for a response.")
      //no error, send to flask
      fetch("/getSyllabus",{
            method:'POST',
            headers : {
            'Content-Type':'application/json'
        },
        body:JSON.stringify({
          "courseID": courseId.courseId.toString(),
          "toLocal": true
        })
      })
      .then(response => response.json()).then(data => {
        setResponse(data['Response'])
      });   
   }
   
   return (
   <div style={{textAlign: "center", color: "#4A2E83"}}>
      <h1 style={{paddingTop: "60px", fontSize: 60}}>Download Syllabus File</h1>
      <p>
         In this function, the user can download the syllabus file of a selected course to their local machine
         and Google Drive or to only their Google Drive.
      </p>
      <div>
         <Button onClick={locallyAndToDrive} style={{margin: "20px", position: "relative" , justifyContent: "center", alignItems: "center", backgroundColor:'#4A2E83'}} type="submit" variant="contained">Download Locally and Google Drive</Button>
         <Button onClick={toDrive} style={{margin: "20px", position: "relative" , justifyContent: "center", alignItems: "center", backgroundColor:'#4A2E83'}} type="submit" variant="contained">Download to Google Drive</Button>
      </div>
      <div>
        <p style={{margin: "20px", position: "relative" , justifyContent: "center", alignItems: "center", color: "#4A2E83", fontSize: 40}}>{responseMessage}</p>
      </div>
   </div>
   )
}

export default DownloadSyllabus