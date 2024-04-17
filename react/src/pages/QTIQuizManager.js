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
      setStatusMessage("Creating the Quiz")
      const response = await fetch(
        "http://127.0.0.1:5000/importQTIQuiz",
        options
      );
      const result = await response.json();
      console.log(result);
      setStatusMessage('created Quiz Sucessfully')
      setTimeout(() => {
        setStatusMessage("")
      }, 3000)
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

  return (
    <div align="center">
      {screenToShow === "" && (
        <>
          <h1 style={{ paddingTop: "60px", fontSize: 60, color: "#4A2E83" }}>Qti Quiz Manager</h1>
          <p
            style={{
              color: "#4a2e83",
            }}
          >In this function we Import/Export a Quiz in Qti format</p>

          <Button
            variant="contained"
            color="primary"
            style={{
              backgroundColor: "#4A2E83",
              height: "40px", width: "150px",
            }}
            onClick={() => handleScreenChange("import")}
          >
            IMPORT
          </Button>
          <Button
            variant="contained"
            color="secondary"
            onClick={() => handleScreenChange("export")}
            style={{
              marginLeft: "10px",
              backgroundColor: "#4A2E83",
              height: "40px", width: "150px",
            }}
          >
            EXPORT
          </Button>
        </>
      )}
      {(screenToShow === "import") && (
        <>
          <div>
            <h1 style={{ paddingTop: "60px", fontSize: 60, color: "#4A2E83" }}>Import Quiz In Qti Format</h1>
            <p
              style={{
                color: "#4a2e83",
              }}
            >In this function we Import a Quiz in Qti format</p>
            <form
              style={{
                display: "flex",
                flexDirection: "column"
              }}
              onSubmit={handleSubmit}>
              <label
                style={{
                  color: "#4a2e83",
                  marginBottom: "15px",
                  fontWeight: "700"
                }}
              >
                Quiz Name
                <input type="text"
                  style={{ marginLeft: "15px" }}
                  name="text" onChange={handleChange} />
              </label>
              <label style={{
                color: "#4A2E83",
                marginLeft: "70px",
                fontWeight: "700"
              }}>
                choose quiz
                <input type="file"
                  style={{
                    marginLeft: "15px"
                  }}
                  name="file" onChange={handleFileChange} />
              </label>
              <Button
                variant="contained"
                color="primary"
                type="submit"
                style={{
                  backgroundColor: "#4A2E83",
                  height: "40px", width: "300px",
                  marginLeft: "37%",
                  marginTop: "15px",
                  marginBottom: "15px"
                }}
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
      )
      }
      {
        (screenToShow === "export") && (
          <>
            <div>
              <h1 style={{ paddingTop: "60px", fontSize: 60, color: "#4A2E83" }}>Export Quiz In Qti Format</h1>
              <form style={{ display: "flex", flexDirection: "column" }}>
                <label
                  style={{
                    marginBottom: "15px",
                    color: "#4A2E83"
                  }}
                >In this function, please select the Quiz from the dropdown that you'd like to export in Qti format</label>
                <Select
                  labelId="demo-multiple-name-label"
                  id="demo-multiple-name"
                  defaultValue='None'
                  value={choosenQuiz}
                  style={{
                    height: "40px", width: "300px",
                    marginLeft: "37%"
                  }}
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
                  style={{
                    marginLeft: "37%",
                    marginBottom: "25px",
                    marginTop: "25px",
                    height: "40px", width: "300px",
                    backgroundColor: "#4A2E83"
                  }}
                  onClick={exportQuiz}
                >
                  Export selected Quiz
                </Button>
                <Button
                  variant="contained"
                  color="secondary"
                  style={{
                    marginLeft: "37%",
                    marginBottom: "25px",
                    height: "40px", width: "300px",
                    backgroundColor: "#4A2E83"
                  }}
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
      {(true) ? (<div>
        <p style={{ margin: "20px", position: "relative", justifyContent: "center", alignItems: "center", color: "#4A2E83", fontSize: 40 }}>{statusMessage}</p>
      </div>
      ) : (<div>testing again</div>)}
    </div >
  );
}

export default QTIQuizManager;
//-----------------------------------------------------------------------------------------------------------------------------
