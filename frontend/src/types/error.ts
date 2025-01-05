// src/types/error.ts
export interface ApiError {
    message: string;
    code?: string;
    details?: Record<string, string[]>;
  }
  