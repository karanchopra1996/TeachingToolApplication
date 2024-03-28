import React, { useState, useEffect } from "react";
//import Box from '@mui/material/Box';
import TextField from '@mui/material/TextField';
import Button from '@mui/material/Button';
import FormControl from '@mui/material/FormControl';
import Select from '@mui/material/Select';
import InputLabel from '@mui/material/InputLabel';
import MenuItem from '@mui/material/MenuItem';
import Autocomplete from '@mui/material/Autocomplete';
import CircularProgress from '@mui/material/CircularProgress';

function sleep(delay = 0) {
  return new Promise((resolve) => {
    setTimeout(resolve, delay);
  });
}


function GoogleDocToCanvas(courseId) {  
  const [open, setOpen] = useState(false);
  const [options, setOptions] = useState([]);
  const [docID, setDocID] = useState("")
  const [docName, setDocName] = useState("")
  const [type, setType] = useState("")
  const [folders, setFolders] = useState([])
  const [googleFiles, setGoogleFiles] = useState([])
  const [choosenFolder, setChoosenFolder] = useState("")
  const [responseMessage, setResponse] = useState("")
  const [statusMessage, setStatus] = useState("Please wait for us to retrieve your google files.")

  const loading = open && options.length === 0;
  useEffect(() => {
    setFolders([])
    setGoogleFiles([])
    fetch("/courseFolders",{
             method:'POST',
             headers : {
            'Content-Type':'application/json'
      },
      body:JSON.stringify({
        "courseID": courseId.courseId.toString(),
      })
    })
    .then(response => response.json()).then(data => {
      setFolders(data.response)
    })
    fetch("/getGoogleFiles").then(res => res.json()).then(data => {
      setGoogleFiles(data.files)
      setStatus("Ready to view google files.")
    })
  // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [courseId.courseId])

  useEffect(() => {
    let active = true;

    if (!loading) {
      return undefined;
    }

    (async () => {
      await sleep(500); // For demo purposes.

      if (active) {
        setOptions([...googleFiles]);
      }
    })();

    return () => {
      active = false;
    };
  }, [loading]);

  useEffect(() => {
    if (!open) {
      setOptions([]);
    }
  }, [open]);
  
  const handleChange = (event) => {
    setChoosenFolder(event.target.value)
  }
  const handleGoogleFile = (event, value) => {
    if(value !== null){
      setDocID(value['id'])
      setDocName(value['title'])
      setType(value['type'])
    }
  }

  const handleSubmit = (e)=> {
    setResponse("Submitted, please wait for a response.")
    e.preventDefault()//prevent refreashing page
    if(docID && choosenFolder){//no error, send to flask
      //console.log(docName, course)
      fetch("/getGoogDoc",{
             method:'POST',
             headers : {
            'Content-Type':'application/json'
      },
      body:JSON.stringify({
        "docID": docID.toString(),
        "docName" : docName.toString(),
        "type" : type.toString(),
        "courseID": courseId.courseId.toString(),
        "folder": choosenFolder.toString()
      })
    })
    .then(response => response.json()).then(data => {
      setResponse(data['Response'])
    });
    }    
  }

  return <div>
    <h1 style= {{textAlign: "center", color:"#4A2E83", paddingTop: "60px", fontSize: 60}} >Import Google Doc as a File to Canvas</h1>
    <p style={{textAlign: "center", color: "#4A2E83", margin: "30px 140px"}}>
      In this function, please choose a file from your Google Drive that you'd like to export 
      and import it to canvas. Also please select the folder in which you'd like to place the file into. 
    </p>
    <p style={{margin: "20px", position: "relative" , justifyContent: "center", textAlign: "center", color: "red", fontWeight: 'bold'}}>
      Please note only google drive native files can be 
      imported to canvas currently.
    </p>

    <div>
      <p style={{margin: "20px", position: "relative" , justifyContent: "center", textAlign: "center", color: "#4A2E83", fontWeight: 'bold'}}>{statusMessage}</p>
    </div>
    

    <div style={{justifyContent:"center", position: 'relative', textAlign: 'center'}}>
      <Autocomplete
        onChange={handleGoogleFile}
        id="asynchronous-demo"
        sx={{marginRight: '300px', '& .MuiFormControl-root':{position:'absolute', width: 300}}}
        open={open}
        onOpen={() => {
          setOpen(true);
        }}
        onClose={() => {
          setOpen(false);
        }}
        isOptionEqualToValue={(option, value) => option.id === value.id}
        getOptionLabel={(option) => option.title}
        options={options}
        loading={loading}
        renderInput={(params) => (
          <TextField
            onChange={handleGoogleFile}
            {...params}
            label="Select File"
            InputProps={{
              ...params.InputProps,
              endAdornment: (
                <React.Fragment>
                  {loading ? <CircularProgress color="inherit" size={20} /> : null}
                  {params.InputProps.endAdornment}
                </React.Fragment>
              ),
            }}
          />
        )}
      />
      <FormControl sx={{width: 200, marginTop: '75px' }}>
              <InputLabel id="demo-multiple-name-label">Select Folder</InputLabel>
              <Select
                labelId="demo-multiple-name-label"
                id="demo-multiple-name"
                defaultValue='None'
                value={choosenFolder}
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
      <div>
      </div>
      <div>
      <Button onClick={handleSubmit} style={{margin: "20px", position: "relative" , justifyContent: "center", alignItems: "center",backgroundColor:'#4A2E83'}} type="submit" variant="contained">Import to Canvas Page</Button>

        <p style={{margin: "20px", position: "relative" , justifyContent: "center", textAlign: "center", color: "#4A2E83", fontSize: 40}}>{responseMessage}</p>
      </div>
    </div>
  </div>
}

export default GoogleDocToCanvas;