'use client'

export default function ArtistSimilarity() {
  const BASE_URL = 'http://127.0.0.1:5000';

  return (
    <div>

      <>
        <h2 className='text-xl text-center text-bold'>Artist Similarity</h2>
        <div className="mt-4 w-full flex justify-center">
          <iframe className="rounded-lg" src={BASE_URL + '/artistsimilarity'} style={{ width: '100%', height: '600px' }} title="Graph" />
        </div>
      </>


    </div>
  );
}

