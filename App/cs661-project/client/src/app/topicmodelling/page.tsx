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
      <h1 className="text-3xl font-bold mb-4">Rhyme Analysis</h1>
      <div className="flex">
        <div className="mr-4">
          <label htmlFor="folderSelect">Select Author:</label>
          <select
            id="folderSelect"
            onChange={(e) => handleFolderSelect(e.target.value)}
            value={selectedFolder}
            className='block w-full py-2 px-4 mb-4 border border-gray-300 rounded-md'
          >
            <option value="">Select Representation</option>
            {folders.map((folder, index) => (
              <option key={index} value={folder}>
                {folder}
              </option>
            ))}
          </select>
        </div>
        <div>
          <label htmlFor="fileSelect">Select Representation:</label>
          <select
            id="fileSelect"
            onChange={(e) => handleFileSelect(e.target.value)}
            value={selectedFile}
            className='block w-full py-2 px-4 mb-4 border border-gray-300 rounded-md'
          >
            <option value="">Select Representation</option>
            {files.map((file, index) => {
              let displayName = file;
              if (file.includes('TOPICS')) {
                displayName = 'Visualize Topic';
              } else if (file.includes('DOC')) {
                displayName = 'Visualize Document';
              }
              else if (file.includes('MAP')){
                displayName = '2-D Doc Map';
              }
              else if (file.includes('BC')){
                displayName = 'Bar Chart for Topic Words';
              }
              return (
                <option key={index} value={file}>
                  {displayName}
                </option>
              );
            })}
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

