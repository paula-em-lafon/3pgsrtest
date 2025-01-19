'use client';

import React, { useState } from 'react';
import { useRouter } from 'next/navigation';
import { Author, Book, NewBook } from '../types';

interface BookFormProps {
  isEdit: boolean;
  book?: Book;
  authors: Author[];
}

const BookForm: React.FC<BookFormProps> = ({ isEdit, book, authors }) => {
  const router = useRouter();
  const [formData, setFormData] = useState<NewBook>({
    title: book?.title || '',
    year: book?.year || 0,
    status: book?.status || 'DRAFT',
    author_id: book?.author || undefined,
    author_name: '',
  });

  const handleChange = (
    e: React.ChangeEvent<HTMLInputElement | HTMLSelectElement>
  ) => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    try {
      const endpoint = isEdit
        ? `http://localhost:8000/api/editbook/${book?.id}/`
        : 'http://localhost:8000/api/newbook';

      const res = await fetch(endpoint, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(formData),
      });

      if (!res.ok) throw new Error('Failed to submit book');

      router.push('/');
    } catch (err) {
      console.error('Error submitting book:', err);
    }
  };

  return (
    <form onSubmit={handleSubmit} className="max-w-lg mx-auto space-y-4">
      <input
        name="title"
        placeholder="Title"
        value={formData.title}
        onChange={handleChange}
        required
        className="border border-gray-300 rounded w-full p-2"
      />
      <input
        name="year"
        placeholder="Year"
        type="number"
        value={formData.year}
        onChange={handleChange}
        required
        className="border border-gray-300 rounded w-full p-2"
      />
      <select
        name="status"
        value={formData.status}
        onChange={handleChange}
        className="border border-gray-300 rounded w-full p-2"
      >
        <option value="DRAFT">DRAFT</option>
        <option value="PUBLISHED">PUBLISHED</option>
      </select>
      <select
        name="author_id"
        value={formData.author_id || ''}
        onChange={(e) =>
          setFormData({ ...formData, author_id: parseInt(e.target.value), author_name: '' })
        }
        className="border border-gray-300 rounded w-full p-2"
      >
        <option value="">Select Author</option>
        {authors.map((author) => (
          <option key={author.id} value={author.id}>
            {author.author}
          </option>
        ))}
      </select>
      <input
        name="author_name"
        placeholder="New Author"
        value={formData.author_name || ''}
        onChange={(e) =>
          setFormData({ ...formData, author_name: e.target.value, author_id: undefined })
        }
        className="border border-gray-300 rounded w-full p-2"
      />
      <button type="submit" className="bg-blue-500 text-white rounded w-full p-2">
        {isEdit ? 'Update Book' : 'Add Book'}
      </button>
    </form>
  );
};

export default BookForm;
