import streamlit as st
from docx import Document
from openai import OpenAI
from datetime import timedelta
from docx.shared import Pt
import os, json, tempfile, re

MODEL = "meta-llama/llama-3.1-8b-instruct"
TEMPLATE_PATH = "Templetes/Template.docx"
WORK_HOURS_PER_DAY = 8
API_key = st.secrets["OPENROUTER_API_KEY"]
client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key = API_key
)

# ================= UI =================
st.set_page_config("Project Planner", layout="centered")
st.title("Project Report Generator")

overview = st.text_area("Project Overview", height=120)
scope = st.text_area("In Scope", height=120)

col1, col2 = st.columns(2)
with col1:
    start_date = st.date_input("Start Date")
with col2:
    end_date = st.date_input("End Date")

# ================= PROMPT =================
def build_prompt(overview, scope):
    return f"""
You are a senior project manager.

1. Expand project overview professionally.
2. Rewrite the in-scope section:
   - Expand each item into full professional sentences
   - Add missing logical scope items if needed
   - Do NOT shorten
3. Generate MAIN detailed project tasks only (6-12 tasks).
4. Each task must include effort in DAYS.
5. Effort should reflect complexity.

Return JSON only:

{{
 "detailed_overview": "...",
 "professional_scope": ["..."],
 "tasks": [
   {{
     "name": "...",
     "effort_days": 0
   }}
 ]
}}

Overview:
{overview}

Scope:
{scope}
"""

# ================= JSON FIX =================
def extract_json(text):
    match = re.search(r"\{.*\}", text, re.DOTALL)

    if not match:
        raise ValueError("No JSON found in response")

    json_str = match.group(0)
    return json.loads(json_str)

def call_llm(prompt):
    res = client.chat.completions.create(
        model=MODEL,
        messages=[
            {"role": "system", "content": "Return only JSON."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.5
    )
    return extract_json(res.choices[0].message.content)

# ================= TASK SCHEDULER =================
def build_schedule(tasks, start_date, end_date):

    total_available_days = (end_date - start_date).days + 1
    total_effort = sum(t["effort_days"] for t in tasks)

    # scale if exceeds timeline
    if total_effort > total_available_days:
        scale = total_available_days / total_effort
        for t in tasks:
            t["effort_days"] = max(1, round(t["effort_days"] * scale))

    current = start_date
    schedule = []

    for t in tasks:
        start = current
        end = start + timedelta(days=t["effort_days"] - 1)
        hours = t["effort_days"] * WORK_HOURS_PER_DAY

        schedule.append({
            "task": t["name"],
            "start": start.strftime("%d-%m-%Y"),
            "end": end.strftime("%d-%m-%Y"),
            "hours": hours
        })

        current = end + timedelta(days=1)

    return schedule

# ================= TABLE BORDER =================
from docx.oxml import OxmlElement
from docx.oxml.ns import qn

def set_table_border(table):
    tbl = table._tbl
    tblPr = tbl.tblPr
    borders = OxmlElement('w:tblBorders')

    for edge in ('top','left','bottom','right','insideH','insideV'):
        elem = OxmlElement(f'w:{edge}')
        elem.set(qn('w:val'), 'single')
        elem.set(qn('w:sz'), '4')
        elem.set(qn('w:color'), '000000')
        borders.append(elem)

    tblPr.append(borders)

# ================= WORD =================
def generate_word(data, schedule, path):
    doc = Document(TEMPLATE_PATH)

    def heading(text):
        h = doc.add_heading(level=2)
        r = h.add_run(text)
        r.bold = True
        r.font.size = Pt(14)

    # overview
    heading("Project Overview")
    doc.add_paragraph(data["detailed_overview"])

    # scope
    heading("In Scope")
    for s in data["professional_scope"]:
        doc.add_paragraph("• " + str(s))

    # task table
    heading("Project Task Plan")

    table = doc.add_table(rows=1, cols=4)
    set_table_border(table)

    hdr = table.rows[0].cells
    hdr[0].text = "Task"
    hdr[1].text = "Start Date"
    hdr[2].text = "End Date"
    hdr[3].text = "Effort (hrs)"

    for row in schedule:
        cells = table.add_row().cells
        cells[0].text = row["task"]
        cells[1].text = row["start"]
        cells[2].text = row["end"]
        cells[3].text = str(row["hours"])

    doc.save(path)

# ================= MAIN =================
if st.button("Generate Report"):
    with st.spinner("Generating report..."):
        ai = call_llm(build_prompt(overview, scope))

    # limit tasks
    if len(ai["tasks"]) > 12:
        ai["tasks"] = ai["tasks"][:12]

    schedule = build_schedule(ai["tasks"], start_date, end_date)

    with tempfile.TemporaryDirectory() as tmp:
        docx_path = os.path.join(tmp, "report.docx")
        pdf_path = os.path.join(tmp, "report.pdf")

        generate_word(ai, schedule, docx_path)
        

        doc_bytes = open(docx_path, "rb").read()

    st.success("Report Generated")

    col1, col2 = st.columns(2)
    with col1:
        st.download_button("Download Word", doc_bytes, "report.docx")
    
