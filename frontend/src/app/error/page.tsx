'use client';


import useAPIError from '../common/hooks/useAPIError'
import { useEffect } from 'react'
import { useRouter } from 'next/navigation';

const ErrorPage: React.FC = () => {
  const router = useRouter();
  const { addError } = useAPIError()

  useEffect(() => {
    const fetchData = async () => {
      try {
        const res = await fetch('http://localhost:8000/apidoesnotexist/');
        if (!res.ok) throw new Error('Failed to fetch authors');

        const data = await res.json();
      } catch (err) {
        addError(`LOAD_DATA_ERROR: ${err}`, (err as Error).message)
      }
    }

    fetchData()
  }, [addError])

  return (<div>            
    <button
      onClick={() => router.push(`/`)}
      className="mt-2 bg-blue-500 text-white px-4 py-2 rounded"
    >
      Go Back
    </button>
</div>)
}

export default ErrorPage;