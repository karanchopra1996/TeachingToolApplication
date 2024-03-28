import React, { useState, useCallback } from "react";
//import Box from '@mui/material/Box';
import Button from '@mui/material/Button';
import FormControl from '@mui/material/FormControl';
import Select from '@mui/material/Select';
import InputLabel from '@mui/material/InputLabel';
import MenuItem from '@mui/material/MenuItem';
import GoogleDrivePicker from "../GoogleDrivePicker";



function DriveSharedFolder(courseId) {
    const [responseMessage, setResponse] = useState("")
    const [selectedGoogleFile, setSelectedGoogleFile] = useState("")
    const [accessOption, setAccessOption] = useState("")
    const [roster, setRoster] = useState([])
    const [url, setURL] = useState("")

    const handleSubmit = (e) => {
        fetch("/exportStudents", {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                "courseId": courseId.courseId.toString(),
                "key": "email"
            })
        }).then(response => response.json()).then(data => {
            setRoster(data['Response'])
        }).then(fetch("/updateSharesOnFolder", {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                "roster": roster,
                "file": selectedGoogleFile['docs'],
                "access": accessOption.toString()
            })
        }).then(response => response.json()).then(data => {
            setResponse(data['Response'])
        }));
    }

    const handleChange = (event) => {
        setAccessOption(event.target.value);
    };

    const handleCourseFolderCreation = (e) => {
        fetch("/exportStudents", {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                "courseId": courseId.courseId.toString(),
                "key": "email"
            })
        }).then(response => response.json()).then(data => {
            setRoster(data['Response'])
        }).then(fetch("/createSharedGoogleFolder", {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                "roster": roster,
                "access": accessOption.toString(),
                "courseID": courseId.courseId.toString(),
                "parentFolder": selectedGoogleFile['docs']
            })
        }).then(response => response.json()).then(data => {
            setResponse(data['Response'])
            setURL('https://drive.google.com/drive/u/1/folders/' + data['Folder']['id'])
        }));
    }

    const sendFolder = useCallback((childData) => {
        if (childData == null) {

        } else {
            setSelectedGoogleFile(childData);
        }
    }, [])

    return (
        <div style={{ textAlign: "center", color: "#4A2E83" }}>

            <h1 style={{ paddingTop: "60px", fontSize: 60 }}>Update Shares on a Folder</h1>
            <p>
                This page allows to select a file and update a Folder to be shared with students on the roster for the course.
                You can choose whether to share the folder to the students as a writer, a commenter or a reader, and this will given all students.

                Created folders will be named "<i>courseID CourseName </i>".
            </p>

            <div style={{ padding: 10 }} align="center">
                <FormControl sx={{ marginTop: 1, width: 300 }}>
                    <InputLabel id="permissions-select">Access Options</InputLabel>
                    <Select
                        labelId="permissions-select"
                        id="permissions-simple-select"
                        value={accessOption}
                        label="Access Options"
                        onChange={handleChange}
                    >
                        <MenuItem value={"writer"}>Writer</MenuItem>
                        <MenuItem value={"commenter"}>Commenter</MenuItem>
                        <MenuItem value={"reader"}>Reader</MenuItem>
                    </Select>
                </FormControl>
            </div>
            <div align="center" style={{ marginTop: 10 }}>

                <GoogleDrivePicker multiselect={false} response={sendFolder} style={{backgroundColor: '#4A2E83' }}></GoogleDrivePicker>
                <Button onClick={handleSubmit} style={{ margin: "10px", position: "relative", justifyContent: "center", alignItems: "center", backgroundColor: '#4A2E83' }} type="submit" variant="contained">Update Shares on Selected File/Folder</Button>
            </div>
            <div align="center" style={{ marginTop: 0 }}>
                <Button onClick={handleCourseFolderCreation} style={{ margin: "10px", position: "relative", justifyContent: "center", alignItems: "center", backgroundColor: '#4A2E83' }} type="submit" variant="contained">Create New Shared Course Folder</Button>
            </div>
            <p style={{ textAlign: "center", color: "#4A2E83" }}>This page requires students to have their email attached to their Canvas account.</p>
            <div>
                <p style={{ margin: "20px", position: "relative", justifyContent: "center", alignItems: "center", color: "#4A2E83", fontSize: 40 }}>{responseMessage}</p>
                <p style={{ margin: "50px", position: "relative", justifyContent: "center", alignItems: "center", color: "#4A2E83", fontSize: 20 }}>{url}</p>

            </div>
        </div >

    )
}

export default DriveSharedFolder