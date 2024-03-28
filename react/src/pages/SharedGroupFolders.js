import React, { useState, useEffect, useCallback } from "react";
//import Box from '@mui/material/Box';
import Button from '@mui/material/Button';
import FormControl from '@mui/material/FormControl';
import Select from '@mui/material/Select';
import InputLabel from '@mui/material/InputLabel';
import MenuItem from '@mui/material/MenuItem';
import GoogleDrivePicker from '../GoogleDrivePicker';



function SharedGroupFolders(courseId) {
    const [responseMessage, setResponse] = useState("")
    const [selectedGoogleFile, setSelectedGoogleFile] = useState({});
    const [accessOption, setAccessOption] = useState("")
    const [roster, setRoster] = useState([])
    const [groupsList, setGroups] = useState([])
    const [chosenGroup, setChosenGroup] = useState("")

    useEffect(() => {
        setGroups([])
        fetch("/listGroups", {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                "courseID": courseId.courseId.toString(),
            })
        }).then(response => response.json()).then(data => {
            setGroups(data.response)
        })
    }, [courseId.courseId])


    const sendFolder = useCallback((childData) => {
        if (childData == null) {

        } else {
            setSelectedGoogleFile(childData);
        }
    }, [])

    const handleSubmit = async (e) => {
        await fetch("/exportGroup", {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                "courseId": courseId.courseId.toString(),
                "key": "email",
                "teamName": chosenGroup
            })
        }).then(response => response.json()).then(data => {
            setRoster(data['Response'])
        });

        await fetch("/updateSharesOnFolder", {
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
        });
    }

    const handleChange = (event) => {
        setAccessOption(event.target.value);
    };
    const handleGroupChange = (event) => {
        setChosenGroup(event.target.value);
    };

    const handleGroupFolderCreation = async (e) => {
        await fetch("/exportGroups", {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                "courseId": courseId.courseId.toString(),
                "key": "email"
            })
        }).then(response => response.json()).then(data => {
            setGroups(data['Response'])
        });

        await fetch("/createGroupGoogleFolders", {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                "roster": roster,
                "access": "writer",
                "courseID": courseId.courseId.toString(),
                "parentFolder": selectedGoogleFile['docs']
            })
        }).then(response => response.json()).then(data => {
            setResponse(data['Response'])
        });

    }
    return (
        <div style={{ textAlign: "center", color: "#4A2E83" }}>

            <h1 style={{ paddingTop: "60px", fontSize: 60 }}>Group Folder</h1>
            <p>
                This page allows you to create group folders based on the groups of the selected course. If the groups are already populated with students, clicking the "Create New Shared Group Folders" will create Folders along the lines of "<i>courseName GroupName </i>", and then invite all of the students in those groups as long as they have their email attached to Canvas.
            </p>
            <p>
                If the Group Folders were already, or you want to select a group to add to a Google Drive Folder, you can select the group you want to target as well as the file and permissions, and update who the file or folder is shared to.
            </p>

            <div align="center" style={{ marginTop: 0 }}>
                <Button onClick={handleGroupFolderCreation} style={{ margin: "10px", position: "relative", justifyContent: "center", alignItems: "center", backgroundColor: '#4A2E83' }} type="submit" variant="contained">Create New Shared Group Folders</Button>
            </div>


            <div style={{ paddingTop: 50 }} align="center">
                <FormControl sx={{ marginTop: 1, marginRight: 1, width: 200 }}>
                    <InputLabel id="groups-label">Select Group</InputLabel>
                    <Select
                        labelId="groups"
                        id="groups"
                        defaultValue='None'
                        value={chosenGroup}
                        onChange={handleGroupChange}
                    >
                        {groupsList.map(group => (
                            <MenuItem
                                key={group.id}
                                value={group.name}
                            >
                                {group.name}
                            </MenuItem>
                        ))}
                    </Select>
                </FormControl>
            </div>
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
                <GoogleDrivePicker multiselect={false} response={sendFolder} style={{ backgroundColor: '#4A2E83' }} filetype="application/vnd.google-apps.folder" />
                <Button onClick={handleSubmit} style={{ margin: "10px", position: "relative", justifyContent: "center", alignItems: "center", backgroundColor: '#4A2E83' }} type="submit" variant="contained">Update Shares on Selected File/Folder</Button>
            </div>

            <p style={{ textAlign: "center", color: "#4A2E83" }}>This page requires students to have their email attached to their Canvas account.</p>


            <div>
                <p style={{ margin: "20px", position: "relative", justifyContent: "center", alignItems: "center", color: "#4A2E83", fontSize: 40 }}>{responseMessage}</p>

            </div>
        </div >

    )
}

export default SharedGroupFolders