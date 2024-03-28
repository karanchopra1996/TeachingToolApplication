import * as React from 'react';
import { useState, useEffect } from 'react';

import List from '@mui/material/List';
import Collapse from '@mui/material/Collapse';
import ListItem from '@mui/material/ListItem';
import ListItemIcon from '@mui/material/ListItemIcon';
import ListItemText from '@mui/material/ListItemText';
import ListSubheader from '@mui/material/ListSubheader';
import ListItemButton from '@mui/material/ListItemButton';
import Tooltip from '@mui/material/Tooltip';
import ExpandLess from '@mui/icons-material/ExpandLess';
import HorizontalRuleIcon from '@mui/icons-material/HorizontalRule';
import ExpandMore from '@mui/icons-material/ExpandMore';
import SettingsIcon from '@mui/icons-material/Settings';
import DashboardIcon from '@mui/icons-material/Dashboard';
import FileUploadIcon from '@mui/icons-material/FileUpload';
import FileDownloadIcon from '@mui/icons-material/FileDownload';
import QuizIcon from '@mui/icons-material/Quiz';
import GroupsIcon from '@mui/icons-material/Groups';
import AddToDriveIcon from '@mui/icons-material/AddToDrive';
import FolderIcon from '@mui/icons-material/Folder';
import AssignmentIcon from '@mui/icons-material/Assignment';
import SchoolOutlinedIcon from '@mui/icons-material/SchoolOutlined';
import SchoolIcon from '@mui/icons-material/School';
import GoogleIcon from '@mui/icons-material/Google';
import PeopleIcon from '@mui/icons-material/People';
import TextSnippetIcon from '@mui/icons-material/TextSnippet';
import ArticleIcon from '@mui/icons-material/Article';
import AttachFileIcon from '@mui/icons-material/AttachFile';
import ClassIcon from '@mui/icons-material/Class';
import MenuBookIcon from '@mui/icons-material/MenuBook';
import CreateNewFolderIcon from '@mui/icons-material/CreateNewFolder';
import AssignmentReturnedIcon from '@mui/icons-material/AssignmentReturned';
import DownloadForOfflineIcon from '@mui/icons-material/DownloadForOffline';
import ImportExportIcon from '@mui/icons-material/ImportExport';
import ShareIcon from '@mui/icons-material/Share';
import FolderSharedIcon from '@mui/icons-material/FolderShared';
import DescriptionIcon from '@mui/icons-material/Description';
import SubjectIcon from '@mui/icons-material/Subject';
import ReactDOM from 'react-dom';
import Welcome from './pages/Welcome';
import ExportCourseRoster from './pages/ExportCourseRoster';
import GoogleDocToCanvas from './pages/GoogleDocToCanvas';
import GoogleFileToFile from './pages/GoogleFileToFile';
import CanvasPageToDrive from './pages/CanvasPageToDrive';
import DriveFileToPage from './pages/GoogleFileToPage';
import DownloadSyllabus from './pages/DownloadSyllabus';
import DownloadAssignments from './pages/Assignments';
import DownloadQuizzes from './pages/Quizzes';
import ImportStudents from './pages/ImportStudents';
import ExportStudents from './pages/ExportStudents';
import CanvasSettings from './pages/CanvasSettings';
import SettingsFromFile from './pages/SettingsFromFile';
import ExportSettings from './pages/ExportSettings';
import AssignmentSubmission from './pages/AssignmentSubmissions';
import QuizSubmission from './pages/QuizSubmissions';
import ExportSyllabus from './pages/ExportSyllabus';
import SubmitAssignment from './pages/SubmitAssignment';
import WorkspaceFileToFile from './pages/WorkspaceFileToFile';
import CanvasFolder from './pages/CanvasFolder';
import GoogleFolder from './pages/GoogleFolder';
import DriveSharedFolder from './pages/DriveSharedFolder';
import SharedGroupFolders from './pages/SharedGroupFolders';
import ExportAssignmentContributors from "./pages/ExportAssignmentGroups"
import UploadFileRoundedIcon from '@mui/icons-material/UploadFileRounded';
import DownloadIcon from '@mui/icons-material/Download';
import PeopleAltIcon from '@mui/icons-material/PeopleAlt';
import QTIQuizManager from './pages/QTIQuizManager';   // Import the QTQuizManager component

//-----------------------------------------------------------------------------------------------
export function MainListItems(courseId, courseRole, name ) {
  console.log(" name in mainlist =>", name)
  const [open, setOpen] = useState(false);
  const [gOpen, gSetOpen] = useState(false);
  const [settingsOpen, settingsSetOpen] = useState(false);
  const [coursesOpen, coursesSetOpen] = useState(true);
  const [page, setPage] = useState('Dashboard')
  const [googOpen, googSetOpen] = useState(false);
  const [canOpen, canSetOpen] = useState(false);

  // New state for managing the open/close status of QTQuizManager in the list
 const [qtQuizManagerOpen, setQtQuizManagerOpen] = useState(false);
  
 
  
  const handleClick = () => {
    setOpen(!open);
  };
  const groupsHandleClick = () => {
    gSetOpen(!gOpen);
  };
  const settingsHandleClick = () => {
    settingsSetOpen(!settingsOpen);
  };
  const coursesHandleClick = () => {
    coursesSetOpen(!coursesOpen);
  };
  const googHandleClick = () => {
    googSetOpen(!googOpen);
  };
  const canHandleClick = () => {
    canSetOpen(!canOpen);
  };
// Handle click for QTQuizManager
  const qtQuizManagerHandleClick = () => {
    setQtQuizManagerOpen(!qtQuizManagerOpen);
  };



  //Re-renders the page with the updated course id if the course is changed while inside the page 
  useEffect(() => {
    switch (page) {
      case 'Settings':
        ReactDOM.render(<React.StrictMode><CanvasSettings courseId={courseId} /></React.StrictMode>, document.getElementById('page'));
        console.log('Settings');
        break;
      case 'Export':
        ReactDOM.render(<React.StrictMode><ExportStudents courseId={courseId} /></React.StrictMode>, document.getElementById('page'));
        console.log('Export');
        break;
      case 'Import':
        ReactDOM.render(<React.StrictMode><ImportStudents courseId={courseId} /></React.StrictMode>, document.getElementById('page'));
        console.log('Import');
        break;
      case 'SettingsFile':
        ReactDOM.render(<React.StrictMode><SettingsFromFile courseId={courseId} /></React.StrictMode>, document.getElementById('page'));
        console.log('SettingsFile');
        break;
      case 'ExportSettings':
        ReactDOM.render(<React.StrictMode><ExportSettings courseId={courseId} /></React.StrictMode>, document.getElementById('page'));
        console.log('ExportSettings');
        break;
      case 'ExportCourseRoster':
        console.log('ExportCourseRoster');
        ReactDOM.render(<React.StrictMode><ExportCourseRoster courseId={courseId} /></React.StrictMode>, document.getElementById('page'));
        
        break;
      case 'ExportAssignments':
        ReactDOM.render(<React.StrictMode><DownloadAssignments courseId={courseId} /></React.StrictMode>, document.getElementById('page'));
        console.log('ExportAssignments');
        break;
      case 'ExportQuizzes':
        ReactDOM.render(<React.StrictMode><DownloadQuizzes courseId={courseId} /></React.StrictMode>, document.getElementById('page'));
        console.log('ExportQuizzes');
        break;
      case 'ExportSyllabus':
        ReactDOM.render(<React.StrictMode><ExportSyllabus courseId={courseId} isMainList={true} /></React.StrictMode>, document.getElementById('page'));
        console.log('ExportSyllabus');
        break;
      case 'DownloadAssignmentSubmissions':
        ReactDOM.render(<React.StrictMode><AssignmentSubmission courseId={courseId} /></React.StrictMode>, document.getElementById('page'));
        console.log('DownloadAssignmentSubmissions');
        break;
      case 'DownloadQuizSubmissions':
        ReactDOM.render(<React.StrictMode><QuizSubmission courseId={courseId} /></React.StrictMode>, document.getElementById('page'));
        console.log('DownloadQuizSubmissions');
        break;
      case 'GoogleDocToCanvas':
        ReactDOM.render(<React.StrictMode><GoogleDocToCanvas courseId={courseId} /></React.StrictMode>, document.getElementById('page'));
        console.log('GoogleDocToCanvas');
        break;
      case 'GoogleFileToFile':
        ReactDOM.render(<React.StrictMode><GoogleFileToFile courseId={courseId} /></React.StrictMode>, document.getElementById('page'));
        console.log('GoogleFileToFile');
        break;
      case 'WorkspaceFileToFile':
        ReactDOM.render(<React.StrictMode><WorkspaceFileToFile courseId={courseId} /></React.StrictMode>, document.getElementById('page'));
        console.log('WorkspaceFileToFile');
        break;
      case 'DriveSharedFolder':
        ReactDOM.render(<React.StrictMode><DriveSharedFolder courseId={courseId} /></React.StrictMode>, document.getElementById('page'));
        console.log('DriveSharedFolder');
        break;
      case 'CanvasFolder':
        ReactDOM.render(<React.StrictMode><CanvasFolder courseId={courseId} /></React.StrictMode>, document.getElementById('page'));
        console.log('CanvasFolder');
        break;
      case 'GoogleFolder':
        ReactDOM.render(<React.StrictMode><GoogleFolder courseId={courseId} /></React.StrictMode>, document.getElementById('page'));
        console.log('GoogleFolder');
        break;
      case 'SharedGroupFolders':
        ReactDOM.render(<React.StrictMode><SharedGroupFolders courseId={courseId} /></React.StrictMode>, document.getElementById('page'));
        console.log('SharedGroupFolders');
        break;
      case 'PageToDoc':
        ReactDOM.render(<React.StrictMode><CanvasPageToDrive courseId={courseId} /></React.StrictMode>, document.getElementById('page'));
        console.log('PageToDoc');
        break;
      case 'DocToPage':
        ReactDOM.render(<React.StrictMode><DriveFileToPage courseId={courseId} /></React.StrictMode>, document.getElementById('page'));
        console.log('DocToPage');
        break;
      case 'SyllabusToDoc':
        ReactDOM.render(<React.StrictMode><DownloadSyllabus courseId={courseId} /></React.StrictMode>, document.getElementById('page'));
        console.log('SyllabusToDoc');
        break;
      case 'SubmitAssignment':
        ReactDOM.render(<React.StrictMode><SubmitAssignment courseId={courseId} /></React.StrictMode>, document.getElementById('page'));
        console.log('Assignmnet Deatils');
        break;
      case "ExportAssignmentContributors":
        ReactDOM.render(<React.StrictMode><ExportAssignmentContributors courseId={courseId} /></React.StrictMode>, document.getElementById('page'));
        console.log('Assignment Group Deatils');
        break;

      // Add a new case for 'QTQuizManager'
      case 'QTQuizManager':
        ReactDOM.render(<React.StrictMode><QTIQuizManager courseId={courseId} /></React.StrictMode>, document.getElementById('page'));
        console.log('QTQuizManager');
        break;

      case 'Dashboard':
        console.log('Dashboard Page');
        break;
      default:
        console.log('Dashboard');
      //Dashboard is the default, but no need to re-render unless new functioanlity is added.
    }

  }, [courseId != ''])//anytime courseId is changed, this useEffect is ran
//----------------------------------------------------------------------------------------------------------------------------------
  function SidebarIcon(props) {
    return (
      
      <Tooltip title={props.desc} placement="right">
        <ListItemButton sx={{ pl: 4 }} onClick={() => {
          ReactDOM.render(<React.StrictMode><props.pageClass courseId={props.courseId} /></React.StrictMode>, document.getElementById('page'));
          setPage(props.pageRender);
        }}>
          <ListItemIcon>
            <props.icon />
          </ListItemIcon>
          
          <ListItemText primary={props.desc} />
        </ListItemButton>
      </Tooltip>
    );
  }
  function FeatureGroupIcon(props) {
    return (
      <Tooltip title={props.desc} placement="right">
        <ListItemButton onClick={props.function}>
          <ListItemIcon>
            <props.icon />
          </ListItemIcon>
          <ListItemText primary={props.desc} />
          {props.expand ? <ExpandLess /> : <ExpandMore />}
        </ListItemButton>
      </Tooltip>
    );
  }

//----------------------------------------------------------------BATCH VIEW--------------------------------------------------------
  

return (
    <div>
      <div style={{textAlign: "center", color: "#585858", fontWeight: 'bold', marginBottom: 10}}> Batch View </div>
      <Tooltip title="Dashboard" placement="right">
        <ListItemButton onClick={() => {
          ReactDOM.render(<React.StrictMode><Welcome /></React.StrictMode>, document.getElementById('page'));
          setPage('Dashboard');
        }}>
          <ListItemIcon>
            <DashboardIcon />
          </ListItemIcon>
          <ListItemText primary="Dashboard" />
        </ListItemButton>
      </Tooltip>

      <FeatureGroupIcon desc="Courses" function={coursesHandleClick} icon={ClassIcon} expand={coursesOpen} ></FeatureGroupIcon>
      <Collapse in={coursesOpen} timeout="auto" unmountOnExit>
        <List component="div" disablePadding>
        <SidebarIcon courseId={courseId} desc="Export Syllabus" pageClass={() => ExportSyllabus(courseId, true)} pageRender="ExportSyllabus" icon={DownloadIcon}></SidebarIcon>
        </List>
      </Collapse>

      <FeatureGroupIcon desc="Canvas Groups" function={groupsHandleClick} icon={GroupsIcon} expand={gOpen} ></FeatureGroupIcon>
      <Collapse in={gOpen} timeout="auto" unmountOnExit>
        <List component="div" disablePadding>
          <SidebarIcon courseId={courseId} desc="Import Groups" pageClass={ImportStudents} pageRender="Import" icon={FileUploadIcon}></SidebarIcon>
          <SidebarIcon courseId={courseId} desc="Export Groups" pageClass={ExportStudents} pageRender="Export" icon={FileDownloadIcon}></SidebarIcon>
          <SidebarIcon courseId={courseId} desc="Group Folders" pageClass={SharedGroupFolders} pageRender="SharedGroupFolders" icon={GroupsIcon}></SidebarIcon>
        </List>
      </Collapse>

      <FeatureGroupIcon desc="Canvas Settings" function={settingsHandleClick} icon={SettingsIcon} expand={settingsOpen} ></FeatureGroupIcon>
      <Collapse in={settingsOpen} timeout="auto" unmountOnExit>
        <List component="div" disablePadding>
          <SidebarIcon courseId={courseId} desc="Import from Course" pageClass={CanvasSettings} pageRender="Settings" icon={ImportExportIcon}></SidebarIcon>
          <SidebarIcon courseId={courseId} desc="Import from File" pageClass={SettingsFromFile} pageRender="SettingsFile" icon={FileUploadIcon}></SidebarIcon>
          <SidebarIcon courseId={courseId} desc="Export Settings" pageClass={ExportSettings} pageRender="ExportSettings" icon={FileDownloadIcon}></SidebarIcon>
        </List>
      </Collapse>

      <FeatureGroupIcon desc="Google Drive" function={googHandleClick} icon={GoogleIcon} expand={googOpen} ></FeatureGroupIcon>
      <Collapse in={googOpen} timeout="auto" unmountOnExit>
        <List component="div" disablePadding>
          <SidebarIcon courseId={courseId} desc="Create Google Drive Folders" pageClass={GoogleFolder} pageRender="GoogleFolder" icon={CreateNewFolderIcon}></SidebarIcon>
        </List>
      </Collapse>


      <FeatureGroupIcon desc="Canvas Files" function={canHandleClick} icon={SchoolIcon} expand={canOpen} ></FeatureGroupIcon>
      <Collapse in={canOpen} timeout="auto" unmountOnExit>
        <List component="div" disablePadding>
          <SidebarIcon courseId={courseId} desc="Create Canvas Folders" pageClass={CanvasFolder} pageRender="CanvasFolder" icon={FolderIcon}></SidebarIcon>
          <SidebarIcon courseId={courseId} desc="Page to Google Doc" pageClass={CanvasPageToDrive} pageRender="PageToDoc" icon={DescriptionIcon}></SidebarIcon>
          <SidebarIcon courseId={courseId} desc="Syllabus to Google Doc" pageClass={DownloadSyllabus} pageRender="SyllabusToDoc" icon={SubjectIcon}></SidebarIcon>
        </List>
      </Collapse>
    </div>
  );
}
//----------------------------------------------------------------BATCH VIEW END-----------------------------------------------------


//---------------------------------------------------------------CLASS VIEW----------------------------------------------------------
//Commented out in Dashboard. Can be used later.
export function SecondaryListItems(courseId1, courseRole1, name) {
 
  console.log(" name in Secondary List =>", name)
  const [open1, setOpen1] = useState(false);
  const [gOpen1, gSetOpen1] = useState(false);
  const [settingsOpen1, settingsSetOpen1] = useState(false);
  const [coursesOpen1, coursesSetOpen1] = useState(false);
  const [page1, setPage1] = useState('Dashboard')
  const [googOpen1, googSetOpen1] = useState(false);
  const [canOpen1, canSetOpen1] = useState(false);
  const [qtQuizManagerOpen1, setQtQuizManagerOpen1] = useState(false)  // Define state for managing the open/close status of each section, including QTQuizManager
  

  const handleClick1 = () => {
    setOpen1(!open1);
  };
  const groupsHandleClick1 = () => {
    gSetOpen1(!gOpen1);
  };
  const settingsHandleClick1 = () => {
    settingsSetOpen1(!settingsOpen1);
  };
  const coursesHandleClick1 = () => {
    coursesSetOpen1(!coursesOpen1);
  };

  const canHandleClick1 = () => {
    canSetOpen1(!canOpen1);
  };

  const googHandleClick1 = () => {
    googSetOpen1(!googOpen1);
  };

  // Handle click for QTQuizManager
  const qtQuizManagerHandleClick1 = () => {
  setQtQuizManagerOpen1(!qtQuizManagerOpen1);
  };


  const handUpdate = () => {
    setOpen1(false)
      gSetOpen1(false)
      settingsSetOpen1(false)
      coursesSetOpen1(false)
      setPage1(false)
      googSetOpen1(false)
      canSetOpen1(false)
      setQtQuizManagerOpen1(false)
      ReactDOM.render(<React.StrictMode><Welcome /></React.StrictMode>, document.getElementById('page'));
      setPage1('Dashboard');
  };
  // useEffect(() => {
  //   setOpen1(false)
  //   gSetOpen1(false)
  //   settingsSetOpen1(false)
  //   coursesSetOpen1(false)
  //   setPage1(false)
  //   googSetOpen1(false)
  //   canSetOpen1(false)
  //   ReactDOM.render(<React.StrictMode><Welcome /></React.StrictMode>, document.getElementById('page'));
  //   setPage1('Dashboard');
  // }, [isBatch]);
  //Re-renders the page with the updated course id if the course is changed while inside the page 

  useEffect(() => {
   
    switch (page1) {
      case 'Settings':
        ReactDOM.render(<React.StrictMode><CanvasSettings courseId={courseId1} /></React.StrictMode>, document.getElementById('page'));
        console.log('Settings');
        break;
      case 'Export':
        ReactDOM.render(<React.StrictMode><ExportStudents courseId={courseId1} /></React.StrictMode>, document.getElementById('page'));
        console.log('Export');
        break;
      case 'Import':
        ReactDOM.render(<React.StrictMode><ImportStudents courseId={courseId1} /></React.StrictMode>, document.getElementById('page'));
        console.log('Import');
        break;
      case 'SettingsFile':
        ReactDOM.render(<React.StrictMode><SettingsFromFile courseId={courseId1} /></React.StrictMode>, document.getElementById('page'));
        console.log('SettingsFile');
        break;
      case 'ExportSettings':
        ReactDOM.render(<React.StrictMode><ExportSettings courseId={courseId1} /></React.StrictMode>, document.getElementById('page'));
        console.log('ExportSettings');
        break;
      case 'ExportCourseRoster':
        console.log('ExportCourseRoster');
        ReactDOM.render(<React.StrictMode><ExportCourseRoster courseId={courseId1} /></React.StrictMode>, document.getElementById('page'));
        
        break;
      case 'ExportAssignments':
        ReactDOM.render(<React.StrictMode><DownloadAssignments courseId={courseId1} /></React.StrictMode>, document.getElementById('page'));
        console.log('ExportAssignments');
        break;
      case 'ExportQuizzes':
        ReactDOM.render(<React.StrictMode><DownloadQuizzes courseId={courseId1} /></React.StrictMode>, document.getElementById('page'));
        console.log('ExportQuizzes');
        break;
      case 'ExportSyllabus':
        ReactDOM.render(<React.StrictMode><ExportSyllabus courseId={courseId1} isMainList={false}/></React.StrictMode>, document.getElementById('page'));
        console.log('ExportSyllabus');
        break;
      case 'DownloadAssignmentSubmissions':
        ReactDOM.render(<React.StrictMode><AssignmentSubmission courseId={courseId1} /></React.StrictMode>, document.getElementById('page'));
        console.log('DownloadAssignmentSubmissions');
        break;
      case 'DownloadQuizSubmissions':
        ReactDOM.render(<React.StrictMode><QuizSubmission courseId={courseId1} /></React.StrictMode>, document.getElementById('page'));
        console.log('DownloadQuizSubmissions');
        break;
      case 'GoogleDocToCanvas':
        ReactDOM.render(<React.StrictMode><GoogleDocToCanvas courseId={courseId1} /></React.StrictMode>, document.getElementById('page'));
        console.log('GoogleDocToCanvas');
        break;
      case 'GoogleFileToFile':
        ReactDOM.render(<React.StrictMode><GoogleFileToFile courseId={courseId1} /></React.StrictMode>, document.getElementById('page'));
        console.log('GoogleFileToFile');
        break;
      case 'WorkspaceFileToFile':
        ReactDOM.render(<React.StrictMode><WorkspaceFileToFile courseId={courseId1} /></React.StrictMode>, document.getElementById('page'));
        console.log('WorkspaceFileToFile');
        break;
      case 'DriveSharedFolder':
        ReactDOM.render(<React.StrictMode><DriveSharedFolder courseId={courseId1} /></React.StrictMode>, document.getElementById('page'));
        console.log('DriveSharedFolder');
        break;
      case 'CanvasFolder':
        ReactDOM.render(<React.StrictMode><CanvasFolder courseId={courseId1} /></React.StrictMode>, document.getElementById('page'));
        console.log('CanvasFolder');
        break;
      case 'GoogleFolder':
        ReactDOM.render(<React.StrictMode><GoogleFolder courseId={courseId1} /></React.StrictMode>, document.getElementById('page'));
        console.log('GoogleFolder');
        break;
      case 'SharedGroupFolders':
        ReactDOM.render(<React.StrictMode><SharedGroupFolders courseId={courseId1} /></React.StrictMode>, document.getElementById('page'));
        console.log('SharedGroupFolders');
        break;
      case 'PageToDoc':
        ReactDOM.render(<React.StrictMode><CanvasPageToDrive courseId={courseId1} /></React.StrictMode>, document.getElementById('page'));
        console.log('PageToDoc');
        break;
      case 'DocToPage':
        ReactDOM.render(<React.StrictMode><DriveFileToPage courseId={courseId1} /></React.StrictMode>, document.getElementById('page'));
        console.log('DocToPage');
        break;
      case 'SyllabusToDoc':
        ReactDOM.render(<React.StrictMode><DownloadSyllabus courseId={courseId1} /></React.StrictMode>, document.getElementById('page'));
        console.log('SyllabusToDoc');
        break;
      case 'SubmitAssignment':
        ReactDOM.render(<React.StrictMode><SubmitAssignment courseId={courseId1} /></React.StrictMode>, document.getElementById('page'));
        console.log('Assignmnet Deatils');
        break;
      case "ExportAssignmentContributors":
        ReactDOM.render(<React.StrictMode><ExportAssignmentContributors courseId={courseId1} /></React.StrictMode>, document.getElementById('page'));
        console.log('Assignment Group Deatils');
        break;

      // Add a new case for 'QTQuizManager'
      case 'QTQuizManager':
        ReactDOM.render(<React.StrictMode><QTIQuizManager courseId={courseId1} /></React.StrictMode>, document.getElementById('page'));
        console.log('QTQuizManager');
        break;

      case 'Dashboard':
        console.log('Dashboard Page');
        break;
      default:
        console.log('Dashboard');
      //Dashboard is the default, but no need to re-render unless new functioanlity is added.
    }

  }, [courseId1 != ''])//anytime courseId1 is changed, this useEffect is ran

  function SidebarIcon(props) {
    return (
      
      <Tooltip title={props.desc} placement="right">
        <ListItemButton sx={{ pl: 4 }} onClick={() => {
          ReactDOM.render(<React.StrictMode><props.pageClass courseId={props.courseId} /></React.StrictMode>, document.getElementById('page'));
          setPage1(props.pageRender);
        }}>
          <ListItemIcon>
            <props.icon />
          </ListItemIcon>
          
          <ListItemText primary={props.desc} />
        </ListItemButton>
      </Tooltip>
    );
  }
  function FeatureGroupIcon(props) {
    return (
      <Tooltip title={props.desc} placement="right">
        <ListItemButton onClick={props.function}>
          <ListItemIcon>
            <props.icon />
          </ListItemIcon>
          <ListItemText primary={props.desc} />
          {props.expand ? <ExpandLess /> : <ExpandMore />}
        </ListItemButton>
      </Tooltip>
    );
  }

  return (
    <div>
      <div style={{textAlign: "center", color: "#585858", fontWeight: 'bold', marginBottom: 10}}> {name} </div>
      <Tooltip title="Dashboard" placement="right">
        <ListItemButton onClick={() => {
          ReactDOM.render(<React.StrictMode><Welcome /></React.StrictMode>, document.getElementById('page'));
          setPage1('Dashboard');
        }}>
          <ListItemIcon>
            <DashboardIcon />
          </ListItemIcon>
          <ListItemText primary="Dashboard" />
        </ListItemButton>
      </Tooltip>

      <FeatureGroupIcon desc="Courses" function={coursesHandleClick1} icon={ClassIcon} expand={coursesOpen1} ></FeatureGroupIcon>
      <Collapse in={coursesOpen1} timeout="auto" unmountOnExit>
        <List component="div" disablePadding>
        {(courseRole1 =='ta' || courseRole1 =='teacher' || courseRole1 =='admin') &&   <SidebarIcon courseId={courseId1} desc="Export Rosters" pageClass={ExportCourseRoster} pageRender="ExportCourseRoster" icon={PeopleIcon}></SidebarIcon>}
         <SidebarIcon courseId={courseId1} desc="Export Assignments" pageClass={DownloadAssignments} pageRender="ExportAssignments" icon={AssignmentIcon}></SidebarIcon>
        {(courseRole1 =='ta' || courseRole1 =='teacher' || courseRole1 =='admin') &&  <SidebarIcon courseId={courseId1} desc="Export Quiz Assignments" pageClass={DownloadQuizzes} pageRender="ExportQuizzes" icon={QuizIcon}></SidebarIcon>}   
          <SidebarIcon courseId={courseId1} desc="Export Syllabus" pageClass={() => ExportSyllabus(courseId1)} pageRender="ExportSyllabus" icon={DownloadIcon}></SidebarIcon>
        { (courseRole1 =='student' || courseRole1 =='admin') &&   <SidebarIcon courseId={courseId1} desc="Submit Assignment" pageClass={SubmitAssignment} pageRender="SubmitAssignment" icon={UploadFileRoundedIcon}></SidebarIcon> }
        { (courseRole1 =='ta' || courseRole1 =='teacher' ||courseRole1=='admin') &&  <SidebarIcon courseId={courseId1} desc="Export Assignment Contributors" pageClass={ExportAssignmentContributors} pageRender="Export Assignment Contributors" icon={PeopleAltIcon}></SidebarIcon>}
        { (courseRole1 =='ta' || courseRole1 =='teacher' ||courseRole1=='admin') &&   <SidebarIcon courseId={courseId1} desc="Download Assignment Submissions" pageClass={AssignmentSubmission} pageRender="DownloadAssignmentSubmissions" icon={AssignmentReturnedIcon}></SidebarIcon>}
        { (courseRole1 =='ta' || courseRole1 =='teacher' ||courseRole1=='admin') &&   <SidebarIcon courseId={courseId1} desc="Download Quiz Submissions" pageClass={QuizSubmission} pageRender="DownloadQuizSubmissions" icon={DownloadForOfflineIcon}></SidebarIcon>}
        { (courseRole1 =='ta' || courseRole1 =='teacher' || courseRole1 =='admin') && <SidebarIcon courseId={courseId1} desc="QTI Quiz Manager" pageClass={QTIQuizManager} pageRender="QTIQuizManager" icon={QuizIcon}></SidebarIcon>} {/* Added QTIQuizManager option */}
        </List>
      </Collapse>


      <FeatureGroupIcon desc="Canvas Settings" function={settingsHandleClick1} icon={SettingsIcon} expand={settingsOpen1} ></FeatureGroupIcon>
      <Collapse in={settingsOpen1} timeout="auto" unmountOnExit>
        <List component="div" disablePadding>
          <SidebarIcon courseId={courseId1} desc="Import from Course" pageClass={CanvasSettings} pageRender="Settings" icon={ImportExportIcon}></SidebarIcon>
          <SidebarIcon courseId={courseId1} desc="Import from File" pageClass={SettingsFromFile} pageRender="SettingsFile" icon={FileUploadIcon}></SidebarIcon>
          <SidebarIcon courseId={courseId1} desc="Export Settings" pageClass={ExportSettings} pageRender="ExportSettings" icon={FileDownloadIcon}></SidebarIcon>
        </List>
      </Collapse>

      <FeatureGroupIcon desc="Google Drive" function={googHandleClick1} icon={GoogleIcon} expand={googOpen1} ></FeatureGroupIcon>
      <Collapse in={googOpen1} timeout="auto" unmountOnExit>
        <List component="div" disablePadding>
          <SidebarIcon courseId={courseId1} desc="File to Canvas File" pageClass={GoogleFileToFile} pageRender="GoogleFileToFile" icon={AttachFileIcon}></SidebarIcon>
          <SidebarIcon courseId={courseId1} desc="Workspace File To File" pageClass={WorkspaceFileToFile} pageRender="WorkspaceFileToFile" icon={TextSnippetIcon}></SidebarIcon>
          <SidebarIcon courseId={courseId1} desc="Create Google Drive Folders" pageClass={GoogleFolder} pageRender="GoogleFolder" icon={CreateNewFolderIcon}></SidebarIcon>
          <SidebarIcon courseId={courseId1} desc="Sharing Drive Files" pageClass={DriveSharedFolder} pageRender="DriveSharedFolder" icon={FolderSharedIcon}></SidebarIcon>
          <SidebarIcon courseId={courseId1} desc="Doc to Canvas File" pageClass={GoogleDocToCanvas} pageRender="GoogleDocToCanvas" icon={ArticleIcon}></SidebarIcon>
          <SidebarIcon courseId={courseId1} desc="Doc to Canvas Page" pageClass={DriveFileToPage} pageRender="DocToPage" icon={MenuBookIcon}></SidebarIcon>
        </List>
      </Collapse>




  
    </div>

  );

}
