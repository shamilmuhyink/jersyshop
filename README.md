# E-Commerce Jersey Website

A modern, fully functional e-commerce website for selling sports jerseys online.

## Tech Stack

### Frontend
- Next.js 14 with TypeScript
- Tailwind CSS
- Zustand for state management
- React Hook Form
- Framer Motion

### Backend
- FastAPI
- PostgreSQL
- SQLAlchemy
- Redis for caching
- JWT authentication

## Development Setup

1. Clone the repository
2. Install Docker and Docker Compose
3. Run `docker-compose up`
4. Frontend: http://localhost:3000
5. Backend API: http://localhost:8000

## Features

- Product catalog with filtering and search
- Shopping cart and checkout
- User authentication and accounts
- Admin dashboard
- Seller tools
- Mobile responsive design

## Project Structure

```
jersyshop/
├── frontend/          # Next.js application
├── backend/           # FastAPI application
├── docker-compose.yml # Development environment
└── README.md          # This file
```