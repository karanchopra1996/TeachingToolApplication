import React, { useState } from "react";
import Button from '@mui/material/Button';
import Grid from '@mui/material/Grid';
//-----------------------------------------------------------------------------------------------
function ImportStudents(courseId) {
    let [status, setStatus] = useState("")
    const [file, setFile] = useState("")

    function handleChange(e){
        setFile(e.target.files[0])
        console.log("file", e.target.files[0])     
    }

    async function handleImport(e){
        const formData = new FormData();
        formData.append('file',file)
        formData.append('courseId',courseId.courseId.toString())
        setStatus("CSV sent...waiting for response")

        await fetch("/importStudentGroups", {
                method:'POST',
                body: formData
                }).then(function(response){
                    return response.json()
                    })
                    .then(function(parsedData){
                    setStatus(parsedData['message'])
                    console.log(parsedData['message'])
                    console.log(parsedData['status_code'])
                    }).catch(error => setStatus("Failed to import groups"))

    }   

    return <div>
        <p style= {{textAlign: "center", fontSize:60, color:"#4A2E83", marginTop:100}} >Import Student Group to Canvas</p>
        <p style= {{textAlign: "center", color:"#4A2E83",marginTop:-30}}><strong>This tool takes a .csv file and creates group categories and groups and fills them with students, or it can fill existing groups with students.</strong></p>
        <div style={{padding:10}}></div>
        <p style= {{textAlign: "center", color:"#4A2E83"}}>Headers on .csv must be <strong>studentName,studentId,groupCategory,groupName</strong></p>
        <p style= {{textAlign: "center", color:"#4A2E83"}}>Only .csv files will be accepted.</p>
        <p style= {{textAlign: "center", color:"#4A2E83"}}>The groupCategory can either be the name of the category, as it appears in Canvas, or the id if the category exists</p>
        <p style= {{textAlign: "center", color:"#4A2E83"}}>The group category name in Canvas must begin with a letter</p>
        <p style= {{textAlign: "center", color:"#4A2E83"}}>Group categories and their groups can be created without listing members. ex: " , ,Project Teams,Project Team 1" </p>
        <p style= {{textAlign: "center", color:"#4A2E83"}}>Because of structure of the Canvas API calls, this tool can take around <strong>30 seconds</strong> to complete.</p>
        <p style= {{textAlign: "center", color:"#4A2E83"}}>A notifcation will appear after groups have been created</p>
        <p style= {{textAlign: "center", color:"#4A2E83"}}><strong>{status}</strong></p>
        <Grid container spacing={2} style={{ marginTop:20}} align="center">
            <Grid item xs={2}></Grid>
            <Grid item xs={4}>
                <form style={{padding:15}} align="center">
                    <input type="file" accept=".csv" onChange={(e)=> handleChange(e)}/>
                </form>
            </Grid>
            <Grid item xs={4}>
                <Button onClick={handleImport} style={{ backgroundColor:'#4A2E83', marginTop:10, marginBottom:40}} type="submit" variant="contained">Import Groups</Button>
            </Grid>
            <Grid item xs={2}></Grid>
        </Grid>
    </div>;
}

export default ImportStudents;