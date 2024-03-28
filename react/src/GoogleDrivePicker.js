import Button from '@mui/material/Button';
import React, { useState, useEffect } from "react";
import useDrivePicker from 'react-google-drive-picker';

var driveSupportedFileTypes = "application/vnd.google-apps.audio,application/vnd.google-apps.document,application/vnd.google-apps.drive-sdk,application/vnd.google-apps.drawing,application/vnd.google-apps.file,application/vnd.google-apps.folder,application/vnd.google-apps.form,application/vnd.google-apps.fusiontable,application/vnd.google-apps.jam,application/vnd.google-apps.map,application/vnd.google-apps.photo,application/vnd.google-apps.presentation,application/vnd.google-apps.script,application/vnd.google-apps.shortcut,application/vnd.google-apps.site,application/vnd.google-apps.spreadsheet,application/vnd.google-apps.unknown,application/vnd.google-apps.video,text/html,application/zip,text/plain,application/rtf,application/vnd.oasis.opendocument.text,application/pdf,application/vnd.openxmlformats-officedocument.wordprocessingml.document,application/epub+zip,application/vnd.openxmlformats-officedocument.spreadsheetml.sheet,application/x-vnd.oasis.opendocument.spreadsheet,application/pdf,text/csv,text/tab-separated-values,application/zip,image/jpeg,image/png,image/svg+xml,application/pdf,application/vnd.openxmlformats-officedocument.presentationml.presentation,application/vnd.oasis.opendocument.presentation,application/pdf,text/plain,application/vnd.google-apps.script+json"

const clientID = "662092689412-nj10beqpqi1fnq4oishulajthdvf38io.apps.googleusercontent.com";
const developerKey = "AIzaSyBhCsjG2zP2t4frwk6U1yZGnpdN8Ti41E8";


function GoogleDrivePicker({ style, multiselect, response, filetype }) {
    // https://github.com/Jose-cd/React-google-drive-picker
    const [selectedGoogleFile, setSelectedGoogleFile] = useState({});
    const [openPicker, authResponse] = useDrivePicker();
    // const customViewsArray = [new google.picker.DocsView()]; // custom view
    const handleOpenPicker = (e) => {
        setSelectedGoogleFile({});
        openPicker({
            clientId: clientID,
            developerKey: developerKey,
            // token: token, // pass oauth token in case you already have one
            showUploadView: true,
            showUploadFolders: true,
            viewMimeTypes: filetype == null ? driveSupportedFileTypes : filetype,
            supportDrives: true,
            setIncludeFolders: true,
            multiselect: multiselect,
            setSelectFolderEnabled: true,

            callbackFunction: (data) => {
                if (data.action === 'cancel') {
                    console.log('User clicked cancel/close button')
                } else {
                    console.log(data)
                    setSelectedGoogleFile(data)
                }
            },
        });
    }

    useEffect(() => {
        response(selectedGoogleFile)
    });

    return (
        <Button onClick={() => handleOpenPicker()} style={style} type="submit" variant="contained" > Open Google Drive</Button >
    )
}
export default GoogleDrivePicker