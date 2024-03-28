import React, { useState, useEffect } from "react";
//import Box from '@mui/material/Box';
import TextField from '@mui/material/TextField';
import Button from '@mui/material/Button';
import FormControl from '@mui/material/FormControl';
import Select from '@mui/material/Select';
import InputLabel from '@mui/material/InputLabel';
import MenuItem from '@mui/material/MenuItem';



function QuizSubmission(courseId) {
   const [responseMessage, setResponse] = useState("")
   const [QuizList, setQuizList] = useState([])
   const [choosenQuiz, setChoosenQuiz] = useState("")

   const handleChange = (event) => {
      setChoosenQuiz(event.target.value)
    }

   useEffect(() => {
    setQuizList([])
      fetch("/listQuizzes",{
               method:'POST',
               headers : {
              'Content-Type':'application/json'
        },
        body:JSON.stringify({
          "courseID": courseId.courseId.toString(),
        })
      })
      .then(response => response.json()).then(data => {
        setQuizList(data.response)
      })
    // eslint-disable-next-line react-hooks/exhaustive-deps
    }, [courseId.courseId])
   
   const handleSubmit = (e)=> {
      e.preventDefault()//prevent refreashing page
      setResponse("Submitted, please wait for a response.")
      if(choosenQuiz){
      //no error, send to flask
      fetch("/downloadQuizSubmissions",{
            method:'POST',
            headers : {
            'Content-Type':'application/json'
        },
        body:JSON.stringify({
          "courseID": courseId.courseId.toString(),
          "Quiz_ID": choosenQuiz.toString()
        })
      })
      .then(response => response.json()).then(data => {
        setResponse(data['Response'])
      });  
      }  
   }
   
   return (
   <div style={{textAlign: "center", color: "#4A2E83"}}>
      <h1 style={{paddingTop: "60px", fontSize: 60}}>Download All Submissions for a Quiz</h1>
      <p>
      In this function, please select the Quiz from the dropdown that you'd like to download submissions for.
      </p>
      <div>
      <FormControl sx={{width: 200 }}>
              <InputLabel id="demo-multiple-name-label">Select Quiz</InputLabel>
              <Select
                labelId="demo-multiple-name-label"
                id="demo-multiple-name"
                defaultValue='None'
                value={choosenQuiz}
                onChange={handleChange}
              >
                {QuizList.map(quiz => (
                  <MenuItem
                    key={quiz.name}
                    value={quiz.id}
                  >
                    {quiz.name}
                  </MenuItem>
                ))}
              </Select>
            </FormControl>
            <div>
               <Button onClick={handleSubmit} style={{margin: "20px", position: "relative" , justifyContent: "center", alignItems: "center", backgroundColor:'#4A2E83'}} type="submit" variant="contained">Download Submissions</Button>
            </div>
         </div>
      <div>
        <p style={{margin: "20px", position: "relative" , justifyContent: "center", alignItems: "center", color: "#4A2E83", fontSize: 40}}>{responseMessage}</p>
      </div>
   </div>
   )
}

export default QuizSubmission