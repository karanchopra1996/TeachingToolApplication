import React, { useState, useEffect } from "react";
import FormControl from '@mui/material/FormControl';
import Select from '@mui/material/Select';
import InputLabel from '@mui/material/InputLabel';
import MenuItem from '@mui/material/MenuItem';
import Button from '@mui/material/Button';

function CanvasSettings(courseId){
    const [favoriteCourses, setFavoriteCourse] = useState([])
    const [fromCourse, setFromCourse] = useState(courseId || "")
    const [status, setStatus] = useState("")

    const handleChange = (event) => {
      setFromCourse(event.target.value);
    };

    useEffect(() => {
      fetch("/courseFavorites").then(res => res.json()).then(data => {
          setFavoriteCourse(data.courses)
          if (!fromCourse && data.courses.length > 0) {
              // Set fromCourse if it's not already set and courses are available
              setFromCourse(courseId || data.courses[0].id);
          }
      })
        }, [courseId])
    
    //***************************************************************************
    async function handleSubmit(e) {
        e.preventDefault()
        setStatus("")

        if(fromCourse === ""){
          console.log(fromCourse)
          setStatus("A course must be selected")
        }
        else{
          setStatus("Sent request...waiting for response")
          await fetch("/settings",{
            method:'POST',
            headers : {
            'Content-Type':'application/json'
            },
            body:JSON.stringify({
              "courseId":fromCourse.toString(),
              "importCourse":courseId.courseId.toString()
            })
          }).then(function(response){
            return response.json()
          })
          .then(function(parsedData){
            setStatus(parsedData['message'])
            console.log(parsedData['message'])
            console.log(parsedData['status_code'])
          }).catch(error => setStatus("Failed"))
        }
    }
       

    return <div>
        <p style= {{textAlign: "center", fontSize:60, color:"#4A2E83",marginTop:100}} >Import Settings and Navigation</p>
        <p style= {{textAlign: "center", color:"#4A2E83", marginTop:-30}}><strong>This tool exports the settings and navigation from a specified course and imports them to another course. </strong></p>
        
        <div style={{padding:5}}></div>
        <p style= {{textAlign: "center", color:"#4A2E83"}}>Because of structure of the Canvas API calls, this tool takes around <strong>30 seconds</strong> to complete.</p>
        <p style= {{textAlign: "center", color:"#4A2E83"}}>A notification will appear after the settings and navigation have been applied to the course.</p>
        <p style= {{textAlign: "center", color:"#4A2E83"}}><strong>{status}</strong></p>
        <div style={{padding:40}}>
        
          <div align="center">
            <FormControl sx={{ m: 1, width: 300 }}>
              <InputLabel sx={{backgroundColor:'white'}} id="demo-multiple-name-label">Settings From Course</InputLabel>
              <Select
                labelId="demo-multiple-name-label"
                id="demo-multiple-name"
                defaultValue='None'
                sx={{backgroundColor:'white'}}
                value={fromCourse}
                onChange={handleChange}
              >
                {favoriteCourses.map(course => (
                  <MenuItem
                    key={course.name}
                    value={course.id}
                  >
                    {course.name}
                  </MenuItem>
                ))}
              </Select>
            </FormControl>  
            <div align="center" style={{marginTop:10}}>
              <Button onClick={handleSubmit} style={{ backgroundColor:'#4A2E83', marginBottom:20}} type="submit" variant="contained">Import Settings and Navigation</Button>         
            </div>
          </div>             
                 
        </div>
    </div>
}

export default CanvasSettings;