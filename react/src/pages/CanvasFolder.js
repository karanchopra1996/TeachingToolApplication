import React, { useState, useEffect } from "react";
import Button from '@mui/material/Button';
import TextField from '@mui/material/TextField';
import FormControl from '@mui/material/FormControl';
import Select from '@mui/material/Select';
import InputLabel from '@mui/material/InputLabel';
import MenuItem from '@mui/material/MenuItem';

function CanvasFolder(courseId) {
    const [responseMessage, setResponse] = useState("")
    const [parentFolder, setParentFolder] = useState("")
    const [folders, setFolders] = useState([])
    const [value, setValue] = useState("")
    const [createdFolder, setCreatedFolder] = useState({})

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

    const handleChoice = (event) => {
        setParentFolder(event.target.value)
    }

    const handleSubmit = (e) => {
        fetch("/createCanvasFolder", {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                "courseID": courseId.courseId.toString(),
                "folderName": value.toString(),
                "parentFolder": parentFolder.toString()
            })
        }).then(response => response.json()).then(data => {
            setResponse(data['Response'])
            setCreatedFolder(data['Folder'])
        });
    }

    const handleChange = (event) => {
        setValue(event.target.value);
    }

    return (
        <div style={{ textAlign: "center", color: "#4A2E83" }}>

            <h1 style={{ paddingTop: "60px", fontSize: 60 }}>Create a Canvas Folder</h1>
            <p>
                This page allows to create a Folder in Canvas
            </p>

            <div style={{ padding: 35 }}>

                <div align="center">
                    <FormControl sx={{ marginTop: 1, width: 300 }}>
                        <InputLabel id="canvas-folder-selector">Canvas Parent Folder</InputLabel>
                        <Select
                            labelId="canvas-folder-selector"
                            id="canvas-folder"
                            defaultValue='None'
                            value={parentFolder}
                            onChange={handleChoice}
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
                        <TextField
                            required
                            id="new-folder-name"
                            placeholder="Folder Name"
                            label='New Folder Name'
                            value={value}
                            onChange={handleChange}
                        />

                    </div>
                </div>
            </div>
            <div>
                <Button onClick={handleSubmit} style={{ marginTop: "20px", position: "relative", justifyContent: "center", alignItems: "center", backgroundColor: '#4A2E83' }} type="submit" variant="contained">Create New Folder</Button>
                <p style={{ margin: "20px", position: "relative", justifyContent: "center", alignItems: "center", color: "#4A2E83", fontSize: 40 }}>{responseMessage}</p>
                <p style={{ margin: "40px", position: "relative", justifyContent: "center", alignItems: "center", color: "#4A2E83", fontSize: 20 }}>{createdFolder['files_url']}</p>
            </div>
        </div >
    )
}
export default CanvasFolder