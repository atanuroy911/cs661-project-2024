'use client'
import React, { useState, useEffect } from 'react';
import axios from 'axios';

const BASE_URL = 'http://127.0.0.1:5000';

const RhymeAnalysis = () => {
  const [selectedTab, setSelectedTab] = useState('entropy');
  const [data, setData] = useState(null);
  const [authorNum, setAuthorNum] = useState('');
  const [selectedAuthor, setSelectedAuthor] = useState('');
  const [numRhymes, setNumRhymes] = useState('');
  const [loading, setLoading] = useState(false);
  const [image, setImage] = useState('');

  useEffect(() => {
    const fetchData = async () => {
      try {
        const response = await axios.get(`${BASE_URL}/data`);
        setData(response.data);
      } catch (error) {
        console.error('Error fetching data:', error);
      }
    };

    fetchData();
  }, []);

  const handleTabChange = (tab) => {
    setSelectedTab(tab);
    setImage('');
  };

  const handleGenerate = async () => {
    try {
      setLoading(true);
      let endpoint = '';
      switch (selectedTab) {
        case 'entropy':
          endpoint = 'rhymepattern';
          break;
        case 'topauthor':
          endpoint = 'topauthor';
          break;
        case 'authorhist':
          endpoint = 'authorhist';
          break;
        default:
          break;
      }

      let url = `${BASE_URL}/${endpoint}`;

      if (selectedTab === 'authorhist') {
        url += `?author=${selectedAuthor}&num_rhymes=${numRhymes}`;
      } else {
        url += `?author_num=${authorNum}`;
      }

      const response = await axios.get(url);
      setImage(url);
    } catch (error) {
      console.error('Error generating image:', error);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="container mx-auto px-4 py-8">
      <h1 className="text-3xl font-bold mb-4">Rhyme Analysis</h1>
      <div className="mb-4">
        <div className="flex">
          <button
            className={`mr-2 py-2 px-4 ${selectedTab === 'entropy' ? 'bg-blue-500 text-white' : 'bg-gray-200 text-gray-700'
              }`}
            onClick={() => handleTabChange('entropy')}
          >
            Entropy Schemes
          </button>
          <button
            className={`mr-2 py-2 px-4 ${selectedTab === 'topauthor' ? 'bg-blue-500 text-white' : 'bg-gray-200 text-gray-700'
              }`}
            onClick={() => handleTabChange('topauthor')}
          >
            Top Author Rhymes
          </button>
          <button
            className={`mr-2 py-2 px-4 ${selectedTab === 'authorhist' ? 'bg-blue-500 text-white' : 'bg-gray-200 text-gray-700'
              }`}
            onClick={() => handleTabChange('authorhist')}
          >
            Author Histogram
          </button>
        </div>
      </div>

      {selectedTab === 'entropy' && (
        <div>
          <div className="mt-4 flex items-center space-x-2">
            <label htmlFor="authorNumInput">Number of Authors:</label>
            <input
              id="authorNumInput"
              type="number"
              value={authorNum}
              onChange={(e) => setAuthorNum(e.target.value)}
              className="border border-gray-400 px-2 py-1 rounded"
            />
            <button onClick={handleGenerate} className="px-4 py-1 bg-blue-500 text-white rounded hover:bg-blue-600">Generate</button>
          </div>
        </div>
      )}

      {selectedTab === 'topauthor' && (
        <div className='flex justify-center content-center w-full'>
          {/* Placeholder for Top Author Rhymes */}
          <p>Top Author Rhymes section</p>
          <br />
          <button onClick={handleGenerate} className="ml-3 px-4 py-1 bg-blue-500 text-white rounded hover:bg-blue-600">Show</button>
        </div>
      )}

      {selectedTab === 'authorhist' && (
        <div>
          <div className="mt-4 flex items-center space-x-2">
            <label htmlFor="authorSelect">Select Author:</label>
            <select
              id="authorSelect"
              value={selectedAuthor}
              onChange={(e) => setSelectedAuthor(e.target.value)}
              className="border border-gray-400 px-2 py-1 rounded"
            >
              <option value="">Select an author</option>
              {data &&
                Object.keys(data).map((author) => (
                  <option key={author} value={author}>
                    {author}
                  </option>
                ))}
            </select>
            <label htmlFor="numRhymesInput">Number of Rhymes:</label>
            <input
              id="numRhymesInput"
              type="number"
              value={numRhymes}
              onChange={(e) => setNumRhymes(e.target.value)}
              className="border border-gray-400 px-2 py-1 rounded"
            />
            <button onClick={handleGenerate} className="px-4 py-1 bg-blue-500 text-white rounded hover:bg-blue-600">Generate</button>
          </div>
        </div>
      )}

      {loading ? (
        <div role="status" className='mx-auto flex justify-center w-full'>
          <svg
            aria-hidden="true"
            className="w-8 h-8 text-gray-200 animate-spin dark:text-gray-600 fill-blue-600"
            viewBox="0 0 100 101"
            fill="none"
            xmlns="http://www.w3.org/2000/svg"
          >
            <path
              d="M100 50.5908C100 78.2051 77.6142 100.591 50 100.591C22.3858 100.591 0 78.2051 0 50.5908C0 22.9766 22.3858 0.59082 50 0.59082C77.6142 0.59082 100 22.9766 100 50.5908ZM9.08144 50.5908C9.08144 73.1895 27.4013 91.5094 50 91.5094C72.5987 91.5094 90.9186 73.1895 90.9186 50.5908C90.9186 27.9921 72.5987 9.67226 50 9.67226C27.4013 9.67226 9.08144 27.9921 9.08144 50.5908Z"
              fill="currentColor"
            />
            <path
              d="M93.9676 39.0409C96.393 38.4038 97.8624 35.9116 97.0079 33.5539C95.2932 28.8227 92.871 24.3692 89.8167 20.348C85.8452 15.1192 80.8826 10.7238 75.2124 7.41289C69.5422 4.10194 63.2754 1.94025 56.7698 1.05124C51.7666 0.367541 46.6976 0.446843 41.7345 1.27873C39.2613 1.69328 37.813 4.19778 38.4501 6.62326C39.0873 9.04874 41.5694 10.4717 44.0505 10.1071C47.8511 9.54855 51.7191 9.52689 55.5402 10.0491C60.8642 10.7766 65.9928 12.5457 70.6331 15.2552C75.2735 17.9648 79.3347 21.5619 82.5849 25.841C84.9175 28.9121 86.7997 32.2913 88.1811 35.8758C89.083 38.2158 91.5421 39.6781 93.9676 39.0409Z"
              fill="currentFill"
            />
          </svg>
          <span className="sr-only">Loading...</span>
        </div>
      ) : (
        image && (
          <div className="mx-auto flex justify-center w-full">
            <img src={image} alt="Rhyme Pattern" className="mt-4 mx-auto" />
          </div>
        )
      )}
    </div>
  );
};

export default RhymeAnalysis;

