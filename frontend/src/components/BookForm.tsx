'use client';

import { useState } from 'react';

interface FormData {
  title: string;
  year: string;
  authorId: string;
  newAuthor: string;
}

export default function BookForm() {
  const [formData, setFormData] = useState<FormData>({ title: '', year: '', authorId: '', newAuthor: '' });

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (formData.newAuthor && formData.authorId) {
      alert('You can either select an author or create a new one, not both.');
      return;
    }

    const payload = {
      title: formData.title,
      year: Number(formData.year),
      status: 'DRAFT',
      author_id: formData.authorId ? Number(formData.authorId) : null,
      author_name: formData.newAuthor || null
    };

    await fetch('/api/newbook', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(payload)
    });

    setFormData({ title: '', year: '', authorId: '', newAuthor: '' });
  };

  return (
    <form onSubmit={handleSubmit}>
      <input
        type="text"
        placeholder="Title"
        value={formData.title}
        onChange={(e) => setFormData({ ...formData, title: e.target.value })}
        required
      />
      <input
        type="number"
        placeholder="Year"
        value={formData.year}
        onChange={(e) => setFormData({ ...formData, year: e.target.value })}
        required
      />
      <input
        type="text"
        placeholder="Or add new author"
        value={formData.newAuthor}
        onChange={(e) => setFormData({ ...formData, newAuthor: e.target.value, authorId: '' })}
      />
      <button type="submit">Add Book</button>
    </form>
  );
}
