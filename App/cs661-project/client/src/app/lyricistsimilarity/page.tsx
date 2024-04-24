'use client'

export default function ArtistSimilarity() {
  const BASE_URL = 'http://127.0.0.1:5000';

  return (
    <div>

      <>
        <h2 className='text-3xl font-bold mb-4 text-center'>Lyricist Similarity</h2>
        <hr />
        <div className="mt-4 w-full flex justify-center">
          <iframe className="rounded-lg" src={BASE_URL + '/artistsimilarity'} style={{ width: '100%', height: '600px' }} title="Graph" />
        </div>
      </>


    </div>
  );
}

