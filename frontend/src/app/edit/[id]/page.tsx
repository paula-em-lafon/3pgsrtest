'use client';

import React, { useEffect, useState } from 'react';
import { useParams } from 'next/navigation';
import BookForm from '../../../components/BookForm';
import { Book, Author } from '../../../types';

const EditPage: React.FC = () => {
  const params = useParams(); // Use Next.js hook to retrieve params
  const id = params?.id; // Extract id safely

  const [book, setBook] = useState<Book | null>(null);
  const [authors, setAuthors] = useState<Author[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    if (!id) return;

    const fetchBookAndAuthors = async () => {
      try {
        const res = await fetch('http://localhost:8000/apis/');
        if (!res.ok) throw new Error('Failed to fetch data');

        const data = await res.json();
        const foundBook = data.books.find((b: Book) => b.id.toString() === id);

        if (!foundBook) throw new Error('Book not found');
        setBook(foundBook);
        setAuthors(data.authors);
      } catch (err) {
        setError((err as Error).message);
      } finally {
        setLoading(false);
      }
    };

    fetchBookAndAuthors();
  }, [id]);

  if (loading) return <p className="text-gray-500 text-center">Loading...</p>;
  if (error) return <p className="text-red-500 text-center">Error: {error}</p>;
  if (!book) return <p className="text-red-500 text-center">Book not found</p>;

  return (
    <div className="p-6">
      <h1 className="text-3xl font-bold mb-6 text-center">Edit Book</h1>
      <BookForm isEdit={true} book={book} authors={authors} />
    </div>
  );
};

export default EditPage;
