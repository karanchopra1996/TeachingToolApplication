import * as React from "react";
import { useState, useEffect } from "react";
import { styled, createTheme, ThemeProvider } from "@mui/material/styles";
import CssBaseline from "@mui/material/CssBaseline";
import MuiDrawer from "@mui/material/Drawer";
import Box from "@mui/material/Box";
import MuiAppBar from "@mui/material/AppBar";
import Toolbar from "@mui/material/Toolbar";
import List from "@mui/material/List";
import Typography from "@mui/material/Typography";
import Divider from "@mui/material/Divider";
import IconButton from "@mui/material/IconButton";
import Container from "@mui/material/Container";
import Grid from "@mui/material/Grid";
import Link from "@mui/material/Link";
import MenuIcon from "@mui/icons-material/Menu";
import ChevronLeftIcon from "@mui/icons-material/ChevronLeft";
import { MainListItems } from "./listItems";
import { SecondaryListItems } from "./listItems";
import FormControl from "@mui/material/FormControl";
import Select from "@mui/material/Select";
import InputLabel from "@mui/material/InputLabel";
import MenuItem from "@mui/material/MenuItem";
import FavoriteIcon from "@mui/icons-material/Favorite";
import LoginButton from "./pages/CanvasLogin";
import Welcome from "./pages/Welcome.js";
import Tabs from "@mui/material/Tabs";
import Tab from "@mui/material/Tab";

//-----------------------------------------------------------------------------------------------
var numOfClicks = 0;
const canvas = document.createElement("canvas");
const context = canvas.getContext("2d");
context.font = getComputedStyle(document.body).font;

function Copyright(props) {
  return (
    <Typography
      variant="body2"
      color="text.secondary"
      align="center"
      {...props}
    >
      {"Copyright © "}
      <Link color="inherit" href="https://www.uwb.edu/">
        UWB Teaching Tools
      </Link>{" "}
      {new Date().getFullYear()}
      {"."}
    </Typography>
  );
}

const drawerWidth = 375;

const AppBar = styled(MuiAppBar, {
  shouldForwardProp: (prop) => prop !== "open",
})(({ theme, open }) => ({
  zIndex: theme.zIndex.drawer + 1,
  transition: theme.transitions.create(["width", "margin"], {
    easing: theme.transitions.easing.sharp,
    duration: theme.transitions.duration.leavingScreen,
  }),
  ...(open && {
    marginLeft: drawerWidth,
    width: `calc(100% - ${drawerWidth}px)`,
    transition: theme.transitions.create(["width", "margin"], {
      easing: theme.transitions.easing.sharp,
      duration: theme.transitions.duration.enteringScreen,
    }),
  }),
}));

const Drawer = styled(MuiDrawer, {
  shouldForwardProp: (prop) => prop !== "open",
})(({ theme, open }) => ({
  "& .MuiDrawer-paper": {
    position: "relative",
    whiteSpace: "nowrap",
    backgroundColor: "#e8e3d3",
    width: drawerWidth,
    transition: theme.transitions.create("width", {
      easing: theme.transitions.easing.sharp,
      duration: theme.transitions.duration.enteringScreen,
    }),
    boxSizing: "border-box",
    ...(!open && {
      overflowX: "hidden",
      transition: theme.transitions.create("width", {
        easing: theme.transitions.easing.sharp,
        duration: theme.transitions.duration.leavingScreen,
      }),
      width: theme.spacing(7),
      [theme.breakpoints.up("sm")]: {
        width: theme.spacing(9),
      },
    }),
  },
}));

const StyledTab = styled((props) => <Tab disableRipple {...props} />)(
  ({ theme, colorOnHover }) => ({
    borderTopLeftRadius: "10px",
    borderTopRightRadius: "10px",
    borderBottomRightRadius: "0px",
    width: "160px",
    height: "50px",
    marginBottom: "0px",
    textTransform: "none",
    "&.Mui-selected": {
      color: "var(--main-color)",
      //backgroundColor: '#4CAF50',
    },
    "&:hover": {
      backgroundColor: colorOnHover,
      "@media (hover: none)": {
        backgroundColor: "transparent",
      },
    },
  })
);

const mdTheme = createTheme();

function DashboardContent() {
  const [open, setOpen] = React.useState(false); //toolbar to the left "drawer"
  const [courseId, setCourseId] = useState("");
  const [courseRole, setCourseRole] = useState("");
  const [favoriteCourses, setFavoriteCourse] = useState([]);
  const [roles, setRoles] = useState([]);
  const [selectedRole, setSelectedRole] = useState([]);
  const [drawer, setDrawer] = useState("temporary"); //the state of the drawer. 'temporary' == hidden, 'permanent' == visible
  const [show, setShow] = useState(false); // the state of the IconButton //opens the left "drawer"
  const [terms, setTerms] = useState([]);
  const [chosenTerm, setChosenTerm] = useState("");
  const [courseTermList, setCourseTermList] = useState([]);
  var [coursesInTerm, setCourseInTerm] = useState([]);
  const [allCourseDetails, setAllCourseDetails] = useState([]);
  const [name, setName] = useState([]);
  const [name1, setName1] = useState([]);
  const [isLoggedIn, setIsLoggedIn] = useState(false);
  const [isBatch, setIsBatch] = useState(false);
  const [selectedTab, setSelectedTab] = React.useState(0);

  const toggleDrawer = () => {
    setOpen(!open);
  };

  //This function is responsible for handling changes in the tab selection.
  const handleTabChange = (event, newValue) => {
    setSelectedTab(newValue);
    setIsBatch(newValue === 1);
  };

  const handleChange = (event) => {
    const selectedCourse = event.target.value;
    //console.log(" name ->", event.target.value.name)
    setName(selectedCourse.name);
    setCourseId(selectedCourse.id);
    setCourseRole(selectedCourse.role);
    setDrawer("permanent");
    setShow(true);
    if (numOfClicks === 0) {
      setOpen(true);
      numOfClicks++;
    }
  };
  const handleRoleChange = (event) => {
    setSelectedRole(event.target.value);
  };

  const handleTermChange = (event) => {
    var courseList = [];
    setChosenTerm(event.target.value);

    allCourseDetails.forEach((singleCourse) => {
      if (singleCourse["term"] == event.target.value) {
        var entity = {
          name: singleCourse["name"],
          id: singleCourse["id"],
          role: singleCourse["role"],
        };
        courseList.push(entity);
      }
    });

    setCourseInTerm(courseList);
  };

  useEffect(() => {
    if (isLoggedIn) {
      // Fetch favorites only if logged in
      fetch("/courseFavorites")
        .then((res) => res.json())
        .then((data) => {
          setFavoriteCourse(data.courses);
        });
    }
  }, [isLoggedIn]);

  useEffect(() => {
    if (isLoggedIn) {
      // Fetch distinct roles only if logged in
      fetch("/getDistinctRoles")
        .then((res) => res.json())
        .then((data) => {
          setRoles(data);
        });
    }
  }, [isLoggedIn]);

  useEffect(() => {
    if (isLoggedIn) {
      // Fetch terms only if logged in
      fetch("/getTerms")
        .then((res) => res.json())
        .then((data) => {
          var terms = [];
          var favorites = [];
          setAllCourseDetails(data);
          data.forEach((singleCourseDetail) => {
            if (terms.indexOf(singleCourseDetail["term"]) === -1)
              terms.push(singleCourseDetail["term"]);
          });

          terms.forEach((term) => {
            console.log(term);
          });

          setTerms(terms);
        });
    }
  }, [isLoggedIn]);

  return (
    <ThemeProvider theme={mdTheme}>
      <Box sx={{ display: "flex" }}>
        <CssBaseline />
        <AppBar
          style={{ background: "#4A2E83" }}
          position="absolute"
          open={open}
        >
          <Toolbar
            sx={{
              pr: "24px", // keep right padding when drawer closed
            }}
          >
            {show && (
              <IconButton
                edge="start"
                color="inherit"
                aria-label="open drawer"
                onClick={toggleDrawer}
                sx={{
                  marginRight: "36px",
                  ...(open && { display: "none" }),
                }}
              >
                <MenuIcon />
              </IconButton>
            )}
            <img src="UWB.png" alt="UWB" width="75" height="75" />
            <Typography
              component="h1"
              variant="h6"
              color="inherit"
              noWrap
              sx={{ flexGrow: 1 }}
            >
              <p>Teaching Tools</p>
            </Typography>
            {isLoggedIn && (
              <>
                <div>
                  <FormControl
                    fullWidth={true}
                    sx={{ m: 1, minWidth: 200, color: "white" }}
                  >
                    <InputLabel
                      sx={{ backgroundColor: "#4A2E83", color: "white" }}
                      id="demo-simple-select-label"
                    >
                      {" "}
                      Courses{" "}
                    </InputLabel>

                    <Select
                      labelId="demo-simple-select-label"
                      id="demo-simple-select-filled"
                      defaultValue="None"
                      sx={{
                        backgroundColor: "#4A2E83",
                        border: "1px solid white",
                        color: "white",
                        "& .MuiSelect-icon": { color: "white" },
                      }}
                      value={courseId}
                      onChange={handleChange}
                    >
                      {favoriteCourses.map((course) => (
                        <MenuItem key={course.name} value={course}>
                          <FavoriteIcon style={{ color: "#4A2E83" }} />
                          &ensp;{course.name}
                        </MenuItem>
                      ))}
                      <Divider />
                      {coursesInTerm.map((courseEntity) => (
                        <MenuItem key={courseEntity.name} value={courseEntity}>
                          {courseEntity.name}
                        </MenuItem>
                      ))}
                    </Select>
                  </FormControl>
                </div>
                &ensp;
                {/* <div>
                <FormControl fullWidth={true} sx={{ m: 1, minWidth: 200, color: 'white'}}>
                  <InputLabel sx={{ backgroundColor:'#4A2E83', color: 'white'}} id="demo-simple-select-label">Roles </InputLabel>
                  <Select
                    labelId="demo-simple-select-label"
                    id="demo-simple-select-filled"
                    
                    defaultValue='None'
                    sx={{backgroundColor:'#4A2E83', border: '1px solid white', color: 'white', '& .MuiSelect-icon':{color:'white'}}}
                    value={selectedRole}
                    onChange={handleRoleChange}
                  >
                    {roles.map(role => (
                      <MenuItem value={role}>
                        {role}
                      </MenuItem>
                    ))}
                    
                  </Select>
                </FormControl>
              </div> */}
                &ensp;
                <div>
                  <FormControl
                    fullWidth={true}
                    sx={{ m: 1, minWidth: 200, color: "white" }}
                  >
                    <InputLabel
                      sx={{ backgroundColor: "#4A2E83", color: "white" }}
                      id="demo-simple-select-label"
                    >
                      {" "}
                      Terms{" "}
                    </InputLabel>
                    <Select
                      labelId="demo-simple-select-label"
                      id="demo-simple-select-filled"
                      defaultValue="None"
                      sx={{
                        backgroundColor: "#4A2E83",
                        border: "1px solid white",
                        color: "white",
                        "& .MuiSelect-icon": { color: "white" },
                      }}
                      value={chosenTerm}
                      onChange={handleTermChange}
                    >
                      {terms.map((term) => (
                        <MenuItem key={term} value={term}>
                          {term}
                        </MenuItem>
                      ))}
                    </Select>
                  </FormControl>
                </div>
              </>
            )}
            &ensp; &ensp; &ensp;
            <LoginButton
              isLoggedIn={isLoggedIn}
              setIsLoggedIn={setIsLoggedIn}
              setShow={setShow}
              onLogout={() => {
                setOpen(false); //closeoolbar the left "drawer"
                setShow(false); // the state of the IconButton
                setDrawer("temporary"); //the state of the drawer. 'temporary' == hidden
              }}
            />
          </Toolbar>
        </AppBar>

        <Drawer variant={drawer} open={open}>
          <Toolbar
            sx={{
              justifyContent: "space-between",
              marginBottom: "-10px",
              marginTop: "20px",
              display: "flex",
              alignItems: "center",
              px: [1],
              backgroundColor:
                selectedTab === 0 ? "sidebarColor1" : "sidebarColor2",
            }}
          >
            <Tabs
              value={selectedTab}
              onChange={handleTabChange}
              aria-label="View Tabs"
              indicatorColor="transparent"
              centered
              sx={{
                ".MuiTabs-indicator": {
                  display: "none", // Hide the indicator line
                },
              }}
            >
              <StyledTab
                label="Class View"
                selected={selectedTab === 0}
                onClick={() => handleTabChange(null, 0)}
                colorOnHover="rgba(76, 175, 80, 0.5)" // Specify the hover color for Class View
                sx={{
                  backgroundColor:
                    selectedTab === 0
                      ? "rgba(76, 175, 80, 0.2)"
                      : "rgba(76, 175, 80, 0.2)", // 'transparent'Set the background color for the first tab
                  color: selectedTab === 0 ? "white" : "inherit", // Set the text color for the first tab
                  marginTop: selectedTab === 0 ? "-2.5px" : "-2.5px",
                }}
              />
              <StyledTab
                label="Batch View"
                selected={selectedTab === 1}
                onClick={() => handleTabChange(null, 1)}
                colorOnHover="rgba(74,46,131, 0.5)" // Specify the hover color for Batch View
                sx={{
                  backgroundColor:
                    selectedTab === 1
                      ? "rgba(74,46,131, 0.2)"
                      : "rgba(74,46,131, 0.2)", // Set the background color for the second tab
                  color: selectedTab === 1 ? "white" : "inherit", // Set the text color for the second tab
                  marginTop: selectedTab === 1 ? "-2.5px" : "-2.5px",
                }}
              />
            </Tabs>

            <IconButton onClick={toggleDrawer}>
              <ChevronLeftIcon />
            </IconButton>
          </Toolbar>
          <Divider />

          {/* Conditional rendering of list items based on isBatch state */}
          <List
            sx={{
              backgroundColor:
                selectedTab === 0
                  ? `rgba(76, 175, 80, 0.2)`
                  : "rgba(74,46,131, 0.2)", // Set the background color for the first tab
              color: selectedTab === 0 ? "inherit" : "inherit", // Set the text color for the first tab
            }}
          >
            {isBatch
              ? MainListItems(courseId, courseRole, name)
              : SecondaryListItems(courseId, courseRole, name)}
          </List>

          <Divider />
        </Drawer>
        <Box
          component="main"
          sx={{
            backgroundColor: (theme) =>
              theme.palette.mode === "light"
                ? theme.palette.grey[100]
                : theme.palette.grey[900],
            flexGrow: 1,
            height: "100vh",
            overflow: "auto",
          }}
        >
          <Container maxWidth="lg" sx={{ mt: 4, mb: 4 }}>
            {
              isLoggedIn ? (
                <div id="page" /> //*------------Where the feature pages are displayed-------------
              ) : (
                <Welcome />
              ) //when you logout it will go back to the Welcome page
            }

            <Grid container spacing={3}></Grid>
            <Copyright sx={{ pt: 4 }} />
          </Container>
        </Box>
      </Box>
    </ThemeProvider>
  );
}

export default function Dashboard() {
  return <DashboardContent />;
}

// Object.keys(data).forEach(function(key) {
//   if (termsArr.indexOf(data[key])  == -1)
//   {
//     termsArr.push(data[key]);
//   }
// });

// useEffect(() => {
//   fetch("/getCourseTerms").then(res => res.json()).then(data => {
//   console.log(data)

//   var termsArr = [];
//   setCourseTermList(data)
//   Object.keys(data).forEach(function(key) {
//     if (termsArr.indexOf(data[key])  == -1)
//     {
//       termsArr.push(data[key]);
//     }
//   });
//   console.log("Array =>", termsArr)
//   setTerms(termsArr)
//   })
// }, [])

// Object.keys(courseTermList).forEach(function(key)
//     {

//         if (courseTermList[key] == event.target.value )
//         courseList.push(key)
//     })
