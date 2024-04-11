import React, { useState, useEffect } from "react";
import Button from "@mui/material/Button";
import FormControl from "@mui/material/FormControl";
import InputLabel from "@mui/material/InputLabel";
import Select from "@mui/material/Select";
import MenuItem from "@mui/material/MenuItem";
import TextField from "@mui/material/TextField";
import { display } from "@mui/system";

function QTIQuizManager({ courseId }) {
  const [screenToShow, setScreenToShow] = useState("");
  const [courseOption, setCourseOption] = useState("");
  const [quizType, setQuizType] = useState("");
  const [selectedFile, setSelectedFile] = useState(null);
  const [statusMessage, setStatusMessage] = useState("");

  // for import function 
  const [quizName, setQuizName] = useState("");

  //for export function 
  const [choosenQuiz, setChoosenQuiz] = useState('')
  const [QuizList, setQuizList] = useState([])

  //get quizes list to choose which one to export 
  useEffect(() => {
    setQuizList([])
    fetch("/listQuizzes", {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({
        "courseID": courseId,
      })
    })
      .then(response => response.json()).then(data => {
        setQuizList(data.response)
      })
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [courseId.courseId])

  //gets Quiz and a name of the quiz to be create from the user throuh form and calls the api made in app.py 
  const importQTIQuiz = async () => {
    try {
      const formData = new FormData();
      formData.append("file", selectedFile);
      formData.append("quizName", quizName);
      formData.append("courseId", courseId);
      const options = {
        method: "POST",
        body: formData,
      };
      const response = await fetch(
        "http://127.0.0.1:5000/importQTIQuiz",
        options
      );
      const result = await response.json();
      console.log(result);
    } catch (err) {
      console.log(err.message);
    }
  };

  const handleChange = (event) => {
    setQuizName(event.target.value);
  };

  const handleScreenChange = (screen) => {
    setScreenToShow(screen);
    setStatusMessage(""); // Reset status message when changing screens
  };

  const handleFileChange = (event) => {
    setSelectedFile(event.target.files[0]);
  };

  const handleSubmit = async (event) => {
    event.preventDefault();
    console.log(quizName);
    console.log(selectedFile);
    importQTIQuiz();
  };

  const exportQuiz = async (event) => {
    event.preventDefault();
    console.log(choosenQuiz)
    try {
      const formData = new FormData();
      formData.append("quizId", choosenQuiz);
      formData.append("courseId", courseId);
      const options = {
        method: "POST",
        body: formData,
      };
      const response = await fetch(
        "http://127.0.0.1:5000/exportQTIQuiz",
        options
      );
      const result = await response.json();
      console.log(result);
    } catch (err) {
      console.log(err.message);
    }
  }

  const exportAllQuizzes = async () => {
    try {
      const formData = new FormData();
      formData.append("courseId", courseId);
      const options = {
        method: "POST",
        body: formData,
      };
      const response = await fetch(
        "http://127.0.0.1:5000/exportAllQTI",
        options
      );
      const result = await response.json();
      console.log(result);
    } catch (err) {
      console.log(err.message);
    }
  }

  const containerStyle = {
    marginTop: "100px",
  }

  const labelStyle = {
    marginLeft: "15px"
  }

  return (
    <div align="center">
      {screenToShow === "" && (
        <>
          <h1>QTI Quiz Manager</h1>
          <Button
            variant="contained"
            color="primary"
            onClick={() => handleScreenChange("import")}
          >
            IMPORT
          </Button>
          <Button
            variant="contained"
            color="secondary"
            onClick={() => handleScreenChange("export")}
            style={{ marginLeft: "10px" }}
          >
            EXPORT
          </Button>
        </>
      )}
      {(screenToShow === "import") && (
        <>
          <div style={containerStyle}>
            <h1>Import Quiz in Qti Format</h1>
            <form onSubmit={handleSubmit}>
              <label>
                Quiz Name
                <input type="text" name="text" onChange={handleChange} />
              </label>
              <label style={labelStyle}>
                choose quiz
                <input type="file" name="file" onChange={handleFileChange} />
              </label>
              <Button
                variant="contained"
                color="primary"
                type="submit"
              >
                IMPORT
              </Button>
            </form>
            <Button
              variant="contained"
              color="error"
              type="submit"
              onClick={() => setScreenToShow('')}
            >
              back
            </Button>
          </div>
        </>
      )}
      {(screenToShow === "export") && (
        <>
          <div style={containerStyle}>
            <h1>export Quiz in Qti format</h1>
            <form>
              <label>Select Quiz</label>
              <Select
                labelId="demo-multiple-name-label"
                id="demo-multiple-name"
                defaultValue='None'
                value={choosenQuiz}
                onChange={(event) => setChoosenQuiz(event.target.value)}
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
              <Button
                variant="contained"
                color="secondary"
                style={{ marginLeft: "10px" }}
                onClick={exportQuiz}
              >
                Export selected Quiz
              </Button>
              <Button
                variant="contained"
                color="secondary"
                style={{ marginLeft: "10px" }}
                onClick={exportAllQuizzes}
              >
                Export every Quiz
              </Button>
            </form>
            <Button
              variant="contained"
              color="error"
              onClick={() => setScreenToShow('')}
            >
              BACK
            </Button>
          </div>
        </>
      )
      }
    </div >
  );
}

export default QTIQuizManager;
//-----------------------------------------------------------------------------------------------------------------------------
