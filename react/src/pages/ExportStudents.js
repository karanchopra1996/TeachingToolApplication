import React, { useState } from "react";
import Button from '@mui/material/Button';

//-----------------------------------------------------------------------------------------------
function ExportStudents(courseId) {
  let [status, setStatus] = useState("")

  async function handleSubmit(e) {
    e.preventDefault()
    setStatus("Exporting...waiting for response")
    
    await fetch("/exportStudentGroups",{
        method:'POST',
        headers : {
        'Content-Type':'application/json'
        },
        body:JSON.stringify({
          "course":courseId.courseId.toString(),
        })
    }).then(function(response){
      return response.json()
    })
    .then(function(parsedData){
      setStatus(parsedData['message'])
      console.log(parsedData['message'])
      console.log(parsedData['status_code'])
    }).catch(error => setStatus("Failed to export groups from course"))
      
    
  }
  return <div>
    <p style= {{textAlign: "center", fontSize:60, color:"#4A2E83",marginTop:100}} >Export Course Groups From Canvas</p>
    <p style= {{textAlign: "center", color:"#4A2E83", marginTop:-30}}><strong>This tool exports group categories, groups, and their members from Canavs to a .csv file.</strong></p>
    <div style={{padding:10}}></div>
    <p style= {{textAlign: "center", color:"#4A2E83"}}>CSV file named <strong>"Course Name"-Groups</strong> will be created in your <strong>downloads folder</strong></p>
    <p style= {{textAlign: "center", color:"#4A2E83"}}>A notifcation will appear after the CSV has been created</p>
    <p style= {{textAlign: "center", color:"#4A2E83"}}><strong>{status}</strong></p>
    <div align="center">
      <Button onClick={handleSubmit} style={{ backgroundColor:'#4A2E83', marginTop:40, marginBottom:40}} type="submit" variant="contained">Export Groups</Button>
    </div>
    
  </div>
}
export default ExportStudents;