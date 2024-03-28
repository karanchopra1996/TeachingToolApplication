import React, { useState, useEffect } from "react";
//import Box from '@mui/material/Box';
import Button from '@mui/material/Button';

function DownloadQuizzes(courseId) {
   console.log(courseId)
   const [responseMessage, setResponse] = useState("")
   
   const handleSubmission = (e)=> {
      e.preventDefault()//prevent refreashing page
      setResponse("Submitted, please wait for a response.")
      if(responseMessage !== ''){
         setResponse('')
      }
      //no error, send to flask
      fetch("/exportQuizzes",{
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
      <h1 style={{paddingTop: "60px", fontSize: 60}}>Download All Quizzes</h1>
      <p>
         In this function, the user can download all the quizzes for the selected course and will be saved
         as an excel file on their local machine.
      </p>
      <div>
         <Button onClick={handleSubmission} style={{margin: "20px", position: "relative" , justifyContent: "center", alignItems: "center",backgroundColor:'#4A2E83'}} type="submit" variant="contained">Download Quizzes</Button>
         <p style={{margin: "20px", position: "relative" , justifyContent: "center", alignItems: "center", color: "#4A2E83", fontSize: 40}}>{responseMessage}</p>
      </div>
   </div>
   )
}

export default DownloadQuizzes