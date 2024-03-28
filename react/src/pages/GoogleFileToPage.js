import React, { useState, useEffect } from "react";
//import Box from '@mui/material/Box';
import TextField from '@mui/material/TextField';
import Button from '@mui/material/Button';
import Autocomplete from '@mui/material/Autocomplete';
import CircularProgress from '@mui/material/CircularProgress';

function sleep(delay = 0) {
   return new Promise((resolve) => {
     setTimeout(resolve, delay);
   });
 }

function DriveFileToPage(courseId) {
   const [open, setOpen] = useState(false);
   const [options, setOptions] = useState([]);
   const [googleFileID, setGoogleFileID] = useState("")
   const [googleFile, setGoogleFile] = useState("")
   const [responseMessage, setResponse] = useState("")
   const [googleFiles, setGoogleFiles] = useState([])
   const [statusMessage, setStatus] = useState("Please wait for us to retrieve your google files.")

   const loading = open && options.length === 0;

   useEffect(() => {
     setOptions([])
     setGoogleFiles([])
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
    }, [loading, googleFiles]);
  
    useEffect(() => {
      if (!open) {
        setOptions([]);
      }
    }, [open]);

   const handleGoogleFile = (event, value) => {
    console.log("handleGoogleFile")
      if(value !== null){
         setGoogleFileID(value['id'])
         setGoogleFile(value['title'])
      }
   }
   
   const handleSubmit = (e)=> {
    console.log("handleSubmit")
      e.preventDefault()//prevent refreashing page
      setResponse("Submitted, please wait for a response.")
      if(googleFile){
      //no error, send to flask
      fetch("/getDriveFileToCanvas",{
            method:'POST',
            headers : {
            'Content-Type':'application/json'
        },
        body:JSON.stringify({
          "courseID": courseId.courseId.toString(),
          "Google_FileID": googleFileID.toString(),
          "Google_File": googleFile.toString(),
        })
      })
      .then(response => response.json()).then(data => {
        setResponse(data['Response'])
      });  
      }  
   }
   
   return (
   <div style={{textAlign: "center", color: "#4A2E83"}}>
      <h1 style={{paddingTop: "60px", fontSize: 60}}>Convert a Google Drive file to a Canvas Page</h1>
      <p>
      In this function convert a Google Drive file to a Canvas Page in a selected course.
      </p>
      <p style={{margin: "20px", position: "relative" , justifyContent: "center", textAlign: "center", color: "red", fontWeight: 'bold'}}>
      Please note only google drive native files can be 
      imported to canvas currently.
    </p>
      <p style={{fontWeight: 'bold'}}>{statusMessage}</p>
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
      <div>
         <Button onClick={handleSubmit} style={{marginTop: "80px", position: "relative" , justifyContent: "center", alignItems: "center",backgroundColor:'#4A2E83'}} type="submit" variant="contained">Import to Canvas Page</Button>
      </div>
      <div>
        <p style={{margin: "20px", position: "relative" , justifyContent: "center", alignItems: "center", color: "#4A2E83", fontSize: 40}}>{responseMessage}</p>
      </div>
   </div>
   )
}

export default DriveFileToPage