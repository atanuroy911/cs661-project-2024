// 'use client'
// import React, { useState } from 'react';

// export default function ArtistSimilarity() {
//   const BASE_URL = 'http://127.0.0.1:5000';
//   const [activeTab, setActiveTab] = useState('artistsimilarity1');

//   const handleTabChange = (tab) => {
//     setActiveTab(tab);
//   };

//   return (
//     <div>
//       <h2 className='text-3xl font-bold mb-4 text-center'>Lyricist Similarity</h2>
//       <hr />
//       <div className="mt-4 w-full">
//         <div className="flex justify-center space-x-4">
//           <button className={`tab-btn ${activeTab === 'artistsimilarity1' ? 'bg-blue-500 text-white' : 'bg-gray-200 text-gray-800'} px-4 py-2 rounded-lg`} onClick={() => handleTabChange('artistsimilarity1')}>k=1</button>
//           <button className={`tab-btn ${activeTab === 'artistsimilarity3' ? 'bg-blue-500 text-white' : 'bg-gray-200 text-gray-800'} px-4 py-2 rounded-lg`} onClick={() => handleTabChange('artistsimilarity3')}>k=3</button>
//           <button className={`tab-btn ${activeTab === 'artistsimilarity5' ? 'bg-blue-500 text-white' : 'bg-gray-200 text-gray-800'} px-4 py-2 rounded-lg`} onClick={() => handleTabChange('artistsimilarity5')}>k=5</button>
//           <button className={`tab-btn ${activeTab === 'artistsimilarity7' ? 'bg-blue-500 text-white' : 'bg-gray-200 text-gray-800'} px-4 py-2 rounded-lg`} onClick={() => handleTabChange('artistsimilarity7')}>k=7</button>
//           <button className={`tab-btn ${activeTab === 'artistsimilarity9' ? 'bg-blue-500 text-white' : 'bg-gray-200 text-gray-800'} px-4 py-2 rounded-lg`} onClick={() => handleTabChange('artistsimilarity9')}>k=9</button>
//         </div>
//         <div className="mt-4 w-full flex justify-center">
//           <iframe className="rounded-lg" src={`${BASE_URL}/${activeTab}`} style={{ width: '100%', height: '600px' }} title="Graph" />
//         </div>
//       </div>
//     </div>
//   );
// }


export default function Page() {
  return (
      <>
      <h1 className="text-3xl font-bold text-center">Lyricist Similarity</h1>
          <iframe src="http://127.0.0.1:5000/networkx" style={{ width: '100%', height: '800px' }} title="Topic Modelling"></iframe>

      </>
  );
}