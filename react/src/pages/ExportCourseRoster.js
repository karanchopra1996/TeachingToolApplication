import React, {useState} from "react";
import Button from '@mui/material/Button';

function ExportCourseRoster(courseId) {
  const [status, setStatus] = useState("")

    async function exportRoster(e){
        e.preventDefault()
        setStatus("Sent request...waiting for response")
        await fetch("/exportCourseRoster",{
              method:'POST',
              headers : {
              'Content-Type':'application/json'
              },
              body:JSON.stringify({
                "courseId":courseId.courseId.toString()
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
  return <div>
    <p style= {{textAlign: "center", fontSize:60, color:"#4A2E83", marginTop:100}} >Export Course Roster</p>
        <p style= {{textAlign: "center", color:"#4A2E83", marginTop:-30}}><strong>This tool exports a course roster to a CSV file.</strong></p>
        
        <div style={{padding:5}}/>
        <p style= {{textAlign: "center", color:"#4A2E83"}}>The file <strong>"Course Name"-Roster</strong>  will be created in your <strong>downloads folder</strong></p>
        <p style= {{textAlign: "center", color:"#4A2E83"}}>A notifcation will appear after the files have been created.</p>
        <p style= {{textAlign: "center", color:"#4A2E83"}}><strong>{status}</strong></p>

        <div style={{marginTop:40}} align="center">
            <Button onClick={exportRoster} style={{ backgroundColor:'#4A2E83', marginTop:10, marginBottom:40}} type="submit" variant="contained">Export Roster</Button>
        </div>
  </div> 
}

export default ExportCourseRoster;