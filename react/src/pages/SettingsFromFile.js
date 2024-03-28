import React, { useState } from "react";
import Button from '@mui/material/Button';
import Grid from '@mui/material/Grid';

function SettingsFromFile(courseId) {
    const [settingsFile, setSettingsFile] = useState("")
    const [navFile, setNavFile] = useState("")
    const [status, setStatus] = useState("")

    function handleFile1(e){
        setSettingsFile(e.target.files[0])     
    }

    function handleFile2(e){
        setNavFile(e.target.files[0])    
    }

    async function sendFiles(e){
        const formData = new FormData();
  
        if (settingsFile !== "" && navFile !== ""){
          formData.append('settingsFile',settingsFile)
          formData.append('navFile',navFile)
          formData.append('courseId',courseId.courseId.toString())
          setStatus("Files sent...waiting for response")
  
          await fetch("/settingsFromFiles", {
                  method:'POST',
                  body: formData
                  }).then(function(response){
                      return response.json()
                      })
                      .then(function(parsedData){
                      setStatus(parsedData['message'])
                      console.log(parsedData['message'])
                      console.log(parsedData['status_code'])
                      }).catch(error => setStatus("Failed to import settings and navigation"))
        }
        else{
          setStatus("Need to attach files")
        }
      }  


    return <div>
        <p style= {{textAlign: "center", fontSize:60, color:"#4A2E83",marginTop:100}} >Import Settings and Navigation From Files</p>
        <p style= {{textAlign: "center", color:"#4A2E83", marginTop:-30}}><strong>This tool imports settings and navigation from Json files.</strong></p>
        
        <div style={{padding:5}}></div>
        <p style= {{textAlign: "center", color:"#4A2E83"}}>Only Json files will be accepted.</p>
        <p style= {{textAlign: "center", color:"#4A2E83"}}>Settings JSON must be in a dictionary. Navigation JSON must be in a list of dictionaries.</p>
        <p style= {{textAlign: "center", color:"#4A2E83"}}>Because of structure of the Canvas API calls, this tool can take around <strong>30 seconds</strong> to complete.</p>
        <p style= {{textAlign: "center", color:"#4A2E83"}}>A notification will appear after the settings and navigation have been applied to the course.</p>
        <p style= {{textAlign: "center", color:"#4A2E83"}}><strong>{status}</strong></p>
        <Grid container spacing={2} style={{ marginTop:20}} align="center">           
            <Grid item xs={12}>
                <form style={{marginTop:20, color:"#4A2E83"}} align="center">
                    <Grid container spacing={2} style={{ marginTop:20}} align="center">
                        <Grid item xs={6} align="center">
                            <label >Settings: </label>
                            <input type="file" accept=".json" onChange={(e)=> handleFile1(e)}/>
                        </Grid>
                        <Grid item xs={6} align="center">
                            <label>Navigation: </label>                
                            <input type="file" accept=".json" onChange={(e)=> handleFile2(e)}/>
                        </Grid>
                    </Grid>
                 
                </form>
            </Grid>
            <Grid item xs={12}>
                <Button onClick={sendFiles} style={{ backgroundColor:'#4A2E83', marginTop:40, marginBottom:20}} type="submit" variant="contained">Import Settings and Navigation</Button>
            </Grid>
        </Grid>
        
    </div> 
}

export default SettingsFromFile;