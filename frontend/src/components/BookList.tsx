import React from 'react';
import { useRouter } from 'next/navigation';
import { Book } from '../types';

interface BookListProps {
  books: Book[];
}

const BookList: React.FC<BookListProps> = ({ books }) => {
  const router = useRouter();

  return (
    <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
      {books.map((book) => (
        <div key={book.id} className="p-4 border rounded shadow-md">
          <h2 className="text-2xl font-bold">{book.title}</h2>
          <p className="text-gray-600">Year: {book.year}</p>
          <p className="text-sm">{book.status}</p>
          <button
            onClick={() => router.push(`/edit/${book.id}`)}
            className="mt-2 bg-green-500 text-white px-4 py-2 rounded"
          >
            Edit
          </button>
        </div>
      ))}
    </div>
  );
};

export default BookList;
