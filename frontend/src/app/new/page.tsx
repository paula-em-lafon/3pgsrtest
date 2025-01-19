'use client';

import React, { useState, useEffect } from 'react';
import { useRouter } from 'next/navigation';
import BookForm from '../../components/BookForm';
import { Author } from '../../types';

const NewBookPage: React.FC = () => {
  const router = useRouter();
  const [authors, setAuthors] = useState<Author[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const fetchAuthors = async () => {
      try {
        const res = await fetch('http://localhost:8000/api/');
        if (!res.ok) throw new Error('Failed to fetch authors');

        const data = await res.json();
        setAuthors(data.authors);
      } catch (err) {
        setError((err as Error).message);
      } finally {
        setLoading(false);
      }
    };

    fetchAuthors();
  }, []);

  if (loading) return <p className="text-gray-500 text-center">Loading...</p>;
  if (error) return <p className="text-red-500 text-center">Error: {error}</p>;

  return (
    <div className="p-6">
      <h1 className="text-3xl font-bold mb-6 text-center">Add New Book</h1>
      <BookForm isEdit={false} authors={authors} />
    </div>
  );
};

export default NewBookPage;
