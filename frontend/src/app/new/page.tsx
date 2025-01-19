// src/app/create/page.tsx
import BookForm from '../../components/BookForm';

export default function CreatePage() {
  return (
    <div>
      <BookForm isEdit={false} />
    </div>
  );
}
