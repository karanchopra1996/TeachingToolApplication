import React, { useState, useEffect } from "react";
//import Box from '@mui/material/Box';
import TextField from '@mui/material/TextField';
import Button from '@mui/material/Button';
import FormControl from '@mui/material/FormControl';
import Select from '@mui/material/Select';
import InputLabel from '@mui/material/InputLabel';
import MenuItem from '@mui/material/MenuItem';



function CanvasPageToDrive(courseId) {
   const [responseMessage, setResponse] = useState("")
   const [canvasPages, setCanvasPages] = useState([])
   const [choosenPage, setChoosenPage] = useState("")

   const handleChange = (event) => {
      setChoosenPage(event.target.value)
    }

   useEffect(() => {
     console.log("Fetching...")
     setCanvasPages([])
      fetch("/canvasCoursePages",{
               method:'POST',
               headers : {
              'Content-Type':'application/json'
        },
        body:JSON.stringify({
          "courseID": courseId.courseId.toString(),
        })
      })
      .then(response => response.json()).then(data => {
        setCanvasPages(data.response)
      })
    // eslint-disable-next-line react-hooks/exhaustive-deps
    }, [courseId.courseId])
   
   const handleSubmit = (e)=> {
      //e.preventDefault()//prevent refreashing page
      setResponse("Submitted, please wait for a response.")
      if(choosenPage){
      //no error, send to flask
      fetch("/getPageInfoToDrive",{
            method:'POST',
            headers : {
            'Content-Type':'application/json'
        },
        body:JSON.stringify({
          "courseID": courseId.courseId.toString(),
          "Canvas_Page": choosenPage.toString()
        })
      })
      .then(response => response.json()).then(data => {
        setResponse(data['Response'])
      });  
      }  
   }
   
   return (
   <div style={{textAlign: "center", color: "#4A2E83"}}>
      <h1 style={{paddingTop: "60px", fontSize: 60}}>Convert a Canvas Page to a Google Drive File</h1>
      <h1>{}</h1>
      <p>
      In this function convert a Canvas Page from a selected course and export it as a file 
      to your Google Drive.
      </p>
      <div>
      <FormControl sx={{width: 200 }}>
              <InputLabel id="demo-multiple-name-label">Select Canvas Page</InputLabel>
              <Select
                labelId="demo-multiple-name-label"
                id="demo-multiple-name"
                defaultValue='None'
                value={choosenPage}
                onChange={handleChange}
              >
                {canvasPages.map(page => (
                  <MenuItem
                    key={page.id}
                    value={page.name}
                  >
                    {page.name}
                  </MenuItem>
                ))}
              </Select>
            </FormControl>
            <div>
               <Button onClick={handleSubmit} style={{margin: "20px", position: "relative" , justifyContent: "center", alignItems: "center", backgroundColor:'#4A2E83'}} type="submit" variant="contained">Import to Google Drive</Button>
            </div>
         </div>
      <div>
        <p style={{margin: "20px", position: "relative" , justifyContent: "center", alignItems: "center", color: "#4A2E83", fontSize: 40}}>{responseMessage}</p>
      </div>
   </div>
   )
}

export default CanvasPageToDrive