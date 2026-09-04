# AI Project Report Generator

An AI-powered project documentation application that converts a user's natural-language project overview and executive summary into a structured and professionally formatted project report.

The application uses an LLM through OpenRouter to analyze the provided project information and automatically generate detailed project documentation, including project scope, assumptions, risks and mitigations, and a high-level project plan.

The generated content is inserted into a predefined Microsoft Word template containing the organization's standard formatting, header, and footer.

---

## 🚀 Features

### 1. Natural Language Project Input

Users can provide project information in their own words without following a predefined format.

The application currently accepts:

- **Project Overview**
- **Executive Summary**
- **Project Start Date**
- **Project End Date**

The AI analyzes these inputs and generates the remaining project documentation.

---

### 2. AI-Generated Project Overview

The application:

- Analyzes the user's project overview.
- Rephrases the content professionally.
- Expands the explanation where required.
- Adds relevant contextual details based on the provided information.

The result is suitable for inclusion in a formal project document.

---

### 3. AI-Generated Executive Summary

The provided executive summary is:

- Rewritten professionally.
- Expanded with additional relevant details.
- Structured for business/project documentation.
- Kept aligned with the project overview.

---

### 4. Detailed In-Scope

The application automatically generates a detailed **In Scope** section.

The AI:

- Identifies activities and deliverables implied by the project description.
- Converts them into professional scope statements.
- Expands short user inputs into detailed descriptions.
- Adds logically related scope items when appropriate.

The application avoids simply shortening the user's input.

---

### 5. Out-of-Scope Definition

The AI analyzes the project context and generates an **Out of Scope** section containing activities, features, or responsibilities that are outside the defined project boundaries.

This helps clearly establish project boundaries.

---

### 6. Assumptions

The application generates project assumptions based on the provided project information.

Examples may include:

- Availability of required stakeholders.
- Availability of required technical resources.
- Access to required systems or environments.
- Timely availability of project inputs.
- Dependencies on existing infrastructure or applications.

---

### 7. Risk & Mitigation

The application automatically identifies potential project risks and provides corresponding mitigation strategies.

The generated report contains a table with:

| Risk | Mitigation |
|---|---|
| Identified project risk | Recommended mitigation approach |

The risks are generated based on the project's context rather than using a fixed predefined list.

---

### 8. High-Level Project Plan

The application generates a high-level project plan based on the project overview and scope.

The plan contains:

| Task | Start Date | End Date | Effort (Hours) |
|---|---|---|---:|
| Project task | DD-MM-YYYY | DD-MM-YYYY | 40 |

The AI identifies the major project activities and estimates their relative effort.

The application intentionally generates **main project tasks rather than breaking the project into hundreds of daily activities**.

---

## 📅 Working-Day Scheduling

The project scheduler considers a **5-day working week**.

### Working Days

- Monday
- Tuesday
- Wednesday
- Thursday
- Friday

### Holidays

- Saturday
- Sunday

The scheduler automatically skips weekends when assigning task dates.

For example:

```text
Friday     → Working day
Saturday   → Holiday
Sunday     → Holiday
Monday     → Working day
```

---

## ⏱️ Full Project Timeline Utilization

The application uses the complete project duration provided by the user.

For example:

```text
Project Start: 01-04-2026
Project End:   29-05-2026
```

The scheduler calculates the available working days and distributes the generated tasks across the available project timeline.

The effort is adjusted according to the generated task complexity so that the plan utilizes the available project duration instead of finishing significantly earlier than the specified end date.

Each working day is calculated as:

```text
8 hours/day
```

Therefore:

```text
5 working days = 40 hours
```

---

## 🧠 Application Workflow

```text
                    User
                     │
                     ▼
          Enter Project Overview
                     │
                     ▼
          Enter Executive Summary
                     │
                     ▼
       Select Project Start & End Date
                     │
                     ▼
              Streamlit App
                     │
                     ▼
             Build AI Prompt
                     │
                     ▼
             OpenRouter API
                     │
                     ▼
                  LLM
                     │
                     ▼
       ┌─────────────────────────────┐
       │ AI Generated Content        │
       │                             │
       │ • Detailed Overview         │
       │ • Executive Summary         │
       │ • In Scope                  │
       │ • Out of Scope              │
       │ • Assumptions               │
       │ • Risks & Mitigations       │
       │ • Project Tasks             │
       └─────────────────────────────┘
                     │
                     ▼
          Task Scheduling Engine
                     │
                     ▼
       Calculate Working Days
                     │
                     ▼
          Assign Task Dates
                     │
                     ▼
         Calculate Effort Hours
                     │
                     ▼
          Load Word Template
                     │
                     ▼
       Insert Generated Content
                     │
                     ▼
       ┌─────────────────────────────┐
       │ Project Report               │
       │                             │
       │ • Overview                  │
       │ • Executive Summary         │
       │ • In Scope                  │
       │ • Out of Scope              │
       │ • Assumptions               │
       │ • High Level Plan           │
       │ • Risk & Mitigation         │
       └─────────────────────────────┘
                     │
                     ▼
             Download Word
```

---

## 🏗️ Architecture

```text
┌─────────────────────────────┐
│         Streamlit UI        │
│                             │
│ Project Overview            │
│ Executive Summary           │
│ Start Date / End Date       │
└──────────────┬──────────────┘
               │
               ▼
┌─────────────────────────────┐
│       Prompt Builder        │
│                             │
│ Converts user input into    │
│ structured LLM instructions │
└──────────────┬──────────────┘
               │
               ▼
┌─────────────────────────────┐
│       OpenRouter API        │
│                             │
│       GPT-4o-mini           │
└──────────────┬──────────────┘
               │
               ▼
┌─────────────────────────────┐
│       JSON Processing       │
│                             │
│ Parses structured AI output │
└──────────────┬──────────────┘
               │
               ├───────────────────┐
               ▼                   ▼
┌──────────────────────┐   ┌──────────────────────┐
│ Task Scheduling      │   │ Risk & Mitigation    │
│                      │   │ Generation            │
│ Working days         │   │                      │
│ Effort calculation   │   │ Risk table           │
│ Date allocation      │   │ Mitigation           │
└──────────┬───────────┘   └──────────────────────┘
           │
           ▼
┌─────────────────────────────┐
│      Word Generator         │
│                             │
│ python-docx                 │
│                             │
│ Existing Template           │
│ Header / Footer             │
│ Tables / Content            │
└──────────────┬──────────────┘
               │
               ▼
        Project_Report.docx
```

---

## 🛠️ Technology Stack

### Frontend

- **Streamlit**

Used to build the interactive web interface.

### LLM

- **GPT-4o-mini**
- Accessed through **OpenRouter API**

The LLM is responsible for:

- Content expansion
- Professional rewriting
- Scope generation
- Assumption generation
- Risk identification
- Mitigation generation
- Project task generation

### Backend / Processing

- **Python**

Python handles:

- Prompt construction
- LLM communication
- JSON processing
- Working-day calculations
- Task scheduling
- Effort calculations
- Word document generation

### Document Generation

- **python-docx**

Used to:

- Load the standard Word template.
- Add generated content.
- Create project plan tables.
- Create risk and mitigation tables.
- Apply table borders.
- Preserve the template's header/footer.


## ⚙️ Installation

### 1. Clone the repository

```bash
git clone <repository-url>
cd AI-Project-Report-Generator
```

### 2. Create a virtual environment

Windows:

```bash
python -m venv venv
```

Activate:

```bash
venv\Scripts\activate
```

Linux/macOS:

```bash
python3 -m venv venv
source venv/bin/activate
```

---

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

---

## 📦 Requirements

`requirements.txt`:

```text
streamlit
openai
python-docx
```

---

## 🔐 API Key Configuration

The application uses an OpenRouter API key.

For local development, create:

```text
.streamlit/secrets.toml
```

Add:

```toml
OPENROUTER_API_KEY = "your-openrouter-api-key"
```

Do **not** commit `secrets.toml` to GitHub.

Add it to `.gitignore`:

```text
.streamlit/secrets.toml
venv/
__pycache__/
*.pyc
```

---

## ▶️ Run the Application

Start Streamlit:

```bash
streamlit run app.py
```

The application will open in your browser.

---

## 📝 Example Input

### Project Overview

```text
We are planning to build an AI based application that can analyze
PowerShell scripts and identify security and compliance issues.
The application will help IT teams review scripts before deployment.
```

### Executive Summary

```text
The project aims to automate PowerShell script review using AI.
It should reduce manual review effort and help identify security
risks before scripts are deployed.
```

### Project Timeline

```text
Start Date: 01-04-2026
End Date:   29-05-2026
```

The application will generate the remaining project documentation automatically.

---

## 📄 Generated Report

The final Word document contains:

### 1. Project Overview

Professionally rewritten and expanded project description.

### 2. Executive Summary

Expanded business-oriented summary.

### 3. In Scope

Detailed project scope statements.

### 4. Out of Scope

Clearly defined project exclusions.

### 5. Assumptions

Project assumptions derived from the provided information.

### 6. High Level Plan

A timeline-based table containing:

- Task
- Start Date
- End Date
- Effort in Hours

### 7. Risk & Mitigation

A table containing:

- Risk
- Mitigation

---

## 🎯 Objective

The primary objective of this application is to reduce the manual effort required to create project documentation.

Instead of manually preparing multiple sections of a project report, the user provides a project description in natural language and the application uses AI to transform the information into a structured, professional project report.

```text
Natural Language Input
        ↓
      AI Analysis
        ↓
Professional Project Content
        ↓
Project Planning
        ↓
Risk Analysis
        ↓
Standard Word Template
        ↓
Professional Project Report
```