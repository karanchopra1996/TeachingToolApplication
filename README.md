# Getting Started
TODO: Guide users through getting your code up and running on their own system. In this section you can talk about:
1.	Installation process
    - Clone repository onto your local machine
    - Generate `canvasCredentials.json` from Canvas
    - Store canvas token in .env file in the same folder as the app.py, 
    Format of .env:
    CLIENT_ID= "Cliented ID goes here"
    CANVAS_ACCESS_TOKEN = "Access token goes here"
    #TOKEN or OAUTH
    LOGIN_METHOD = "TOKEN" 
    - Generate `credentials.json` from [Google](https://developers.google.com/workspace/guides/create-credentials)
    - To install and initalize the Front End: 
        - navigate via `cd` into the `/react` directory and enter the command: `npm install` to install all dependencies
        - Before running for the first time, run `pip install -r requirements.txt` in the terminal to install dependencies
    - To install and initalize the Back End: 
        - Install the virtual environment by entering the command: `python -m venv {desired folder name}` or `python3 -m venv {desired folder name}`. 
            - Typically, the desired folder name will be `venv` or some variation on that. 
2.	Software dependencies
    - requirements.txt
3.	Latest releases
4.	API references
    - [In this project most backend calls are to the Canvas API](https://canvas.instructure.com/doc/api/)
    - [Here is a site where you can get comfortable learning about Canvas APIs](https://canvas.instructure.com/doc/api/live)
    - [Some are to the Google Drive API](https://developers.google.com/drive/api/v3/about-sdk)

# Initialization
To initalize the Back End: 
- activate virtual environment by entering the command: `venv/Scripts/activate` on windows, then build and run `python app.py`

To initalize the Front End: 
- In the terminal, `cd react` to change your directory to the React directory
- Initialize by running `npm start'

**_NOTE:_**  Important note for Canvas OAuth2.0 users:
If you plan on using the Canvas OAuth2.0 feature and running the application on your local machine, it's essential to create a localhost that is SSL secured. To do this in React, you can use the following command:
- On Linux and MacOS: `HTTPS=true npm start`
- On Windows: `set HTTPS=true&&npm start`



# Build and Test
-Back End: activate virtual environment by entering the command: `venv/Scripts/activate`, then build and run `app.py`. You may be required to enter `Set-ExecutionPolicy -Scope CurrentUser Unrestricted` if Powershell limits you from running scripts. 
-Front End: cd into react directory, then `npm start`
-Testing: Once both the front end and back end are running, Teaching Tools can be used. Unit Tests can be ran by running: `test.py` or `python -m pytest`


# Contribute
For any given functionality that you want to implement, you need to think about the names first.
- The feature name to be used in the Python side, usually a short 1 to 2 descriptor of the feature
- Endpoint name, so that you can call it from the React frontend, usually a short descriptor of the feature, slightly more descriptive
- The javascript feature name, can be the same name as the python file or similar. 

Each feature needs at a minimum of the following three things:
1. Functions/`feature.py`
    - Your feature should be fully developed in Python, and should be the necessary calls to the Core/ directory to make calls to the APIs
2. `app.py` Function call
    - You function call within the `app.py` file should be something along the lines of the following:
    ```python
    @app.route('/endpointCall', methods=['GET', 'POST'])
    def functionName():
        '''deserialize json into a Json Dictionary'''
        status = Function.feature.functionName(deseralizedJsonObject)
        return status
    ```
3. React version of your feature: `react/src/pages/~~featureName~~.js`
    - With the backend completed, now you need the frontend
    - Below is a simple skeleton with a simple Button to press, but this can be as complex as wanted
    ```javascript
    function featureName(CourseId) {
        
        async function handleButtonPress(e){

            await fetch("http://127.0.0.1:5000/endpointCall", {
                //json object building

            }).then(function (/* returned data*/) {
                // do something here, typically return something
            })
        }
        return <div>
            <div align="center">
                <Button onClick={handleButtonPress}>Any Text You Want to Display</Button>
            </div>
        </div>

    } 
    export default featureName;
    ```   
    - Finally to add your feature to the sidebar of the Dashboard, you need to add it to the `listItems.js` file.
    ```js
    <ListItemButton sx={{ pl: 4 }} onClick={() => {ReactDOM.render(<React.StrictMode><featureName courseId={courseId}/></React.StrictMode>,document.getElementById('page') );
            setPage('endpointCall')  
        }}>
        <ListItemIcon>
            <HorizontalRuleIcon />
        </ListItemIcon>
        <ListItemText primary="Brief Feature Description" />
    </ListItemButton>
    ``` 

TODO: Explain how other users and developers can contribute to make your code better. 

If you want to learn more about creating good readme files then refer the following [guidelines](https://docs.microsoft.com/en-us/azure/devops/repos/git/create-a-readme?view=azure-devops). You can also seek inspiration from the below readme files:
- [ASP.NET Core](https://github.com/aspnet/Home)
- [Visual Studio Code](https://github.com/Microsoft/vscode)
- [Chakra Core](https://github.com/Microsoft/ChakraCore)



# Example Walkthrough: 
## Export Student Groups

![TEACHING-TOOLS sequence](../images/sequence.png)

To give you a sense of how our program works, we will walk you through an example of exporting Student Groups within Canvas.

![TEACHING-TOOLS structure](../images/structure.png)

The Front End of Teaching Tools utilzes React, and within our program is kept in the `react/src` folder. Inside `src/` there is a `pages` directory and four `.js` files. The four `.js` files in the `src/` directory are our Front End, and all the features we've implemented are included in the `pages/` directory. It should probably be renamed `features/` but ***it is called pages because React renders each of those "pages"(`.js` files) into the dashboard when the user selects from the items in the left side pull out menu on the main site***. REWORD THIS SECTION

![TEACHING-TOOLS react](../images/react.png)

`ExportStudents.js` is the "page" for exporting groups. ***In that file, anything below the return statement is displayed on the screen, in this case a button and some text***. REWORD THIS SECTION

![TEACHING-TOOLS function](../images/function.png)

Once the button has been clicked, the `handleSubmit()` function is called. Inside `handleSumbit()`, there is a fetch statement which sends data to the backend. The backend address is what you see there. The `/exportStudentGroups` part is where the fetch will specifically be sent to the backend. It is a `'POST'` (the back end will look for this) and it is posting `'Content-Type':'application/json'` (some json). The body holds the json is which is in the form of `{"course": 123456}` (123456 is just an example of what could be there). From here the json is sent to the backend or `app.py`.

![TEACHING-TOOLS fetch](../images/fetch.png)

Once you are in `app.py`, there will be many `@app.routes()` with functions below them. Look for `@app.route('/exportStudentGroups', ...)`. This is where the front end is specifically sending the json. The logic of this function is as follows: 

>
> If the request that was sent (the fetch) is a 'POST', 
>
> Then go into the `Functions/` directory and into the `exportStudents` file and call the `exportManager()` function.
>

***All the code that is in the `Functions` directory could have technically been in `app.py` but it would have made that file difficult to navigate. We decided to keep most of the backend logic in each file in the Functions directory and call that logic from `app.py`. There is some term for this that we learn in class.*** REWORD THIS SECTION

![TEACHING-TOOLS app](../images/app.png)

Once you've navigated to the `exportManager()` function in the `exportStudents.py` file, let's take a look inside this function. The first two lines get the course ID that was sent from the front end. The third line sends that course ID to the core which is where all the API calls are located. 

Now, navigate to the `core/` directory and to the `canvas_calls.py` file, and look for the `getCoursesName()` function. The first line constructs part of the url where the API call will be sent, then passes that one level deeper to the `http_calls` file to the `httpGet()` function. This function finally sends the API call, which in this case is `request.get(...)`. After this API call, the function returns the data (response) back up to the `getCoursesName()` function in the `canvas_calls.py` file, and then back up to the `exportManager()` function in `exportStudents.py`. ***There are a few other calls to the core in `exportManager(`) but I wont go over those because they are very similar to what I just described.*** REWORD THIS SECTION

![TEACHING-TOOLS core](../images/core.png)

Long story short, that feature creates a `.csv` of all the groups in the course. At the bottom of `exportManager()` there are return statements, one of which will be returned back to `exportStudentGroups()` in `app.py`, which is returned to the front end.

Going back to where we started (`react/pages/ExportStudents.js`) the fetch statement has `.then()` statements which are promises. I would do some research on those, but it is expecting something to be sent back to it.

![TEACHING-TOOLS then](../images/then.png)

All the features I am aware of are done in this way. Things change slightly in the core depending on if the API call is a POST, PUT, or a GET though.


## Add a new Feature and pass it the global course variable
---
`listItems.js` is where this is done, then you can pass your features(pages/(Your_file_name_here.js)) function the `courseId`.

It is done first in the `ListItemButton`. The `courseId` is passed to the component in the `ReactDOM.render()`.

It needs to be done again to update the `courseId` in the `useEffect()`'s switch statement
