import React, { useRef, useState, useEffect } from "react";
import Button from '@mui/material/Button';
import Select, { SelectChangeEvent } from '@mui/material/Select';
import FormControl from '@mui/material/FormControl';
import InputLabel from '@mui/material/InputLabel';
import MenuItem from '@mui/material/MenuItem';
import { purple } from '@mui/material/colors';
import { brown } from '@mui/material/colors';
import Chip from '@mui/material/Chip';
import { styled } from '@mui/material/styles';
import Alert from '@mui/material/Alert';
import Stack from '@mui/material/Stack';
import IconButton from '@mui/material/IconButton';
import CloseIcon from '@mui/icons-material/Close';
import Box from '@mui/material/Box';
import Tab from '@mui/material/Tab';
import TabContext from '@mui/lab/TabContext';
import TabList from '@mui/lab/TabList';
import TabPanel from '@mui/lab/TabPanel';
import CircularProgress from '@mui/material/CircularProgress';
import Card from '@mui/material/Card';
import CardContent from '@mui/material/CardContent';

const ListItem = styled('li')(({ theme }) => ({
  margin: theme.spacing(0.5),
}));

/* This pages provides layot for selecting group members for the submitted assignment in the cabvas
the data is posted at the comment section of the Canvas  */
function SubmitAssignment(courseId) {
  /* The below two reference handlers for file handler during file updation and for text area field during text_entry type of submission*/
  const aRef = useRef(null);
  const textFieldRef = useRef("");

  /* Required to display submitter information */
  const [submitterData, setSubmitterData] = useState([])
  const [submitterName, setSubmitterName] = useState('')

  /* required to populate assignmnet and contributor drop down */
  const [assignmentList, setAssignmentList] = useState([])
  const [chosenAssignment, setChosenAssignment] = useState("")
  const [studentList, setStudentList] = useState([])

  /* to support adding or deleting group member selections */
  const [chipData, setChipData] = React.useState([]);
  const [showPaper, setShowPaper] = useState(false)

  /* assignmnet metadata */
  const [submissionTypeList, setSubmissionTypeList] = useState([])

   /*textArea and File submission */
   const [fileIds, setFileIds] = useState([])
   const [fileNames, setFileNames] = useState([])
 
   /*submission tabs */
   const [tabValue, setTabValue] = React.useState("");
   const [allowedExtension, setAllowedExtensions] = React.useState("");

  /* error message and success message display */
  /* assignmnet madation nmessages */
  const [assign_mandate, set_assign_mandate] = useState(false)
  const [assign_mandate_msg, set_assign_mandate_msg] = useState("")

  /*  submission status messages */ 
  const [action_completion_msg, set_action_completion_msg] = useState("")
  const [action_completion, set_action_completion] = useState(false)
  const [success_flag, set_success_flag] = useState(null)

  /* Submit file upload states (as a part of submission)  */
  const [upload_action_flag, set_upload_action_flag] = useState(false)

  /* syllabus body mandatory checks */
  const [body_mandate, set_body_mandate] = useState(false)
  const [file_mandate, set_file_mandate] = useState(false)
  const [mandate_body_msg, set_mandate_body_msg] = useState("")

  const [submission_progress, set_submission_progress] = useState(false)

  /*
    endpoint : "/getAssignments"
    details : end points populates all the assignments in a course 
    event : useEffect ()
    details: fured on launch 
  */
  useEffect(() => {
    setAssignmentList([])
    setSubmitterData([])
    fetch("/getAssignments",
      {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({
          "courseId": courseId.courseId.toString()
        })
      }).then(response => response.json()).then(data => {
        setAssignmentList(data.response)
      }).catch(error => {
        console.error('There was an error!', error);
      });

  /*
    endpoint : "/getSubmitterData"
    details : end points gets all the neccesary information about the UI user (submitter) 
    event : useEffect ()
    details: fured on launch 
  */
  fetch("/getSubmitterData").then(response => response.json()).then(data => {
      console.log(" Submitter data =>", data)
      setSubmitterData(data)
      setSubmitterName(data.name)
    }).catch(error => {
      console.error('There was an error!', error);
    });
  }, [courseId.courseId])

  /*
    endpoint : "/getCourseStudents"
    details : populates possible contributoes :: all students in the course 
    event : useEffect ()
    details: fured on launch 
  */
  useEffect(() => {
    setChipData([])
    fetch("/getCourseStudents",
      {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({
          "courseId": courseId.courseId.toString()
        })
      }).then(response => response.json()).then(data => {
        console.log("student names =>", data.response)
        setStudentList(data.response)

      }).catch(error => {
        console.error('There was an error!', error);
      });

  }, [courseId.courseId])

  /*
    endpoint: "/getAssignmentMetadata"
    details: for each of the chosen assignment get all the metadata about the assignment such as acceptable types, attempts
  */
  const changeAssignment = (event) => {
    set_assign_mandate(false)
    set_action_completion(false)
    console.log("Chosen assignment", event.target.value)
    setChosenAssignment(event.target.value);

    /* get assignment metadata */
    fetch("/getAssignmentMetadata",
      {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({
          "courseId": courseId.courseId.toString(),
          "assignId": event.target.value
        })
      }).then(response => response.json()).then(data => {

        /* parses extension types and according the input file allows these extension type to be uploaded  */
        if (data.allowed_extensions != undefined) {
          var allowedExtensionString = ""
          data.allowed_extensions.forEach(extension => {
            allowedExtensionString = allowedExtensionString + "," + "." + extension;
          });
          setAllowedExtensions(allowedExtensionString)
        }

        /* parses mode of submission */
        if (data.submission_types[0] == 'none') {
          console.log(" This assignmnet requires no submission")
        }
        else {
          setSubmissionTypeList(data.submission_types)
          /* the below code is for default activation of the tab. 
          By default it checks if text entry is present , then file upload then disabled tabs like web url,
          media or student annotation */
          if ((data.submission_types.indexOf("online_text_entry")) > -1) {
            setTabValue("online_text_entry")
          }
          else if ((data.submission_types.indexOf("online_upload")) > -1) {
            setTabValue("online_upload")
          }
          else if ((data.submission_types.indexOf("online_url")) > -1) {
            setTabValue("online_url")
          }
          else if ((data.submission_types.indexOf("media_recording")) > -1) {
            setTabValue("media_recording")
          }
          else if ((data.submission_types.indexOf("student_annotation")) > -1) {
            setTabValue("student_annotation")
          } else {
            setTabValue("")
          }
        }
      }).catch(error => {
        console.error('There was an error!', error);
      });
  };

  /*
    details: default tab for any assignmnet is online_text_entry but this method changes tab values
  */
  const handleTabChange = (event, newValue) => {
    setTabValue(newValue);
  };
  /*
    endpoint : "/submitAssignment"
    details : submits the assignmnet 
  */
  const submitComments = (event) => {
    
    var comment = ""
    var submission_body = null
    console.log (" fileIds", fileIds)
    console.log (" tab", tabValue)
    /* submission is not possible without assignment details */
    if (chosenAssignment == '') {
      console.log(" Choose an assignment")
      set_assign_mandate(true)
      set_assign_mandate_msg("Assignment is not chosen !!")
      setChipData([])
      setShowPaper(false)
      return
    }
    else if ( tabValue == 'online_text_entry')
    {
       /* online_text_entry type of submissions needs non empty text_body */
      if (textFieldRef.current.value == undefined || textFieldRef.current.value == "")
      {
        set_body_mandate(true)
        set_mandate_body_msg("Text Contents are empty")
        return
      }
      /* If there is non empty text_body then it can be submitted. submission_body is used later to form the json   */
      submission_body = textFieldRef.current.value
    }
    else if (tabValue == 'online_upload' && fileIds.length <= 0)
    {
      console.log(" In")
      /* online_upload type of submissions needs at least one file */
      set_mandate_body_msg("No file is selected !! ")
      set_file_mandate(true)
      return
    }
      resetAlerts()
      set_submission_progress(true)
       /* Forms the comments having contributors data*/
      comment = "Submitted by: " + submitterName + "\n \n ";
      if ((chipData).length > 0) {
        comment = comment + "Group Members:  Student-Name, Student-Id" + "\n" +
          "---------------------------------" + "\n ";
      }
      var contributors = []
      chipData.forEach(student => {
        comment = comment + student.name + ", " + student.studentId  + "\n";
        contributors.push({"id":student.studentId, "name":student.name})
      });

      
      var entity = {
        "courseId": courseId.courseId,
        "assignId": chosenAssignment,
        "submitterData": { "id":submitterData.id, "name":submitterData.name, "short_name":submitterData.short_name},
        "comment": comment,
        "submission_type": tabValue,
        "submission_body": submission_body,
        "fileIds": fileIds,
        "contributors":contributors
      }
      fetch("/submitAssignment",
        {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json'
          },
          body: JSON.stringify(entity)
        }).then(response => response.json()).then(data => {

          /* response is the error object if attempts are maximum */
          if (data.response['errors']) {
            set_action_completion_msg(data.response['errors']['attempt'][0]['message'])
            set_success_flag(false)
          }
          else {
            set_action_completion_msg(data.response)
            set_success_flag(true)
          }
          set_action_completion(true)
          resetData()
        }).catch(error => {
          set_action_completion_msg(" Error occured while submitting an assignment")
          set_success_flag(false)
          set_action_completion(true)
          set_submission_progress(false)
          console.error('There was an error!', error);
        });
  }
  /* few reset methods */
  const resetData = () => {
    setShowPaper(false)
    setChipData([])
    setChosenAssignment('')
    setSubmissionTypeList([])
    setFileNames([])
    setTabValue("")
    setFileIds([])
    setProgress(false)
    set_submission_progress(false)
  }
  const resetAlerts = () => {
    set_body_mandate(false)
    set_assign_mandate(false)
    set_file_mandate(false)
  }
  const resetInput = () => {
    aRef.current.value = null;
    setFileIds([])
    setSelectedFile(null)
    setFileName('')
    setIsSelected(false)
    setFileNames([])
  };


  /* HTML layot :: adding and delting contributors */
  const addToChip = (event) => {
    set_action_completion(false)
    var collaborators = [];
    var found = false

    chipData.some(student => {
      if (student.studentId === event.target.value.studentId)
        found = true

    })
    if (!found) {
      chipData.forEach(chip => {
        collaborators.push(chip)
      });
      collaborators.push(event.target.value)
      setChipData(collaborators)
      setShowPaper(true)
    }
  }

  /* helper function to update contributors */
  const deleteChip = (chipToDelete) => () => {
    set_action_completion(false)
    setChipData((chips) => chips.filter((chip) => chip !== chipToDelete));
    console.log("Chip Data ", chipData)
    if (chipData.length <= 1) {
      setShowPaper(false)
    }
  };

  /* HTML layot :: File manipulation
    Endpoint : "uploadSubmissionFiles"
   */
  const [selectedFile, setSelectedFile] = useState();
  const [fileName, setFileName] = useState('');
  const [isSelected, setIsSelected] = useState(false);
  const [progress, setProgress] = useState(false)
  const changeFileHandler = (event) => {
    setFileNames([])
    resetAlerts(false)
    console.log(" File chosen =>", event.target.files[0])
    setSelectedFile(event.target.files[0]);
    setIsSelected(true);
    setFileName(event.target.files[0].name)

    var fileNames = []
    Array.from(event.target.files).forEach(file => {
      fileNames.push(file.name)
    })
    setFileNames(fileNames)

    var fileIds = []
    Array.from(event.target.files).forEach(file => {
      const data = new FormData();
      data.append('file', file);
      data.append('name', file.name)
      data.append('size', file.size)
      data.append('content_type', file.type)
      data.append('studentId', submitterData.id)

      setProgress(true)
      /* need to make a call to backend to complete three step process in order to get file id after uploading file to canvas files */
      fetch("/uploadSubmissionFiles",
        {
          method: 'POST',
          body: data
        }).then(response => response.json()).then(data => {

          console.log(" data  ======>", data.response)
          if (data.response['error']) {
            console.log(" error msg =>", data.response['error'])
            set_action_completion_msg(data.response['error'])
            set_upload_action_flag(true)
            setProgress(false)
          }else{
          console.log(" File Id ==>", data.response)
          setProgress(false)
          fileIds.push(data.response.toString())
          }

        }).catch(error => {
          setProgress(false)
          console.log(" Error Occured while parsing the data response.. ")
        });

    })
    setFileIds(fileIds)
  };


  const getTableLabel = (submissionType) => {
    // console.log(" Tab label=>",submissionType)

    if (submissionType == "online_text_entry") {
      return "Text Entry"
    }
    else if (submissionType == "online_url") {
      return "Website URL"
    }
    else if (submissionType == "online_upload") {
      return "File Upload"
    }
    else if (submissionType == "media_recording") {
      return "Media"
    }
    else if (submissionType == "student_annotation") {
      return "Student Annotation"
    }
    return "No submission "
  };

  /**CSS */
  const TextAreaStyle = {
    backgroundColor: "#E3E1E1",
    color: "#394239",
    fontSize : 15,
    lineHeight:2,
    fontFamily: 'Franklin Gothic Medium'
  }

  /*HTML for the page */
  return (
    <div style={{ textAlign: "center", color: "black" }}>
      <h1 style={{ paddingTop: "60px", fontSize: 60 }}>Assignment Submission</h1>
      <p>
        This page enables students to submit their assignments.
        It provides capability for a submiiter of an assignmnet to indicate the name of the students that they worked with for completing the assignment.
      </p>
      <div>
        {/* First div gives the submitter name  */}
        <div>
          <FormControl sx={{ marginTop: 2, marginLeft: 0, width: 400, outlineColor: brown }}>
            Submitted By: <Chip label={submitterName}></Chip>
          </FormControl>
        </div>

        {/* assignmnet and studnet drop down */}
        <div>
          <FormControl sx={{ marginTop: 3, marginLeft: 2, width: 400, outlineColor: brown }}>
            <InputLabel id="permissions-select" sx={{ color: "balck", outline: purple }}>Select the Assignment</InputLabel>
            <Select
              labelId="permissions-select"
              id="permissions-simple-select"
              value={chosenAssignment}
              label="Choose an Assignment"
              onChange={changeAssignment}
            >
              {assignmentList.map(assigment => (
                <MenuItem
                  key={assigment.name}
                  value={assigment.id}>
                  {assigment.name}
                </MenuItem>
              ))}
            </Select>
            {assign_mandate ?
              (<Stack sx={{ width: '100%', marginTop: 1 }} spacing={2}>
                <Alert variant="filled" severity= "error"
                  action = {
                              <IconButton
                                aria-label="close"
                                color="inherit"
                                size="small"
                                onClick={() => {
                                  set_assign_mandate(false)
                                }}>  
                                <CloseIcon fontSize="inherit" />
                                </IconButton> 
                            }>
                    {assign_mandate_msg}
                </Alert>
              </Stack>) :
              (<p></p>)
            }
          </FormControl>

          { /* students list */}
          <FormControl sx={{ marginTop: 3, marginLeft: 2, width: 400, outlineColor: brown }}>
            <InputLabel id="permissions-select" sx={{ color: "balck", outline: purple }}>Collaborators</InputLabel>
            <Select
              labelId="permissions-select"
              id="permissions-simple-select"
              value={chosenAssignment}
              label="Choose group members"
              onChange={addToChip}
            >
              {studentList.map(student => (
                <MenuItem
                  value={student}>
                  {student.name}
                </MenuItem>
              ))}
            </Select>

          </FormControl>
        </div>

        {/* contributor chip */}
        <div>
          {/* This div gives the chip lot in a paper based on addition / deetion of the member.
           Ternary operator is used to show or hide paper  */}
          {showPaper ?
            (<FormControl sx={{ marginTop: 2, marginLeft: 0, width: 750, outlineColor: brown }}>
                <span sx={{
                  display: 'flex',
                  justifyContent: 'center',
                  flexWrap: 'wrap',
                  listStyle: 'none',
                }}  >
                {
                    chipData.map((student) => {
                      return (
                          <Chip sx={{ marginTop: 1, marginLeft:1}}
                            label={student.name}
                            onDelete={deleteChip(student)}
                          />
                      );
                    })
                }
                </span> 
              {/* </Paper> */}
            </FormControl>)
            :
            (<p> </p>)
          }
        </div>

        {/* tabs for submission  */}
        <div>
          <FormControl sx={{ marginTop: 2, marginLeft: 0, width: 800, outlineColor: brown }}>
            <Box sx={{ width: '100%', borderBlock: 'divider' }}>
              <TabContext value={tabValue}>
                <Box >
                  <TabList onChange={handleTabChange} aria-label="lab API tabs example">
                    {submissionTypeList.map(submissionType => (
                      <Tab value={submissionType} label={getTableLabel(submissionType)} />
                      // {{"index":submissionTypeList.indexOf(submissionType),"name":submissionType}}
                    ))}
                  </TabList>
                </Box>
                
                <TabPanel value="online_text_entry" index={0}>
                  <textarea cols="100" rows={18} style={TextAreaStyle}
                  id="myTextField"
                  label="Text Field"
                  variant="outlined"
                  ref={textFieldRef}
                  />
                {body_mandate ?
                  (<Stack sx={{ width: '100%', marginTop: 1}} spacing={2}>
                    <Alert variant="filled" severity="error" 
                        action = {
                                      <IconButton
                                        aria-label="close"
                                        color="inherit"
                                        size="small"
                                        onClick={() => {
                                          resetAlerts()
                                        }}>  
                                        <CloseIcon fontSize="inherit" />
                                        </IconButton> 
                                    } sx={{ width: 350 }}>
                            {mandate_body_msg}
                        </Alert>
                  </Stack>) :
                  (<p></p>)
                }
                </TabPanel>
                <TabPanel value="online_upload" index={1}>
                  <Card sx={{ height: 500, backgroundColor: "#ecebe9",color:"gray"  }}>
                    <p> <strong>File upload template</strong></p>
                    <CardContent >
                      {/* <div>
                        <Button type="input" variant="contained" size="medium"
                          sx={{ '&:hover': { backgroundColor: "#4A2E83", color: 'white', }, height: 50, marginLeft: 2,marginRight: 2, marginTop: 1, backgroundColor: "#4A2E83", color: "white", float: "left" }}>
                          <input ref={aRef} type="file" accept={allowedExtension} name="Choose File" onChange={changeFileHandler} multiple/>
                        </Button>
                      </div> */}
                      <Button
  variant="contained"
  component="label"
  sx = {{ backgroundColor: "#4A2E83", color: "white", float: "left" ,marginLeft: 15,marginRight: 2, marginTop: 1, '&:hover': { backgroundColor: "#4f3991", } }}
>
  Upload Files
  <input
    ref={aRef}
    accept={allowedExtension}
    type="file"
    name="Choose File"
    hidden
    onChange={changeFileHandler} multiple
  />
</Button>
                      <div sx={{ float: "left" }}>
                        {progress ?
                          <div>
                            <p><b>Wait..file upload is in progress!! </b></p>
                            <CircularProgress />
                          </div>
                          :
                          <p></p>
                        }
                        {/* <p ><span sx={{ borderBlock: 'white',  float:"left" }}>{fileName}</span></p> */}
                      </div>
                      <div>
                        {
                        upload_action_flag ?
                        <Alert variant="filled" severity="error" 
                        action = {
                                      <IconButton
                                        aria-label="close"
                                        color="inherit"
                                        size="small"
                                        onClick={() => {
                                          set_upload_action_flag(false);
                                          resetInput()
                                        }}>  
                                        <CloseIcon fontSize="inherit" />
                                        </IconButton> 
                                    } sx={{ width: 350 }}>
                            {action_completion_msg}
                        </Alert>
                         :
                         <div>
                         {(fileNames.length > 0) ?
                           fileNames.map(file => (
                             <span > {file} </span>
                           )) : <p></p>}
                       </div>
                      } 
                      </div>
                    </CardContent>
                  </Card>
                  {file_mandate ?
                  (<Stack sx={{ width: '100%', marginTop: 1}} spacing={2}>
                    <Alert variant="filled" severity="error" 
                        action = {
                                      <IconButton
                                        aria-label="close"
                                        color="inherit"
                                        size="small"
                                        onClick={() => {
                                          resetAlerts()
                                        }}>  
                                        <CloseIcon fontSize="inherit" />
                                        </IconButton> 
                                    } sx={{ width: 350 }}>
                            {mandate_body_msg}
                        </Alert>
                  </Stack>) :
                  (<p></p>)
                }
                </TabPanel>
                <TabPanel value="online_url" index={2} disabled>
                <Card sx={{ height: 500, backgroundColor: "#ecebe9" ,color:"gray" }}>
                <CardContent >
                  <b>This feature is not supported.  Currently this mode of submission is not availbale</b>
                </CardContent>
                </Card>
                </TabPanel>
                <TabPanel value="media_recording" index={3} disabled>
                <Card sx={{ height: 500,backgroundColor: "#ecebe9",color:"gray" }}>
                    <CardContent >
                  <b>This feature is not supported.  Currently this mode of submission is not availbale</b>
                  </CardContent>
                </Card>
                </TabPanel>
                <TabPanel value="student_annotation" index={4} disabled>
                <Card sx={{ height: 500,backgroundColor: "#ecebe9", color:"gray" }}>
                    <CardContent >
                  <b>This feature is not supported.  Currently this mode of submission is not availbale</b>
                          </CardContent>
                          </Card>
                </TabPanel>

              </TabContext>
            </Box>
          </FormControl>
        </div>
          {/* Submit button that adds contributors */}
          <FormControl sx={{ marginLeft: 0, marginTop: 0, width: 250, backgroundColor: "4A2E83", color: "gray" }}>
          <div sx={{ float: "left" }}>
                        {submission_progress ?
                          <div>
                            <p><b>Wait..assignment submission is in progress!! </b></p>
                            <CircularProgress />
                          </div>
                          :
                          <p></p>
                        }
                        {/* <p ><span sx={{ borderBlock: 'white',  float:"left" }}>{fileName}</span></p> */}
            </div>
            <Button onClick={submitComments}
              variant="contained"
              sx={{ width: 250, '&:hover': { backgroundColor: "#4A2E83", color: 'white', }, height: 50, backgroundColor: "#4A2E83", color: "white" }}
            >
              Submit Assignment
            </Button>
          </FormControl>
          <FormControl>
          {action_completion ?
            <Alert variant="filled" severity={success_flag ? "success" : "error"} 
            action = {
                       <IconButton
                         aria-label="close"
                         color="inherit"
                         size="small"
                         onClick={() => {
                           set_action_completion(false);
                           resetData()
                         }}>  
                         <CloseIcon fontSize="inherit" />
                         </IconButton> 
                     } sx={{ marginTop: 2,marginLeft: 2, width: 450 }}>
             {action_completion_msg}
           </Alert>
            :
            (<p></p>)
          }
          </FormControl>
      </div>
    </div>
  )
}

export default SubmitAssignment

