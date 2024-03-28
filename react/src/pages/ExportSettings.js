import React, {useState} from "react";
import Button from '@mui/material/Button';

function ExportSettings(courseId) {
    const [status, setStatus] = useState("")

    async function exportSettings(e){
        e.preventDefault()
        setStatus("Sent request...waiting for response")
        await fetch("/exportSettings",{
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
        <p style= {{textAlign: "center", fontSize:60, color:"#4A2E83", marginTop:100}} >Export Settings and Navigation To Files</p>
        <p style= {{textAlign: "center", color:"#4A2E83", marginTop:-30}}><strong>This tool exports course settings and navigation to Json files.</strong></p>
        
        <div style={{padding:5}}/>
        <p style= {{textAlign: "center", color:"#4A2E83"}}>The JSON files <strong> "Course Name"-Settings</strong> and <strong>"Course Name"-Navigation</strong> will be created in your <strong>downloads folder</strong></p>
        <p style= {{textAlign: "center", color:"#4A2E83"}}>The id in the navigation file is for reference and should not be modified</p>
        <p style= {{textAlign: "center", color:"#4A2E83"}}>A notifcation will appear after the files have been created</p>
        <p style= {{textAlign: "center", color:"#4A2E83"}}><strong>{status}</strong></p>

        <div align="center" style={{marginTop:40}}>
          <Button onClick={exportSettings} style={{ backgroundColor:'#4A2E83', marginBottom:40}} type="submit" variant="contained">Export Settings and Navigation</Button>
        </div>
    </div> 
}

export default ExportSettings;