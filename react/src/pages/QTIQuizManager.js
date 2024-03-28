import React, { useState } from 'react';
import Button from '@mui/material/Button';
import FormControl from '@mui/material/FormControl';
import InputLabel from '@mui/material/InputLabel';
import Select from '@mui/material/Select';
import MenuItem from '@mui/material/MenuItem';
import TextField from '@mui/material/TextField';

function QTIQuizManager({ courseId }) {
    const [screenToShow, setScreenToShow] = useState('');
    const [courseOption, setCourseOption] = useState('');
    const [quizType, setQuizType] = useState('');
    const [selectedFile, setSelectedFile] = useState(null);
    const [statusMessage, setStatusMessage] = useState('');

    const handleScreenChange = (screen) => {
        setScreenToShow(screen);
        setStatusMessage(''); // Reset status message when changing screens
    };

    const handleFileChange = (event) => {
        setSelectedFile(event.target.files[0]);
    };

    const handleSubmit = async (event) => {
        event.preventDefault();
        setStatusMessage(`${screenToShow.toUpperCase()} in progress...`);

        let url = '';
        let options = {};

        if (screenToShow === 'import') {
            url = '/importQTIQuiz';
            const formData = new FormData();
            formData.append('file', selectedFile);
            formData.append('courseOption', courseOption);
            formData.append('quizType', quizType);
            formData.append('courseId', courseId.courseId.toString());

            options = {
                method: 'POST',
                body: formData,
            };
        } else if (screenToShow === 'export') {
            url = '/exportQTIQuiz';
            options = {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    courseOption: courseOption,
                    quizType: quizType,
                    courseId: courseId.courseId.toString(),
                }),
            };
        }

        await fetch(url, options)
            .then(response => response.json())
            .then(data => {
                setStatusMessage(data.message);
            })
            .catch(error => {
                console.error('Error:', error);
                setStatusMessage(`Failed to ${screenToShow} quiz.`);
            });

        // Optional: Reset form state here if needed
    };

    return (
        <div align="center">
            {screenToShow === '' && (
                <>
                    <h1>QTI Quiz Manager</h1>
                    <Button variant="contained" color="primary" onClick={() => handleScreenChange('import')}>
                        IMPORT
                    </Button>
                    <Button variant="contained" color="secondary" onClick={() => handleScreenChange('export')} style={{ marginLeft: '10px' }}>
                        EXPORT
                    </Button>
                </>
            )}
            {(screenToShow === 'import' || screenToShow === 'export') && (
                <>
                    <h1>{screenToShow.charAt(0).toUpperCase() + screenToShow.slice(1)} QTI Quiz</h1>
                    <form onSubmit={handleSubmit}>
                        {/* Form Fields */}
                        {/* Status Message */}
                        <p><strong>{statusMessage}</strong></p>
                        {/* Other components based on the previous examples */}
                    </form>
                </>
            )}
        </div>
    );
}

export default QTIQuizManager;
//-----------------------------------------------------------------------------------------------------------------------------