'use client';

import React, { useState, useEffect } from 'react';
import BookList from '../components/BookList';
import { Book, Author } from '../types';

const HomePage: React.FC = () => {
  const [books, setBooks] = useState<Book[]>([]);
  const [authors, setAuthors] = useState<Author[]>([]);
  const [selectedAuthor, setSelectedAuthor] = useState<number | null>(null);

  useEffect(() => {
    const fetchData = async () => {
      const res = await fetch('http://localhost:8000/api/');
      const data = await res.json();
      setBooks(data.books);
      setAuthors(data.authors);
    };

    fetchData();
  }, []);

  const filteredBooks = selectedAuthor
    ? books.filter((book) => book.author === selectedAuthor)
    : books;

  return (
    <div className="container mx-auto p-6">
      <h1 className="text-4xl font-bold text-center mb-6">Yes Sir I Can Boogie</h1>

      <div className="mb-4">
        <select
          onChange={(e) => setSelectedAuthor(Number(e.target.value) || null)}
          className="w-full p-2 border rounded"
        >
          <option value="">All Authors</option>
          {authors.map((author) => (
            <option key={author.id} value={author.id}>
              {author.author}
            </option>
          ))}
        </select>
      </div>

      <BookList books={filteredBooks} />
    </div>
  );
};

export default HomePage;
