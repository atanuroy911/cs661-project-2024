import React, { useState, useEffect } from 'react';
import './SongSelector.css';
import { SONGTABLE } from '@/data/SongDBL';
import axios from 'axios';

const SongSelector = ({ updateLyrics }) => {
  const [selectedAuthor, setSelectedAuthor] = useState('');
  const [selectedSong, setSelectedSong] = useState('');
  const [lyrics, setLyrics] = useState('');

  const handleGenerate = () => {
    const fetchData = async () => {
      try {
        const response = await axios.get(`http://127.0.0.1:5000/lyrics?author=${selectedAuthor}&song=${selectedSong}`);
        setLyrics(response.data);
        // console.log(lyrics?.lyrics);
        
      } catch (error) {
        console.error('Error fetching data:', error);
      }
    };

    fetchData().then(() => {
      if (!lyrics){
        fetchData()
      }
      updateLyrics(lyrics?.lyrics);

    });
  };



  return (
    <div className="form-horizontal songselector">
      <div className="form-group">
        <div className="col-xs-11">
          <select
            className="block w-full py-2 px-4 mb-4 border border-gray-300 rounded-md"
            onChange={(e) => setSelectedAuthor(e.target.value)}
          >
            <option value="">Select Lyricist</option>
            {Object.keys(SONGTABLE).map((author) => (
              <option key={author} value={author}>
                {author}
              </option>
            ))}
          </select>

          {selectedAuthor && (
            <div>
              <select
                className="block w-full py-2 px-4 mb-4 border border-gray-300 rounded-md"
                onChange={(e) => setSelectedSong(e.target.value)}
                disabled={!selectedAuthor}
              >
                <option value="">Select Song</option>
                {selectedAuthor &&
                  SONGTABLE[selectedAuthor].map((song) => (
                    <option key={song} value={song}>
                      {song}
                    </option>
                  ))}
              </select>
              <button
                className="py-2 px-4 bg-blue-500 text-white rounded-md"
                onClick={handleGenerate}
                disabled={!selectedAuthor || !selectedSong}
              >
                Generate
              </button>
            </div>
          )}
          <br />
        </div>
      </div>
    </div>
  );
};

export default SongSelector;
