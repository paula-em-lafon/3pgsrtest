export interface Author {
  id: number;
  author: string;
}

export interface Book {
  id: number;
  title: string;
  year: number;
  status: "DRAFT" | "PUBLISHED";
  author: number;
}

export interface NewBook {
  title: string;
  year: number;
  status: "DRAFT" | "PUBLISHED";
  author_id?: number;
  author_name?: string;
}
