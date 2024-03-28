import React, { useState, useEffect, useCallback } from "react";
//import Box from '@mui/material/Box';
import Button from '@mui/material/Button';
import FormControl from '@mui/material/FormControl';
import Select from '@mui/material/Select';
import InputLabel from '@mui/material/InputLabel';
import MenuItem from '@mui/material/MenuItem';

import GoogleDrivePicker from "../GoogleDrivePicker";

var driveSupportedFileTypes = "application/vnd.google-apps.audio,application/vnd.google-apps.document,application/vnd.google-apps.drive-sdk,application/vnd.google-apps.drawing,application/vnd.google-apps.file,application/vnd.google-apps.folder,application/vnd.google-apps.form,application/vnd.google-apps.fusiontable,application/vnd.google-apps.jam,application/vnd.google-apps.map,application/vnd.google-apps.photo,application/vnd.google-apps.presentation,application/vnd.google-apps.script,application/vnd.google-apps.shortcut,application/vnd.google-apps.site,application/vnd.google-apps.spreadsheet,application/vnd.google-apps.unknown,application/vnd.google-apps.video"
//-----------------------------------------------------------------------------------------------
function WorkspaceFileToFile(courseId) {
    const [responseMessage, setResponse] = useState("")
    const [selectedGoogleFile, setSelectedGoogleFile] = useState({});
    const [destFolder, setDestFolder] = useState("")
    const [folders, setFolders] = useState([])

    useEffect(() => {
        setFolders([])
        fetch("/courseFolders", {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                "courseID": courseId.courseId.toString(),
            })
        })
            .then(response => response.json()).then(data => {
                setFolders(data.response)
            })
    }, [courseId.courseId])

    const handleChange = (event) => {
        setDestFolder(event.target.value)
    }

    const handleSubmit = (e) => {
        fetch("/downloadWorkspaceFile", {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                "courseID": courseId.courseId.toString(),
                "file": selectedGoogleFile['docs'],
                "destFolder": destFolder.toString()
            })
        }).then(response => response.json()).then(data => {
            setResponse(data['Response'])
        });
    }

    const sendFolder = useCallback((childData) => {
        if (childData == null) {

        } else {
            setSelectedGoogleFile(childData);
        }
    }, [])


    return (
        <div style={{ textAlign: "center", color: "#4A2E83" }}>

            <h1 style={{ paddingTop: "60px", fontSize: 60 }}>Convert a Google Workspace file to a Canvas File</h1>
            <p>
                This page allows to choose a file from Google Drive to send to a selected Course, where you can specify which folder within that course you want to upload the file to. You can select mulitple files to upload.
            </p>
            <p style={{ textAlign: "center", color: "#4A2E83" }}>This page only currently works for Google-based file formats, such as a Sheets doc, Slides doc, or Docs doc.</p>

            <div style={{ padding: 40 }}>

                <div align="center">
                    <FormControl sx={{ marginTop: 1, width: 300 }}>
                        <InputLabel id="canvas-folder-selector">Select Folder</InputLabel>
                        <Select
                            labelId="canvas-folder-selector"
                            id="canvas-folder"
                            defaultValue='None'
                            label='Canvas Folder'
                            value={destFolder}
                            onChange={handleChange}
                        >
                            {folders.map(folder => (
                                <MenuItem
                                    key={folder.id}
                                    value={folder.name}
                                >
                                    {folder.name}
                                </MenuItem>
                            ))}
                        </Select>
                    </FormControl>
                    <div align="center" style={{ marginTop: 10 }}>
                        <GoogleDrivePicker multiselect={false} response={sendFolder} style={{ backgroundColor: '#4A2E83' }} filetype={driveSupportedFileTypes}/>
                    </div>
                </div>
                <Button onClick={handleSubmit} style={{ marginTop: "80px", position: "relative", justifyContent: "center", alignItems: "center", backgroundColor: '#4A2E83' }} type="submit" variant="contained">Import to Canvas Files</Button>
            </div>
            <div>
                <p style={{ margin: "20px", position: "relative", justifyContent: "center", alignItems: "center", color: "#4A2E83", fontSize: 40 }}>{responseMessage}</p>
            </div>
        </div >
    )
}

export default WorkspaceFileToFile