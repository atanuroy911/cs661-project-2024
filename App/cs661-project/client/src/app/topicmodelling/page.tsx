'use client'
import { useState, useEffect } from 'react';

export default function TopicModelling() {
  const [folders, setFolders] = useState([]);
  const [selectedFolder, setSelectedFolder] = useState('');
  const [files, setFiles] = useState([]);
  const [selectedFile, setSelectedFile] = useState('');

  useEffect(() => {
    const fetchFolders = async () => {
      try {
        const response = await fetch('http://127.0.0.1:5000/folders');
        const data = await response.json();
        setFolders(data);
      } catch (error) {
        console.error('Error fetching folders:', error);
      }
    };

    fetchFolders();
  }, []);

  const handleFolderSelect = async (folderName) => {
    setSelectedFolder(folderName);
    try {
      const response = await fetch(`http://127.0.0.1:5000/files/${folderName}`);
      const data = await response.json();
      setFiles(data);
    } catch (error) {
      console.error('Error fetching files:', error);
    }
  };

  const handleFileSelect = (fileName) => {
    setSelectedFile(fileName);
  };

  const fileUrl = selectedFile ? `http://127.0.0.1:5000/files/${selectedFolder}/${selectedFile}` : '';

  return (
    <div>
      <div className="flex">
        <div className="mr-4">
          <label htmlFor="folderSelect">Select Folder:</label>
          <select
            id="folderSelect"
            onChange={(e) => handleFolderSelect(e.target.value)}
            value={selectedFolder}
          >
            <option value="">Select Folder</option>
            {folders.map((folder, index) => (
              <option key={index} value={folder}>
                {folder}
              </option>
            ))}
          </select>
        </div>
        <div>
          <label htmlFor="fileSelect">Select File:</label>
          <select
            id="fileSelect"
            onChange={(e) => handleFileSelect(e.target.value)}
            value={selectedFile}
          >
            <option value="">Select File</option>
            {files.map((file, index) => (
              <option key={index} value={file}>
                {file}
              </option>
            ))}
          </select>
        </div>
      </div>
      {selectedFile && (
        <>
          <h2 className='text-xl text-center text-bold'>Preview</h2>
          <div className="mt-4 w-full flex justify-center">
            <iframe src={fileUrl} style={{ width: '100%', height: '600px' }} title="File Preview" />
          </div>
        </>

      )}
    </div>
  );
}

