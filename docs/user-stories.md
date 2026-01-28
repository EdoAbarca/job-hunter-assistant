# User Stories

## Vision

A single-user app that reduces time spent applying by letting the user ingest job descriptions (manually, JSON, or scraper artifacts), store and track positions, upload a master CV, and generate tailored CV variants and cover letters by triggering API-based LLM calls. Manual intake is primary.

---

## Persona

**Eduardo** — Single user building/using the tool to speed job hunting.

---

## User Stories

### US-0 (P0) — Project Initialization & Infrastructure Setup

**As** a developer  
**I want** to set up the complete project infrastructure with all required dependencies and services  
**So that** I can start building features on a solid foundation with proper CI/CD pipelines

**User Story**
As a developer, I need to initialize the entire project structure including frontend (React + Vite), backend (Django + DRF), databases (MongoDB, Redis), containerization (Docker), and CI/CD pipelines (GitHub Actions) so that the development environment is consistent, reproducible, and ready for feature development.

**Acceptance Criteria**
- Frontend app (React 18+ with Vite) initialized with proper folder structure (`src/`, `public/`, `tests/`)
- Frontend dependencies installed: Tailwind CSS 3+, Toastify.js, Iconify React, Yup, React Router
- Backend app (Django 4+ with DRF) initialized with proper project structure (`apps/`, `config/`, `tests/`)
- Backend dependencies installed: djangorestframework, pymongo, redis, celery, pyjwt, pyyaml, python-docx, PyPDF2
- MongoDB 6+ and Redis 7+ configured in docker-compose.yml with persistent volumes
- Dockerfiles created for both frontend (multi-stage build with nginx) and backend (Python 3.11+)
- GitHub Actions workflows for CI with test and lint jobs, dependency caching enabled
- Makefile with common commands: build, up, down, restart, test, lint, clean, logs, migrate, seed
- All services can start with `docker-compose up` and communicate properly via internal network
- CI pipeline runs tests and linting on pull requests and merge to main
- Health check endpoints implemented for backend (`/api/health/`) and frontend serves correctly

**Definition of Done**
- Frontend app scaffolded with Vite + React 18 + Tailwind CSS 3
- Backend app scaffolded with Django 4 + DRF with project name `jobhunter`
- `Dockerfile.frontend` with multi-stage build (build stage + nginx stage)
- `Dockerfile.backend` with Python 3.11+ and all dependencies
- `docker-compose.yml` with services: frontend (port 3000), backend (port 8000), mongodb (port 27017), redis (port 6379)
- MongoDB configured with authentication and persistent volume
- Redis configured with persistent volume
- `.github/workflows/ci.yml` with jobs: test-frontend, test-backend, lint-frontend, lint-backend
- `.github/workflows/super-linter.yml` configured with appropriate linters
- `Makefile` with all specified targets and documentation comments
- `.dockerignore` files for both frontend and backend
- `.env.example` files for both frontend and backend with all required variables
- `.gitignore` configured for Python, Node.js, and IDE files
- `README.md` updated with: project description, prerequisites, setup instructions, running instructions, testing instructions, tech stack list
- All containers start successfully without errors
- Backend accessible at `http://localhost:8000/api/health/` returns 200 OK
- Frontend accessible at `http://localhost:3000` renders welcome page
- MongoDB connection verified via backend health check
- Redis connection verified via backend health check

---

### US-1 (P0) — Manual Job Paste

**As** Eduardo  
**I want** a simple form to paste a full job description and save the job  
**So that** I can generate tailored documents and track it later

**User Story**
As Eduardo, I need to manually add a job position by pasting the complete job description into a form, so that the system can parse it, extract requirements, and allow me to generate tailored application materials.

**Acceptance Criteria**
- Form has required fields: title (max 200 chars), company (max 100 chars), raw_description (min 50 chars, max 50000 chars)
- Form has optional fields: url (valid URL format), location (max 200 chars), posted_at (date picker or ISO date string)
- All fields have proper validation with clear error messages displayed inline
- Raw description textarea supports multi-line text with at least 10 rows visible
- Submit button is disabled while form is invalid or submission is in progress
- After successful submit, job appears at top of job list (newest→oldest sort)
- Newly created job automatically has an associated Application with status `NOT_APPLIED`
- Success notification displayed: "Job position added successfully"
- Form is cleared after successful submission
- On error, user-friendly error message displayed with details from backend

**Definition of Done**
- Backend: `POST /api/jobs/manual` endpoint implemented with proper validation
- Backend: Job model created in MongoDB with schema: id, title, company, location, url, raw_description, posted_at, source (default: "MANUAL"), created_at, updated_at
- Backend: Application model auto-created with job_id foreign key and status `NOT_APPLIED`
- Backend: Endpoint returns 201 Created with job + application data
- Backend: Endpoint returns 400 Bad Request with validation errors
- Frontend: Form component created with Yup validation schema
- Frontend: Form integrates with Toastify for success/error notifications
- Frontend: Job list component refreshes after new job added
- Tests: Unit tests for job creation endpoint (happy path + validation errors)
- Tests: Integration test for job + application creation
- Tests: Frontend component tests for form validation

---

### US-2 (P0) — Upload Master CV

**As** Eduardo  
**I want** to upload a master CV (YAML/JSON/Markdown or PDF/DOCX)  
**So that** it becomes the single source for CV generation

**User Story**
As Eduardo, I need to upload my master CV in various formats (structured: YAML/JSON/Markdown or binary: PDF/DOCX) so that the system can use it as the source of truth for generating tailored CV variants for different job positions.

**Acceptance Criteria**
- Upload interface supports drag-and-drop and file selection
- Accepted formats: .yaml, .yml, .json, .md, .pdf, .docx (max file size: 10MB)
- File format validated before upload with clear error message for unsupported formats
- For structured formats (YAML/JSON/Markdown): system parses and extracts sections (personal_info, experience, education, skills, projects, certifications)
- For binary formats (PDF/DOCX): file stored as-is with metadata noting it requires manual parsing
- Upload shows progress indicator for files > 1MB
- Only one active master CV at a time; uploading new CV prompts user to confirm replacement
- Master CV details displayed: filename, upload date, format type, parse status (parsed/raw), file size
- Parse errors shown to user with option to re-upload or continue with raw storage
- Success notification: "Master CV uploaded and parsed successfully" or "Master CV uploaded (raw format)"
- Ability to download currently uploaded master CV
- Ability to delete master CV with confirmation prompt

**Definition of Done**
- Backend: `POST /api/master-cv/upload` endpoint with file upload handling
- Backend: `GET /api/master-cv/` endpoint returns current master CV metadata
- Backend: `GET /api/master-cv/download` endpoint serves file
- Backend: `DELETE /api/master-cv/` endpoint removes current CV
- Backend: MasterCV model with fields: id, filename, file_path, format (enum: YAML/JSON/MARKDOWN/PDF/DOCX), upload_date, parsed_content (JSON), parse_status (enum: PARSED/RAW/ERROR), file_size, is_active
- Backend: Parser service for YAML/JSON/Markdown formats with structured extraction
- Backend: File storage in `/media/master_cvs/` with unique filenames
- Backend: Celery task for async parsing of uploaded CV
- Frontend: Upload component with drag-and-drop using React hooks
- Frontend: File validation before upload
- Frontend: Progress bar for upload
- Frontend: Display current master CV with metadata
- Frontend: Download and delete buttons with proper confirmation
- Tests: Unit tests for parsers (each format + edge cases)
- Tests: Integration test for upload → parse → store flow
- Tests: File validation tests (size limits, format checks)
- Tests: Frontend component tests for upload interactions

---

### US-3 (P0) — Auto-extract Job Requirements

**As** Eduardo  
**I want** the system to automatically extract skills and requirements from the job description using LLM  
**So that** the tailored CV/cover letter can focus on the right skills

**User Story**
As Eduardo, after I add a job position, I need the system to automatically extract key requirements, tech stack, and a concise summary from the raw job description using an LLM API, so that I can quickly understand what skills to emphasize in my application materials.

**Acceptance Criteria**
- Extraction triggered automatically as a background job after job creation (within 30 seconds)
- Job detail view shows extraction status: PENDING, PROCESSING, COMPLETED, FAILED
- For COMPLETED status: displays `requirements_summary` (2-4 sentences) and `normalized_stack` (array of tech tags)
- Tech tags extracted include: programming languages, frameworks, tools, methodologies (max 20 tags)
- Extraction metadata displayed: model_used, tokens_used, timestamp, processing_time
- For FAILED status: displays error message with option to retry extraction
- Manual retry button available if extraction fails
- Extraction uses configured LLM provider (Google AI Studio or Hugging Face by default)
- Loading indicator shown while extraction is in progress
- Toast notification when extraction completes or fails
- Extracted data persists even if job is edited later (can re-extract manually)

**Definition of Done**
- Backend: LLM service abstraction layer with provider interface (supports Google AI Studio, Hugging Face, OpenAI, DeepSeek)
- Backend: Configuration system for LLM provider selection and API keys
- Backend: `POST /api/jobs/{id}/extract-requirements` endpoint for manual trigger
- Backend: Celery task `extract_job_requirements` that calls LLM and updates job
- Backend: Job model extended with: requirements_summary, normalized_stack (array), extraction_status, extraction_metadata (JSON: model_used, tokens_used, timestamp, error_message)
- Backend: LLM prompt template for requirements extraction with structured output format
- Backend: Retry logic with exponential backoff for LLM API failures
- Backend: Logging of all LLM calls with request/response/errors
- Frontend: Extraction status indicator in job detail view
- Frontend: Display of requirements summary and tech tags as badges
- Frontend: Retry button for failed extractions
- Frontend: Real-time status updates using polling or WebSocket
- Tests: Unit tests for LLM service with mocked API responses
- Tests: Integration test for extraction flow (job creation → extraction → storage)
- Tests: Test with various job description formats and edge cases
- Tests: Error handling tests for API failures, timeouts, rate limits

---

### US-4 (P0) — Generate Tailored CV Variant

**As** Eduardo  
**I want** to generate a tailored CV for a given job using my master CV  
**So that** the CV emphasizes relevant skills and bullets for that job

**User Story**
As Eduardo, I need to generate a tailored CV variant that emphasizes the most relevant experiences and skills from my master CV based on a specific job's requirements, so that I can submit a customized application that maximizes my chances of getting an interview.

**Acceptance Criteria**
- "Generate Tailored CV" button available on Application detail page (only if master CV exists)
- Generation triggered as background job with status indicator: PENDING, PROCESSING, COMPLETED, FAILED
- Generated CV highlights skills matching extracted job requirements
- CV uses professional formatting (consider RenderCV for PDF generation)
- Generated document attached to Application with metadata: filename, file_path, format (PDF), created_at, model_used, tokens_used, cost_estimate
- Document appears in Application's document list with download button
- Preview available before final download (if PDF)
- Generation takes less than 30 seconds for typical CV
- Error handling: if generation fails, clear error message shown with retry option
- Notification shown when generation completes: "Tailored CV generated successfully"
- Multiple versions can be generated for same application (versioning)
- Document list shows: version number, creation date, model used, download link
- Cost tracking: tokens and estimated cost displayed per document

**Definition of Done**
- Backend: `POST /api/applications/{id}/generate-cv` endpoint
- Backend: Celery task `generate_tailored_cv` that:
  - Loads master CV parsed content
  - Loads job requirements and normalized stack
  - Calls LLM to select/rewrite relevant CV sections
  - Uses RenderCV or similar to generate PDF
  - Stores document with metadata
- Backend: Document model with fields: id, application_id, type (enum: CV/COVER_LETTER), filename, file_path, format, model_used, tokens_used, cost_estimate, version_number, created_at, metadata (JSON)
- Backend: Document storage in `/media/documents/{application_id}/`
- Backend: `GET /api/documents/{id}/download` endpoint for file download
- Backend: `GET /api/applications/{id}/documents` endpoint for listing documents
- Backend: LLM prompt template for CV tailoring with instructions to maintain factual accuracy
- Backend: Post-processing validation to ensure no hallucinated content
- Frontend: "Generate Tailored CV" button with loading state
- Frontend: Document list component showing all generated documents
- Frontend: Download button for each document
- Frontend: Status indicator for generation progress
- Frontend: Cost display per document (tokens + estimated cost)
- Frontend: Version history view
- Tests: Unit tests for CV generation logic
- Tests: Integration test for full generation flow
- Tests: Test with different master CV formats
- Tests: Validation test to ensure no fabricated information
- Tests: E2E test covering: job creation → CV upload → extraction → CV generation → download

---

### US-5 (P0) — Generate Tailored Cover Letter

**As** Eduardo  
**I want** to create a concise tailored cover letter for a job  
**So that** I can use it as the first draft in my applications

**User Story**
As Eduardo, I need to generate a professional cover letter tailored to a specific job that highlights 2-3 key matches between my experience and the job requirements, so that I can submit a compelling application that demonstrates my fit for the role.

**Acceptance Criteria**
- "Generate Cover Letter" button available on Application detail page (only if master CV exists)
- Generation triggered as background job with status indicator
- Output format: 3-4 short paragraphs (250-400 words total)
- Content requirements:
  - Paragraph 1: Opening with job title and company name, brief statement of interest
  - Paragraph 2-3: 2-3 specific matches between candidate's experience and job requirements (drawn from master CV and job description)
  - Paragraph 4: Closing with call to action and contact information
- Language constraints: professional tone, no fabricated facts, all experiences must be from master CV
- Optional fields in generation form: recruiter name, specific requirements to emphasize
- Generated document stored as .txt or .pdf with metadata
- Preview modal shows generated content before finalizing
- Edit capability: allow minor edits before saving final version
- Document attached to Application with same metadata structure as CV
- Multiple versions can be generated (versioning)
- Notification: "Cover letter generated successfully"

**Definition of Done**
- Backend: `POST /api/applications/{id}/generate-cover-letter` endpoint
- Backend: Optional request body: {recruiter_name, emphasis_points}
- Backend: Celery task `generate_cover_letter` that:
  - Loads master CV experience and skills
  - Loads job title, company, requirements
  - Calls LLM with constrained prompt (3-4 paragraphs, factual only)
  - Validates output for length and structure
  - Stores document as .txt and optionally .pdf
- Backend: LLM prompt template with strict instructions: no fabrication, use only provided CV data, 3-4 paragraph structure
- Backend: Post-generation validation: checks for company name, job title, reasonable length
- Backend: Document storage same as CV generation
- Frontend: "Generate Cover Letter" button with modal form for optional inputs
- Frontend: Preview modal showing generated cover letter with edit capability
- Frontend: Rich text editor for minor edits before finalizing
- Frontend: Save and Download buttons in preview modal
- Frontend: Document list includes cover letters with version history
- Tests: Unit tests for cover letter generation with various inputs
- Tests: Validation tests ensuring no hallucinated content
- Tests: Test output format (paragraph count, length)
- Tests: Integration test for full flow
- Tests: Test with optional inputs (recruiter name, emphasis points)

---

### US-6 (P1) — JSON Job Import

**As** Eduardo  
**I want** to upload a JSON artifact with multiple jobs  
**So that** I can bulk import scraped results or GitHub Actions artifacts

**User Story**
As Eduardo, I need to import multiple job positions at once from a JSON file (scraped results or GitHub Actions artifacts) so that I can quickly populate my job tracker without manual entry for each position.

**Acceptance Criteria**
- Upload interface accepts .json files (max 50MB)
- JSON schema validated before import:
  ```json
  {
    "generated_at": "ISO 8601 timestamp",
    "source": "string (e.g., greenhouse, linkedin, indeed)",
    "jobs": [
      {
        "external_id": "string (required)",
        "title": "string (required)",
        "company": "string (required)",
        "location": "string (optional)",
        "tech_stack": ["array of strings (optional)"],
        "url": "string (optional)",
        "posted_at": "ISO date (optional)",
        "raw_description": "string (required)"
      }
    ]
  }
  ```
- Deduplication: skip jobs where `source + external_id` already exists in database
- Import summary displayed after processing: "Imported: X new jobs, Skipped: Y duplicates"
- Each imported job has `source` set to value from JSON artifact
- Each imported job automatically gets Application with status `NOT_APPLIED`
- Auto-extraction triggered for all newly imported jobs
- Progress indicator during import for large files
- Error handling: invalid JSON shows specific validation errors
- Partial import support: if some jobs fail validation, import others and report errors
- Import history: log each import with timestamp, source, counts, user

**Definition of Done**
- Backend: `POST /api/jobs/import` endpoint accepting file upload
- Backend: JSON schema validation using jsonschema library
- Backend: Deduplication logic: query by (source, external_id) before insert
- Backend: Bulk insert optimization for large imports
- Backend: Response format: {"imported": int, "skipped": int, "errors": [{job_index, error_message}]}
- Backend: Trigger extraction jobs for all imported jobs
- Backend: ImportLog model: id, filename, source, imported_count, skipped_count, error_count, created_at, user_id
- Frontend: File upload component for JSON files
- Frontend: File validation before upload
- Frontend: Progress bar during import
- Frontend: Import summary modal with details (imported, skipped, errors)
- Frontend: Import history view showing past imports
- Tests: Unit tests for JSON parsing and validation
- Tests: Deduplication tests with various scenarios
- Tests: Test with valid JSON containing multiple jobs
- Tests: Test with invalid JSON (schema violations)
- Tests: Test partial import (some valid, some invalid jobs)
- Tests: Performance test with 1000+ jobs

---

### US-7 (P1) — Job List & Filtering

**As** Eduardo  
**I want** to browse jobs sorted newest→oldest and filter by status/company/tags  
**So that** I can prioritize which to apply to

**User Story**
As Eduardo, I need to view all job positions in a list with sorting and filtering options so that I can easily find and prioritize jobs based on application status, company, or required technologies.

**Acceptance Criteria**
- Default view: all jobs sorted by created_at (newest → oldest)
- Sorting options:
  - Created date (newest first, oldest first)
  - Posted date (newest first, oldest first)
  - Company name (A-Z, Z-A)
  - Application status
- Filter options:
  - Application status: NOT_APPLIED, APPLIED, INTERVIEW, REJECTED, OFFER, WITHDRAWN (multi-select)
  - Company: dropdown with autocomplete (derived from existing jobs)
  - Tech tags: multi-select dropdown/tag selector (derived from normalized_stack)
  - Date range: created between date1 and date2
- Filters can be combined (AND logic)
- Job list item displays:
  - Job title and company
  - Location (if available)
  - Application status badge with color coding
  - Top 3-5 tech tags as badges
  - Posted date or created date
  - Quick actions: View Details, Generate CV, Generate Cover Letter
- Pagination: 20 jobs per page with page navigation
- Search bar: full-text search across title, company, location, raw_description
- Filter state persists in URL query params (shareable, bookmarkable)
- "Clear all filters" button resets to default view
- Results count displayed: "Showing X of Y jobs"
- Empty state: if no jobs match filters, show "No jobs found" with clear filters suggestion
- Clicking job row opens detail view/modal with full information and actions

**Definition of Done**
- Backend: `GET /api/jobs` endpoint with query parameters:
  - `sort`: created_at_desc|created_at_asc|posted_at_desc|posted_at_asc|company_asc|company_desc|status
  - `status`: comma-separated list of statuses
  - `company`: exact match or comma-separated list
  - `tags`: comma-separated list (OR logic within tags)
  - `date_from`, `date_to`: ISO date strings
  - `search`: full-text search string
  - `page`, `page_size`: pagination params
- Backend: Response includes: {jobs: [...], total_count: int, page: int, page_size: int, filters_applied: {}}
- Backend: Optimize queries with proper indexes on: created_at, posted_at, company, status, normalized_stack
- Backend: Full-text search index on title, company, location, raw_description
- Frontend: Job list component with grid/list view toggle
- Frontend: Filter sidebar with all specified filters
- Frontend: Sort dropdown in header
- Frontend: Search bar with debounce (300ms)
- Frontend: Pagination component
- Frontend: URL state management (React Router query params)
- Frontend: Loading skeleton while fetching
- Frontend: Job detail modal or route
- Tests: Unit tests for backend filtering logic
- Tests: Test each filter independently and in combination
- Tests: Test sorting for each option
- Tests: Test pagination edge cases
- Tests: Test search functionality
- Tests: Frontend component tests for filters and sorting

---

### US-8 (P1) — API Configuration & LLM Provider Management

**As** Eduardo  
**I want** to configure LLM API keys and select providers  
**So that** I can use different LLM services based on cost and availability

**User Story**
As Eduardo, I need to configure API keys for different LLM providers and select which provider to use for each operation (requirements extraction, CV generation, cover letter generation) so that I can optimize for cost, quality, and availability.

**Acceptance Criteria**
- Settings page accessible from main navigation
- LLM Provider configuration section with supported providers:
  - Google AI Studio (Gemini) - FREE tier
  - Hugging Face Inference API - FREE tier
  - OpenAI (GPT-4, GPT-4 Turbo) - PAID
  - DeepSeek - PAID
- For each provider:
  - Enable/disable toggle
  - API key input field (masked, with show/hide toggle)
  - Test connection button to verify API key
  - Default model selection dropdown
- Provider selection for operations:
  - Requirements extraction: dropdown to select provider
  - CV generation: dropdown to select provider
  - Cover letter generation: dropdown to select provider
- API keys encrypted at rest in database
- Validation: API key format validated before saving
- Test connection: sends test request to verify credentials
- Success/error feedback for all operations
- Ability to delete/clear API keys
- Default configuration: Google AI Studio enabled, others disabled
- Warning if no provider configured when trying to generate documents

**Definition of Done**
- Backend: `GET /api/settings/llm-providers` endpoint
- Backend: `PUT /api/settings/llm-providers` endpoint to update configuration
- Backend: `POST /api/settings/llm-providers/test` endpoint to test API key
- Backend: LLMConfig model: id, provider (enum), api_key_encrypted, is_enabled, default_model, created_at, updated_at
- Backend: Encryption utility for API keys (using Fernet or similar)
- Backend: Provider selection stored in UserSettings: extraction_provider, cv_generation_provider, cover_letter_generation_provider
- Backend: LLM service layer uses configured provider for each operation
- Frontend: Settings page with provider configuration UI
- Frontend: Masked input fields for API keys
- Frontend: Test connection button with loading and result feedback
- Frontend: Form validation for API key format
- Frontend: Save button with confirmation
- Tests: Unit tests for API key encryption/decryption
- Tests: Integration tests for provider selection
- Tests: Test connection validation for each provider

---

### US-9 (P1) — Application Status Management

**As** Eduardo  
**I want** to update application status as I progress through the hiring process  
**So that** I can track which stage each application is in

**User Story**
As Eduardo, I need to update the status of my job applications as I progress through different stages of the hiring process so that I can keep track of where each application stands and prioritize my efforts.

**Acceptance Criteria**
- Application status can be one of: NOT_APPLIED, APPLIED, INTERVIEW, REJECTED, OFFER, WITHDRAWN
- Status can be updated from Application detail view via dropdown or button group
- Status change triggers:
  - Timestamp recorded for status_updated_at
  - Optional notes field to add context (e.g., interview date, rejection reason)
  - Status history preserved (audit trail)
- Visual indicators:
  - Color-coded status badges (NOT_APPLIED=gray, APPLIED=blue, INTERVIEW=yellow, REJECTED=red, OFFER=green, WITHDRAWN=orange)
  - Status icons for quick recognition
- Status transition validation:
  - Allow any transition (flexible workflow)
  - Warning for unusual transitions (e.g., OFFER → REJECTED)
- Status filters work in job list view
- Dashboard shows status distribution: pie chart or bar chart with counts per status
- Quick actions from job list: "Mark as Applied", "Schedule Interview", "Mark as Rejected"
- Notes field supports markdown formatting
- Status history displayed in timeline format on Application detail page

**Definition of Done**
- Backend: `PATCH /api/applications/{id}/status` endpoint
- Backend: Request body: {status: string, notes: string (optional)}
- Backend: ApplicationStatusHistory model: id, application_id, old_status, new_status, changed_at, notes
- Backend: Application model updated_at timestamp updated on status change
- Backend: `GET /api/applications/{id}/history` endpoint for status history
- Frontend: Status update dropdown/buttons in Application detail
- Frontend: Notes textarea for status updates
- Frontend: Confirmation modal for status changes
- Frontend: Status history timeline component
- Frontend: Color-coded status badges with icons
- Frontend: Quick action buttons in job list
- Frontend: Dashboard with status distribution chart (using Chart.js or similar)
- Tests: Unit tests for status update endpoint
- Tests: Test status history creation
- Tests: Test invalid status transitions
- Tests: Frontend component tests for status updates

---

### US-10 (P2) — LLM Cost Tracking & Usage Monitoring

**As** Eduardo  
**I want** to see tokens/cost per generated document and total monthly usage  
**So that** I can control my LLM spend

**User Story**
As Eduardo, I need to monitor my LLM API usage including tokens consumed and estimated costs so that I can stay within budget and make informed decisions about which providers to use.

**Acceptance Criteria**
- Each generated document displays:
  - Model used (e.g., "gpt-4-turbo", "gemini-pro")
  - Total tokens (prompt + completion)
  - Estimated cost in USD
  - Generation timestamp
- Usage dashboard accessible from main navigation with:
  - Total spend this month (estimated)
  - Total tokens used this month
  - Spend by provider (pie chart)
  - Daily usage chart (last 30 days)
  - Usage by operation type (extraction, CV gen, cover letter gen)
- Cost estimation based on provider pricing:
  - Google AI Studio: FREE (show $0.00)
  - Hugging Face: FREE (show $0.00)
  - OpenAI: calculated based on current pricing per 1K tokens
  - DeepSeek: calculated based on current pricing
- Configurable monthly budget with alerts:
  - Set monthly budget limit in settings
  - Warning at 80% of budget
  - Block operations at 100% (with override option)
- Export usage data: CSV download with all operations and costs
- Usage breakdown table:
  - Date | Operation Type | Job Title | Provider | Model | Tokens | Cost
  - Sortable and filterable
  - Pagination (50 per page)

**Definition of Done**
- Backend: Token/cost tracking in all LLM wrapper calls
- Backend: Pricing configuration for each provider/model
- Backend: `GET /api/usage/summary` endpoint: {current_month_cost, current_month_tokens, by_provider, by_operation}
- Backend: `GET /api/usage/history` endpoint: paginated list of all LLM operations with filters
- Backend: `GET /api/usage/export` endpoint: CSV download
- Backend: `GET /api/settings/budget` and `PUT /api/settings/budget` endpoints
- Backend: Budget check before LLM operations
- Backend: UsageLog model: id, operation_type, provider, model, prompt_tokens, completion_tokens, total_tokens, estimated_cost, job_id, application_id, document_id, created_at
- Frontend: Usage dashboard with charts (Chart.js)
- Frontend: Budget configuration in settings
- Frontend: Budget progress bar in header/dashboard
- Frontend: Usage history table with filtering and sorting
- Frontend: CSV export button
- Frontend: Cost display on each document
- Tests: Unit tests for cost calculation for each provider
- Tests: Test budget enforcement logic
- Tests: Test usage aggregation queries
- Tests: Frontend component tests for charts and tables

---

### US-11 (P2) — Document Management & Export

**As** Eduardo  
**I want** to manage all generated documents with version control  
**So that** I can access, compare, and export different versions of my application materials

**User Story**
As Eduardo, I need to view all generated documents (CVs and cover letters) for each application with full version history so that I can download the right version, compare changes, and maintain an organized archive of my application materials.

**Acceptance Criteria**
- Application detail page shows "Documents" section with two tabs: "CVs" and "Cover Letters"
- Each document listed with:
  - Version number (v1, v2, v3...)
  - Creation date and time
  - Model used for generation
  - File format (PDF, TXT)
  - File size
  - Download button
  - Preview button (for PDF)
  - Delete button (with confirmation)
- Document preview modal:
  - PDF viewer for CVs
  - Text display for cover letters
  - Navigation between versions
  - Download from preview
- Version comparison (if multiple versions exist):
  - Side-by-side text diff for cover letters
  - Visual indication of changes
- Bulk export: "Download All Documents" button exports zip file with all documents for an application
- Document naming convention: `{JobTitle}_{Company}_CV_v{N}.pdf` or `{JobTitle}_{Company}_CoverLetter_v{N}.txt`
- Search within documents: filter documents by creation date range
- Document stats: total documents generated, disk space used

**Definition of Done**
- Backend: `GET /api/applications/{id}/documents` endpoint with type filter (CV, COVER_LETTER)
- Backend: `GET /api/documents/{id}/download` endpoint with proper content-type headers
- Backend: `GET /api/documents/{id}/preview` endpoint for PDF viewing
- Backend: `DELETE /api/documents/{id}` endpoint with cascade rules
- Backend: `GET /api/applications/{id}/documents/export` endpoint generates zip file
- Backend: File cleanup job to remove orphaned files
- Backend: Document versioning logic: auto-increment version number per application+type
- Frontend: Documents section in Application detail with tabs
- Frontend: Document list with all metadata displayed
- Frontend: PDF preview modal using PDF.js or similar
- Frontend: Text diff component for cover letter comparison
- Frontend: Download all button with progress indicator
- Frontend: Delete confirmation modal
- Frontend: Document stats display
- Tests: Unit tests for document CRUD operations
- Tests: Test versioning logic
- Tests: Test zip file generation for bulk export
- Tests: Test file cleanup job
- Tests: Frontend component tests for document management

---

## Definition of Done (Project-wide)

A story is considered **Done** when:

1. **Code Quality**
   - Code is merged to main branch via pull request with required approvals
   - All tests passing in CI pipeline (unit, integration, E2E)
   - Code coverage meets minimum threshold: 80% for backend, 70% for frontend
   - Code follows project style guidelines and passes all linters (ESLint, Prettier, Black, Flake8)
   - No critical or high-severity security vulnerabilities in dependencies
   - Code review completed with all comments addressed

2. **Functionality**
   - All acceptance criteria validated and met
   - Feature works in development, staging, and production environments
   - No known critical bugs or regressions
   - Error handling implemented for all failure scenarios
   - User-facing errors display helpful messages with actionable guidance

3. **API Compliance**
   - API endpoints match specification in requirements.md
   - Request/response schemas validated with proper error codes (200, 201, 400, 404, 500)
   - API documentation updated (OpenAPI/Swagger)
   - Backwards compatibility maintained for existing endpoints
   - Rate limiting and throttling implemented where appropriate

4. **UI Implementation**
   - UI implements required flows with comprehensive validation (client-side and server-side)
   - Responsive design tested on key screen sizes: mobile (375px), tablet (768px), desktop (1440px)
   - Accessibility requirements met: keyboard navigation, ARIA labels, color contrast ratios (WCAG 2.1 AA)
   - Loading states and error states implemented for all async operations
   - Consistent with design system (Tailwind CSS utility classes, color scheme, typography)
   - Toast notifications for success/error feedback (using Toastify.js)

5. **LLM Integration**
   - LLM calls wrapped in abstraction layer with provider interface
   - Errors handled gracefully with user-friendly messages and retry options
   - Multiple providers supported: Google AI Studio (FREE), Hugging Face (FREE), OpenAI (PAID), DeepSeek (PAID)
   - Token usage and cost tracking implemented and accurate
   - API keys stored securely (encrypted at rest)
   - Timeout and rate limit handling implemented
   - All LLM operations logged with request/response metadata
   - Prompt templates validated and tested for quality outputs
   - Output validation to prevent hallucinated content

6. **Data Layer**
   - Database migrations present, tested, and reversible
   - Indexes created for query optimization on frequently accessed fields
   - Seed data/fixtures available for development and testing
   - Data validation at model layer (constraints, required fields)
   - Cascade delete rules properly configured to maintain referential integrity
   - MongoDB collections properly indexed for performance

7. **Testing**
   - Unit tests: all business logic functions and classes (minimum 80% coverage)
   - Integration tests: API endpoints, database operations, LLM integrations (with mocks)
   - E2E tests: critical user flows (job creation → CV upload → extraction → document generation → download)
   - Frontend component tests: all interactive components (using React Testing Library)
   - Error scenario tests: network failures, API errors, validation failures, edge cases
   - Performance tests: load testing for bulk operations (e.g., 1000+ job import)

8. **Documentation**
   - README.md updated with new feature description and usage instructions
   - API endpoints documented in OpenAPI/Swagger spec
   - Inline code comments for complex logic
   - Configuration options documented in .env.example
   - Architecture decision records (ADRs) created for significant design decisions
   - Demo/tutorial added for major features

9. **Performance**
   - Response times meet requirements:
     - CRUD operations: < 2 seconds
     - CV upload and parsing: < 8 seconds
     - Document generation: < 30 seconds (LLM-dependent)
     - UI interactions: < 200ms
   - Database queries optimized (no N+1 queries)
   - Async operations use background jobs (Celery)
   - Large file uploads handled with progress indicators

10. **Security**
    - Input validation and sanitization on all user inputs
    - SQL/NoSQL injection prevention (parameterized queries)
    - XSS prevention (proper escaping in UI)
    - CSRF protection enabled
    - API keys and sensitive data encrypted at rest
    - Secrets not committed to repository (.env, .gitignore configured)
    - File upload validation (type, size, content)
    - Rate limiting on API endpoints

11. **Deployment**
    - Feature deployable via docker-compose up
    - Environment variables documented and properly used
    - Database migrations run automatically or via make command
    - No manual steps required for deployment (fully automated)
    - Rollback procedure documented for production
    - Health check endpoints return correct status

12. **User Acceptance**
    - Feature demo'd to stakeholders (if applicable)
    - User feedback incorporated or documented for future iteration
    - Known limitations documented
    - Feature flag or toggle available for gradual rollout (if high risk)
