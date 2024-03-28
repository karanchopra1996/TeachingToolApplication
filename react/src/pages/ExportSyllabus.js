import React, { useState, useEffect } from "react";
import FormControl from '@mui/material/FormControl';
import InputLabel from '@mui/material/InputLabel';
import MenuItem from '@mui/material/MenuItem';
import Select, { SelectChangeEvent } from '@mui/material/Select';
import Button from '@mui/material/Button';
import { purple } from '@mui/material/colors';
import { brown } from '@mui/material/colors';
import CircularProgress from '@mui/material/CircularProgress';
import Alert from '@mui/material/Alert';
import IconButton from '@mui/material/IconButton';
import CloseIcon from '@mui/icons-material/Close';

/* 
courseNameIdMap: This data acts as the hardcoded master data as of now 
TBD: pull master data out of hardcoded version 
This is the Mapping between course ID and course Name
*/
const courseNameIdMap = {
  "CSS 566 A Sp 22: Software Management": "1561396",
  "CSS 555 A Wi 22: Evaluating Software Design": "1541375",
  "Career Resources for MSCSSE, MSCSE & MSEE Students": "1154632",
  "CSS 501 B Au 22: Data Structures And Object-Oriented Programming I": "1594728",
  "CSS 517 A Au 22: Information Assurance And Cybersecurity": "1588659",
  "CSS 533 A Sp 22: Distributed Computing": "1561393",
  "CSS 549 A Au 21: Algorithm Design And Analysis": "1492343",
  "CSS 565 A Wi 22: Research Methods In Software Development": "1541378",
  "CSS 572 A Au 21: Evidence-Based Design": "1492347",
  "CSS 599 A Wi 22: Faculty Research Seminar": "1541383",
  "CSS Graduate Student Resources": "1443029",
  "CSSSKL 511 A Wi 22: Technical Writing": "1541377",
  "CSSSKL 594 A Au 22: Scientific Writing For Thesis/Project": "1588645",
  "Software Engineering Studio Badging": "1521080",
  "Teaching Tools Testbed": "1521081",
  "University 501": "1104039"
};

/*
1. This function exports the syllabus of the single course to pdf 
2. Syllabuses of all the enrolled courses to PDF
3. As of now the export functionality supports PDF exports only
3. When the user is in export syllabus page in UI, the  'GET' end point  fetches all the enrolled course information 
4. User can select a 'course name' and 'type of export' and click submit button. 
5. 'POST' REST end point gets communites to python backend to get the response
*/

function ExportSyllabus(courseId , isMainList = false) {
  /* 'courseList' will hold all the available couurses fetched by 'GET' api call */
  const [courseList, setVal] = useState([])
  const [labelText, setLabelText] = useState('Course Options');
  /*  The states that maintains drop down choices for course and export type  */
  const [chosenCourse, setChosenCourse] = React.useState('');
  const [exportType, setExportType] = React.useState('');

  /* helper states */
  const [courseID, setCourseID] = useState([])
  const [isAll, setIsAll] = useState(false)

  /* ui messages */
  const [responseMessage, setResponseMessage] = useState('')
  const [errorMessage, setErrorMessage] = useState('')

  /* UI progress bar */
  const [progress, setProgress] = useState(false)
  const [success_flag, set_success_flag] = useState(null)
  const [action_completion, set_action_completion] = useState(false)
  const [message, setMessage] = useState('')

  
  // Fetch courses once when the component mounts
useEffect(() => {
  fetch("/coursesAndID")
    .then(response => response.json())
    .then(response => {
      setVal(response.response);
    });
}, []);
  
  
  /* On Application load, this end point gets all the enrolled courses for the current logged in user */
useEffect(() => {

  if (isMainList) {
        // For Main List, set 'All Courses' as default
        setChosenCourse('all');
        setLabelText('All Courses');
      } else {
        // For Secondary List, find the course name based on courseId from the response
        const course = courseList.find(course => course.id === courseId);    
        if (course) {
          setChosenCourse(course.name);
          setLabelText(course.name); // Update label text for specific course
          setCourseID(courseId); // Set the specific course ID for export
        }
      }
 
}, [courseId, courseList, isMainList]);

  /* Exports the syllabus details to pdf or database. Right now only export feature is implemented */
  const exportSyllabus = (event) => {
     
    if (isAll) {
      setCourseID("")
    }
    if (responseMessage !== '') {
      setResponseMessage('')
    }
    if(courseID.length == 0)
    {
      setMessage(' Course(s) is(are) not selected ')
      set_action_completion(true)
      set_success_flag(false)
      return
    }
    if (exportType.toString() == '') {
      setMessage(' Export type is not selected ')
      set_action_completion(true)
      set_success_flag(false)
      return
    }
    setErrorMessage('')
    setProgress(true)
    fetch("/exportSyllabus",
      {
        method: 'POST',
        headers: {
        'Content-Type': 'application/json'
        },
        body: JSON.stringify({
        "courseId": courseID,
        "exportType": exportType.toString(),
        "isSaveAll": isAll
        })
      }).then(response => response.json()).then(data => {
        set_success_flag(true)
        set_action_completion(true)
        setProgress(false)
        console.log("SUCCESS => ", data['response'])
        setMessage(data.response)
     
      }).catch(error => {
        set_action_completion(true)
        set_success_flag(false)
        setProgress(false)
        console.error('There was an error!', error);
      });
  };


  /* helper functions */
  const changeCourse = (event) => {
    resetPage()
    setChosenCourse(event.target.value);
    if (event.target.value == "all") {
      console.log("set all save as True")
      setIsAll(true)
    }
    else {
      setIsAll(false)
      setCourseID(courseNameIdMap[event.target.value])
    }
  };

  const changeExportType = (event) => {
    setExportType(event.target.value);
  };

  const resetPage = (event) => {
    set_action_completion(false)
    set_success_flag(false)
  }

  return (
    <div style={{ textAlign: "center", color: "#4A2E83" }}>
      {/* Introductory Div */}
      <h1 style={{ paddingTop: "60px", fontSize: 60 }}>Export Course Syllabus</h1>
      <p style={{ fontSize: 20 }}>
        In this page you can select a single or all course so that their course syllabus can be exported.
        We have different export options available such as PDF export, database export.
      </p>
      <div>
        {/* This form control  is related to populating all courses*/}

        <FormControl sx={{ marginTop: 1, width: 300 }}>
        <InputLabel id="permissions-select">Course Options</InputLabel>
        <Select
          labelId="permissions-select"
          id="permissions-simple-select"
          value={chosenCourse}
          label="Choose Course"
          onChange={changeCourse}>
          {isMainList && <MenuItem value={'all'}>All Courses</MenuItem>}
          {!isMainList && <MenuItem value={chosenCourse}>{labelText}</MenuItem>}
          {isMainList && courseList.map(course => (
            <MenuItem value={course.name}>{course.name}</MenuItem>
          ))}
        </Select>
      </FormControl>
        {/* This form control  is related Export Type changes*/}
        <FormControl sx={{ marginTop: 1, marginLeft: 3, width: 300 }}>
          <InputLabel id="permissions-select" sx={{ color: "black", outline: purple }}>Export Type</InputLabel>
          <Select
            labelId="permissions-select"
            id="permissions-simple-select"
            value={exportType}
            label="Choose Course"
            onChange={changeExportType}
          >
            <MenuItem value={'toPDF'}>PDF</MenuItem>
            <MenuItem value={'toDB'} disabled>Database</MenuItem>
          </Select>
        </FormControl>
        <FormControl sx={{ marginLeft: 4, marginTop: 1, width: 150, backgroundColor: "purple", color: "white" }}>
          <Button onClick={exportSyllabus}
            variant="contained"
            sx={{ width: 150, '&:hover': { backgroundColor: '#4A2E83', color: 'white', }, height: 50, backgroundColor: "#4A2E83", color: "white" }}>
            Export
          </Button>
        </FormControl>
      </div>
      <FormControl sx={{ marginLeft: 4, marginTop: 3, width: 250, backgroundColor: "4A2E83", color: "gray" }}>
          <div>
            {progress ?
              <div>
                <p><b>Wait..Export action is in progress!! </b></p>
                <CircularProgress />
              </div>
              :
              <p></p>
            }
            {/* <p ><span sx={{ borderBlock: 'white',  float:"left" }}>{fileName}</span></p> */}
          </div>
      </FormControl>
      {
      action_completion ?
      
      <Alert variant="filled" severity={success_flag ? "success" : "error"} 
         action = {
                    <IconButton
                      aria-label="close"
                      color="inherit"
                      size="small"
                      onClick={() => {
                        set_action_completion(false);
                      }}>  
                      <CloseIcon fontSize="inherit" />
                      </IconButton> 
                  } sx={{ marginLeft: 22, width: 700 }}>
          {message}
      </Alert> : <p></p> 
    }
  
    </div>
  )
}

export default ExportSyllabus