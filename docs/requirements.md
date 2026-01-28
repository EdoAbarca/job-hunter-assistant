# Requirements Specification

## Technology Stack

**Frontend**: React.js with Vite, Tailwind CSS, Toastify.js, Iconify React, Yup validation

**Backend**: Python Django with Django REST Framework, JWT, RenderCV for CV generation, background job queuer

**Database**: MongoDB for primary storage, Redis for queue and real-time updates

**LLM Integration**: Google AI Studio API (Gemini), Hugging Face Inference API (open-source models), with pluggable architecture for future providers (OpenAI, DeepSeek)

**DevOps**: Docker, docker-compose, GitHub Actions for CI/CD

---

## Functional Requirements

### FR-0 — Manual Job Intake (Priority: P0)

**Description**: The system shall allow the user to create a job by pasting the full job description into a form and supplying basic metadata (title, company, URL, location).

**Acceptance Criteria**:
- A posted job is persisted and appears in the job list sorted newest→oldest
- All required fields are validated before submission

**Definition of Done**:
- `POST /jobs/manual` endpoint implemented
- Database row created with proper schema
- UI form exists with validation

---

### FR-1 — JSON Job Import (Priority: P1)

**Description**: The system shall accept a JSON artifact containing multiple jobs and import only new jobs (dedupe by `source + external_id`).

**Acceptance Criteria**:
- Upload returns summary (imported count, skipped duplicates)
- New jobs have `source=JSON`
- Duplicate detection works correctly

**Definition of Done**:
- `POST /jobs/import` endpoint implemented
- Artifact parsing logic created
- Deduplication logic implemented and tested

**JSON Schema**:
```json
{
  "generated_at": "2026-01-06T10:00:00Z",
  "source": "greenhouse",
  "jobs": [
    {
      "external_id": "gh_123456",
      "title": "Junior Backend Engineer",
      "company": "Acme Corp",
      "location": "Remote - LATAM",
      "tech_stack": ["python", "django", "aws"],
      "url": "https://acme.jobs/gh_123456",
      "posted_at": "2026-01-05",
      "raw_description": "Full job text here..."
    }
  ]
}
```

---

### FR-2 — Job Model (Priority: P0)

**Description**: Each job shall store comprehensive information to support tailored document generation and tracking.

**Required Fields**:
- `id` (primary key)
- `external_id` (nullable for manual entries)
- `source` (enum: MANUAL, JSON, SCRAPER)
- `title` (string, required)
- `company` (string, required)
- `location` (string, optional)
- `url` (string, optional)
- `raw_description` (text, required)
- `posted_at` (timestamp, optional)
- `normalized_stack` (JSON array)
- `requirements_summary` (text)
- `created_at` (timestamp, auto)

**Acceptance Criteria**:
- Database schema exists and supports required queries
- List can be sorted by `created_at` or `posted_at`
- Proper indexes for filtering and sorting

**Definition of Done**:
- Database migrations created
- Sample data available for testing

---

### FR-3 — Application Creation (Priority: P0)

**Description**: For every new job imported/created, the system shall create an `Application` with initial status `NOT_APPLIED`.

**Application Model**:
- `id` (primary key)
- `job_id` (foreign key to jobs)
- `status` (enum: NOT_APPLIED, APPLIED, INTERVIEW, REJECTED, OFFER, WITHDRAWN)
- `created_at` (timestamp, auto)
- `updated_at` (timestamp, auto)
- `notes` (text, optional)

**Acceptance Criteria**:
- Applications are automatically linked to jobs
- List view can filter by status
- Status transitions are tracked

**Definition of Done**:
- `applications` table created
- Auto-creation logic implemented
- Status update endpoints working

---

### FR-4 — Master CV Upload (Priority: P0)

**Description**: The system shall allow the user to upload a single master CV (source of truth) in various formats.

**Supported Formats**:
- Structured: YAML, JSON, Markdown
- Binary: PDF, DOCX (stored as fallback)

**Acceptance Criteria**:
- Uploaded master CV is stored and visible in UI
- Metadata displayed: upload date, file path, parsed content if structured
- Only one active master CV at a time

**Definition of Done**:
- Upload UI component created
- Backend storage endpoint implemented
- Parser for structured formats (YAML/JSON/Markdown)
- Fallback storage for binary files
- Update/replace functionality

---

### FR-5 — Requirements Extraction (LLM-assisted) (Priority: P0)

**Description**: The system shall extract job requirements/key skills from `raw_description` to produce `normalized_stack` and a short `requirements_summary`. This process uses an LLM via remote API.

**Acceptance Criteria**:
- After ingestion, job shows an extracted summary and tech tags in the UI
- Extraction is logged with model used and token count
- Failures are handled gracefully with user notification

**Definition of Done**:
- Endpoint or background job that calls LLM wrapper implemented
- Results stored in job record
- Sanity test with sample job description passes

---

### FR-6 — Tailored CV Generation (Priority: P0)

**Description**: Given a `Job` and the `Master CV`, the system shall produce a tailored CV variant optimized for the job's extracted requirements (rule-based selection + LLM rewrite).

**Acceptance Criteria**:
- User clicks "Generate CV" → new document created and attached to Application
- Generated CV highlights matched skills and uses phrasing derived from Master CV bullets
- Document metadata contains `model_used` and `tokens_used`

**Definition of Done**:
- `POST /applications/{id}/generate-cv` endpoint implemented
- Document storage mechanism working
- UI link to download created
- E2E test covering generation

---

### FR-7 — Tailored Cover Letter Generation (Priority: P0)

**Description**: Given a `Job` and the `Master CV` (and optionally recruiter/name), the system shall generate a concise (3–4 short paragraphs) cover letter tailored to the job.

**Acceptance Criteria**:
- User clicks "Generate Cover Letter" → document created and attached to Application
- Output is 3–4 short paragraphs
- No fabricated facts or hallucinations
- References job/company name and key experience matches

**Definition of Done**:
- `POST /applications/{id}/generate-cover-letter` endpoint implemented
- UI preview component created
- Sample outputs pass acceptance criteria

---

### FR-8 — Document Storage & Versioning (Priority: P1)

**Description**: Generated documents (CVs/cover letters) shall be stored with comprehensive metadata.

**Document Model**:
- `id` (primary key)
- `application_id` (foreign key)
- `type` (enum: CV, COVER_LETTER)
- `file_path` (string)
- `model_used` (string)
- `tokens_used` (integer, nullable)
- `cost_estimate` (decimal, nullable)
- `created_at` (timestamp)
- `metadata` (JSON)

**Acceptance Criteria**:
- Each Application shows a list of generated documents with metadata
- Documents can be downloaded
- Version history is preserved

**Definition of Done**:
- `documents` table created
- Attachment mechanism implemented
- Download endpoint working

---

### FR-9 — Job List & Filtering (Priority: P0)

**Description**: The system shall display job positions sorted newest→oldest and support filtering by status, company, and tech tag.

**Acceptance Criteria**:
- UI list with sorting controls
- Filters work correctly: status, company, tech tags
- Selecting a job opens detail view with Application and actions

**Definition of Done**:
- Frontend job list component created
- Backend query endpoints with filtering implemented
- Manual QA passed

**API Endpoint**:
```
GET /jobs?status=&company=&tags=&sort=created_at_desc
```

---

### FR-10 — Cost & Token Tracking (Priority: P2)

**Description**: The system shall track LLM usage per generation (tokens used and provider cost if available) and show aggregate usage for the user.

**Acceptance Criteria**:
- Each generated document displays tokens and cost (if returned or estimated)
- Usage dashboard shows totals by day/month
- Configurable cost limits

**Definition of Done**:
- LLM wrapper records tokens/cost in `documents` metadata
- Usage view/dashboard implemented
- Cost calculation logic for different providers

---

## Non-Functional Requirements

### NFR-1 — Single-User Constraint

**Description**: MVP is single-user; no authentication required. All data is assumed personal and not multi-tenant.

**Rationale**: Simplifies initial development and deployment while focusing on core functionality.

---

### NFR-2 — Reliability

**Description**: Manual intake must always function offline of scrapers; system should not depend on scrapers to operate.

**Requirements**:
- Core flows work without scraper
- Graceful degradation if LLM API is unavailable
- Error messages surfaced in UI

---

### NFR-3 — Extensibility

**Description**: LLM integration must be pluggable via adapter/wrapper so providers can be swapped with no code changes beyond configuration.

**Requirements**:
- Abstract LLM provider interface
- Configuration-based provider selection
- Support for multiple providers: OpenAI, Anthropic, Google, etc.

---

### NFR-4 — Security & Privacy

**Description**: Uploaded job descriptions and CVs may contain personal data; store files securely and restrict external logging.

**Requirements**:
- Disk encryption or at-rest protection recommended
- No logging of full raw descriptions to external services
- Input validation and sanitization
- API key encryption and secure storage

---

### NFR-5 — Observability

**Description**: Log LLM calls, errors, and token usage. Error messages should be surfaced in the UI if generation fails.

**Requirements**:
- Structured logging for all LLM calls
- Token usage tracking
- Error handling with user-friendly messages
- Monitoring hooks for production

---

### NFR-6 — Cost Control

**Description**: Provide mechanisms to control and monitor LLM spending.

**Requirements**:
- Simple toggle or QA mode to preview documents without finalizing LLM calls
- Option to set per-day or per-month LLM spend cap
- Warning when approaching limits
- Detailed cost breakdown by document type

---

### NFR-7 — Performance

**Description**: System must respond quickly to user actions to maintain smooth user experience.

**Requirements**:
- CV upload and parsing: < 8 seconds
- Job CRUD operations: < 2 second
- Document generation: < 30 seconds (LLM-dependent)
- UI responsiveness: < 200ms for interactions

---

### NFR-8 — Accessibility

**Description**: Application should be usable by people with diverse abilities.

**Requirements**:
- Keyboard navigation support
- ARIA labels for screen readers
- Sufficient color contrast ratios
- Responsive design for various screen sizes

---

### NFR-9 — Testing Coverage

**Description**: Maintain high code quality through comprehensive testing.

**Requirements**:
- Unit tests for all business logic (minimum 80% coverage)
- Integration tests for LLM API interactions
- End-to-end tests for critical user flows
- UI component testing

---

## Minimal API Contracts

### POST /jobs/manual
**Payload**:
```json
{
  "title": "string (required)",
  "company": "string (required)",
  "location": "string (optional)",
  "url": "string (optional)",
  "posted_at": "ISO date (optional)",
  "raw_description": "string (required)"
}
```
**Response**: `201 Created` with job + application

---

### POST /jobs/import
**Payload**: File upload containing job artifact (see FR-1 schema)  
**Response**: 
```json
{
  "imported": 5,
  "skipped": 2
}
```

---

### GET /jobs
**Query Parameters**:
- `status`: Filter by application status
- `company`: Filter by company name
- `tags`: Filter by tech tags (comma-separated)
- `sort`: Sort order (created_at_desc, posted_at_desc)

**Response**: Paginated job list

---

### POST /applications/{id}/generate-cv
**Action**: Generate CV variant  
**Response**: Document metadata (id, path, tokens, cost)

---

### POST /applications/{id}/generate-cover-letter
**Action**: Generate cover letter  
**Response**: Document metadata (id, path, tokens, cost)

---

## Data Model Summary

### Job
Primary entity for job positions

### Application
Links jobs to application status and tracking

### Document
Stores generated CVs and cover letters with metadata

### MasterCV
Stores user's source CV in structured or binary format
