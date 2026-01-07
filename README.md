# Job Hunter Assistant

An AI-powered job search assistant with web scraping capabilities, built with Next.js, Django, and CUDA-accelerated processing.

## Project Structure

```
job-hunter-assistant/
├── .github/
│   └── workflows/
│       ├── super-linter.yml    # PR linting workflow
│       ├── scraper.yml         # Scheduled scraper workflow (CRON)
│       └── ci.yml              # PR CI/CD workflow
├── frontend/                   # Next.js TypeScript frontend
│   ├── app/                    # Next.js app directory
│   ├── Dockerfile             # Frontend container
│   └── package.json
├── backend/                    # Django REST API backend
│   ├── config/                # Django configuration
│   ├── api/                   # API application
│   ├── Dockerfile             # Backend container
│   └── requirements.txt
├── scraper/                    # CUDA-accelerated job scraper
│   ├── scraper.py             # Main scraper script
│   ├── Dockerfile             # NVIDIA CUDA container
│   └── requirements.txt
├── docker-compose.yml          # Multi-service orchestration
├── Makefile                   # Development commands
└── .env.example               # Environment variables template
```

## Features

- **Next.js Frontend**: Modern, responsive UI built with TypeScript and Tailwind CSS
- **Django Backend**: RESTful API with PostgreSQL database
- **Job Scraper**: Python script with CUDA GPU acceleration for efficient data processing
- **Docker Compose**: Complete development environment with one command
- **GitHub Actions**: Automated linting, testing, and scheduled scraping
- **Makefile**: Convenient commands for common development tasks

## Prerequisites

- Docker and Docker Compose
- Node.js 20+ (for local frontend development)
- Python 3.11+ (for local backend development)
- NVIDIA GPU with CUDA support (optional, for scraper acceleration)

## Quick Start

1. **Clone the repository**
   ```bash
   git clone https://github.com/EdoAbarca/job-hunter-assistant.git
   cd job-hunter-assistant
   ```

2. **Set up environment variables**
   ```bash
   cp .env.example .env
   # Edit .env with your configuration
   ```

3. **Start all services with Docker Compose**
   ```bash
   make up
   # or
   docker-compose up -d
   ```

4. **Access the services**
   - Frontend: http://localhost:3000
   - Backend API: http://localhost:8000
   - Admin Panel: http://localhost:8000/admin

## Development

### Using Makefile Commands

```bash
make help              # Show all available commands
make build             # Build all Docker containers
make up                # Start all services
make down              # Stop all services
make logs              # View logs from all services
make restart           # Restart all services
make clean             # Remove all containers and volumes
```

### Frontend Development

```bash
cd frontend
npm install
npm run dev           # Start development server
npm run build         # Build for production
npm run lint          # Run linter
npm test             # Run tests
```

### Backend Development

```bash
cd backend
pip install -r requirements.txt
python manage.py migrate              # Run migrations
python manage.py createsuperuser      # Create admin user
python manage.py runserver            # Start development server
python manage.py test                 # Run tests
```

### Scraper

Run the scraper manually:
```bash
make scraper-run
# or
docker-compose run --rm scraper
```

The scraper runs automatically via GitHub Actions on a daily schedule (CRON).

## GitHub Actions Workflows

### Super-Linter (PR)
Automatically lints all code changes in pull requests:
- JavaScript/TypeScript (ESLint)
- Python (Black, Flake8)
- Dockerfile (Hadolint)
- YAML files

### CI (PR)
Runs comprehensive tests on pull requests:
- Frontend: lint, type-check, test, build
- Backend: lint, test
- Docker: build verification for all services

### Scraper (CRON)
Scheduled to run daily at 00:00 UTC:
- Scrapes job postings from configured sources
- Archives results as GitHub Actions artifacts
- Can be triggered manually via workflow dispatch

## Environment Variables

See `.env.example` for all available configuration options.

Key variables:
- `POSTGRES_DB`: Database name
- `POSTGRES_USER`: Database user
- `POSTGRES_PASSWORD`: Database password
- `DJANGO_SECRET_KEY`: Django secret key (change in production!)
- `DEBUG`: Django debug mode (False in production)
- `NEXT_PUBLIC_API_URL`: Backend API URL for frontend

## Testing

Run all tests:
```bash
make test
```

Or individually:
```bash
# Frontend tests
cd frontend && npm test

# Backend tests
cd backend && python manage.py test
```

## License

See [LICENSE](LICENSE) file for details.

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

All PRs will be automatically linted and tested by GitHub Actions.