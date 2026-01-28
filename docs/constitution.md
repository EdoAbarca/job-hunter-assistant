# Job Hunter Assistant Constitution

**Version**: 1.0.0  
**Ratified**: 2026-01-17  
**Last Amended**: 2026-01-17

---

## Purpose

The Job Hunter Assistant is a single-user application designed to streamline and optimize the job application process. It enables job seekers to efficiently manage job opportunities, create tailored CVs and cover letters using AI-powered document generation, and track their application progress—all while maintaining full control over their personal data.

---

## Scope

### In Scope
- Manual job position intake via web form
- JSON-based bulk job import
- Master CV upload and management (YAML/JSON/Markdown/PDF/DOCX)
- Tailored CV generation using LLM APIs
- Customized cover letter generation
- Job position tracking and filtering
- Job application status management
- Document versioning and metadata tracking
- LLM cost and token usage monitoring

### Out of Scope (MVP)
- Multi-user support and authentication
- Automatic job application submission
- Local LLM execution
- Real-time web scraping (scraper artifacts can be imported)
- Job board integrations for posting applications
- Mobile native applications (web responsive design supported)

---

## Core Principles

### I. User-Centric Design
The application must provide an intuitive visual interface that simplifies the job search process. Every feature should reduce friction and save time for job seekers. The UI must be responsive, accessible, and work seamlessly across different devices and screen sizes.

### II. Data Privacy and Security
User data (CVs, personal information, job applications) must be stored securely. All sensitive data should be encrypted at rest and in transit. Users must have full control over their data with options to export and delete information at any time.

**User Data Policy**: Users maintain full ownership of their data. The application serves as a tool to enhance their job search, not to collect or monetize their information.

### III. Document Management
The system must support full CRUD operations for both CV management and job position tracking. Documents should be versioned to allow users to track changes and revert if needed. File formats supported must include PDF, DOCX, and plain text.

### IV. LLM Integration (NON-NEGOTIABLE)
The application must integrate with external LLM services (e.g., OpenAI GPT, Anthropic Claude, Google Gemini) for intelligent content generation. 

**LLM Usage Policy**: The application must never attempt to run LLMs locally. All AI functionality must use cloud-based API services to ensure scalability, reliability, and access to latest models.

The LLM integration must:
- Generate tailored CVs based on original CV and job position
- Create customized cover letters matching job requirements
- Highlight relevant skills and experiences
- Maintain professional tone and formatting
- Be pluggable via adapter/wrapper so providers can be swapped with no code changes beyond config

### V. Quality and Accuracy
Generated documents must maintain factual accuracy based on the original CV. The system must never fabricate experience or qualifications. All AI-generated content should be clearly marked and reviewable by users before export.

### VI. Single-User Architecture
The MVP is designed for single-user operation with no authentication required. All data is assumed personal and not multi-tenant. This constraint simplifies initial development while maintaining security through physical access control.

---

## Technologies

### Stack

**Frontend**
- React.js + JavaScript
- Vite
- Tailwind CSS + Toastify.js + Iconify React
- Yup
- PDF parsing libraries

**Backend**
- Python with Django, JWT, Django REST Framework, PDF parser and generator dependencies (Consider RenderCV for tailored CV generation)
- Queuer for background processes
- RESTful API design

**Database**
- MongoDB
- Redis for queue and real-time updates

**LLM Integration**
- Early Stage: Google AI Studio API for Gemini usage and Hugging Face Inference API for open-source model usage
- Later iterations:
    - OpenAI API (GPT-5)
    - DeepSeek API
**File Storage**
- Local filesystem with organized directory structure
- Later: Cloud storage (S3, GCS) for production deployments

---

## Architecture

### System Components

1. **Web Frontend**: Single-page application providing user interface
2. **API Server**: RESTful backend handling business logic
3. **Database**: Persistent storage for jobs, api keys, and document reference
4. **LLM Adapter**: Abstraction layer for multiple LLM providers
5. **Document Generator**: Service orchestrating CV/cover letter creation
6. **File Storage**: Secure storage for uploaded and generated documents

### Data Flow
1. User uploads master CV → Parsed and stored
2. User adds job position → Saved to database → Application created
3. System extracts job requirements via LLM → Results stored
4. User requests document generation → LLM generates tailored content → Document saved and linked to application

---

## Security Standards

- Input validation and sanitization on all user inputs
- API key encryption and secure storage
- Disk encryption or at-rest protection for stored files
- Background queued works for job position and master CV upload and CV and Cover Letter generation

---

## Constraints

### Explicit Constraints
- Single-user, no multi-user auth for MVP
- Manual paste intake is the primary ingestion method
- No auto application submission to external job boards in MVP
- No local LLM execution; only remote APIs allowed
- LLM integration must be pluggable via adapter/wrapper

### Cost Management
- Provide a simple toggle or QA mode to preview documents without finalizing LLM calls
- Option to set per-day or per-month LLM spend cap
- Token usage tracking and cost estimation for all generations

---

## Governance

This constitution defines the non-negotiable requirements for the Job Hunter Assistant application. All development decisions must align with these core principles. 

### Amendment Process
Changes to this constitution require:
1. Documentation of rationale
2. Impact assessment on existing features
3. Approval from project maintainer(s)
4. Version increment and amendment date update
