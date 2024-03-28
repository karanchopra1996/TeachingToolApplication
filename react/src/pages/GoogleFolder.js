import React, { useState, useCallback } from "react";
import Button from '@mui/material/Button';
import TextField from '@mui/material/TextField';
import GoogleDrivePicker from '../GoogleDrivePicker';

function GoogleFolder(courseId) {
    const [responseMessage, setResponse] = useState("")
    const [selectedGoogleFile, setSelectedGoogleFile] = useState({});
    const [createdFolder, setCreatedFolder] = useState({})
    const [value, setValue] = useState("")
    const [url, setURL] = useState("")

    const handleSubmit = async (e) => {
        await fetch("/createGoogleFolder", {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                "courseID": courseId.courseId.toString(),
                "folderName": value.toString(),
                "parentFolder": selectedGoogleFile['docs']
            })
        }).then(response => response.json()).then(data => {
            setResponse(data['Response'])
            setCreatedFolder(data['Folder'])
            setURL('https://drive.google.com/drive/u/1/folders/' + createdFolder['id'])
        });
    }

    const handleChange = (event) => {
        setValue(event.target.value);
    }

    const sendFolder = useCallback((childData) => {
        if (childData == null) {

        } else {
            setSelectedGoogleFile(childData);
        }
    }, [])

    return (

        <div style={{ textAlign: "center", color: "#4A2E83" }}>

            <h1 style={{ paddingTop: "60px", fontSize: 60 }}>Create a Google Drive Folder</h1>
            <p>
                This page allows to create a Folder in Google Drive
            </p>

            <div style={{ padding: 25 }} align="center">
                <div align="center" style={{ marginTop: 10 }}>
                    <TextField
                        required
                        id="new-folder-name"
                        placeholder="Folder Name"
                        label="Google Folder Name"
                        value={value}
                        onChange={handleChange}
                    />
                </div>
                <div align="center" style={{ marginTop: 10 }}>
                    <GoogleDrivePicker multiselect={false} response={sendFolder} style={{ backgroundColor: '#4A2E83' }} filetype="application/vnd.google-apps.folder"/>
                    <Button onClick={handleSubmit} style={{ margin: "10px", position: "relative", justifyContent: "center", alignItems: "center", backgroundColor: '#4A2E83' }} type="submit" variant="contained">Create New Folder</Button>
                </div>


            </div>
            <div>
                <p style={{ margin: "10px", position: "relative", justifyContent: "center", alignItems: "center", color: "#4A2E83", fontSize: 30 }}>{responseMessage}</p>
                <p style={{ margin: "50px", position: "relative", justifyContent: "center", alignItems: "center", color: "#4A2E83", fontSize: 20 }}>{url}</p>

            </div>
        </div >
    )
}
export default GoogleFolder