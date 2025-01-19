'use client';

import React, { useState } from 'react';
import { useRouter } from 'next/navigation';
import { Author, NewBook } from '../../../types'

interface BookFormProps {
  isEdit: boolean;
  authors: Author[];
  book?: NewBook;
}

const BookForm: React.FC<BookFormProps> = ({ isEdit, authors, book }) => {
  const router = useRouter();
  const [formData, setFormData] = useState<NewBook>({
    title: book?.title || '',
    year: book?.year || 0,
    status: book?.status || 'DRAFT',
    author_id: book?.author_id || undefined,
    author_name: '',
  });

  const handleChange = (e: React.ChangeEvent<HTMLInputElement | HTMLSelectElement>) => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    try {
      const endpoint = isEdit
        ? `http://localhost:8000/api/editbook/${book?.title}/`
        : 'http://localhost:8000/api/newbook';
      const res = await fetch(endpoint, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(formData),
      });
      if (!res.ok) throw new Error('Failed to submit book');
      router.push('/');
    } catch (err) {
      console.error(err);
    }
  };

  return (
    <form onSubmit={handleSubmit} className="max-w-lg mx-auto space-y-4">
      <input name="title" value={formData.title} onChange={handleChange} className="border rounded w-full p-2" placeholder="Title" required />
      <input name="year" type="number" value={formData.year} onChange={handleChange} className="border rounded w-full p-2" placeholder="Year" required />
      <select name="status" value={formData.status} onChange={handleChange} className="border rounded w-full p-2">
        <option value="DRAFT">DRAFT</option>
        <option value="PUBLISHED">PUBLISHED</option>
      </select>
      <button type="submit" className="bg-blue-500 text-white p-2 rounded w-full">
        {isEdit ? 'Update Book' : 'Add Book'}
      </button>
    </form>
  );
};

export default BookForm;
