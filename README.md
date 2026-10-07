# 🤖 Multi-Agent Research System

An AI-powered research system that uses multiple specialized agents to search the web, read relevant webpages, generate a structured research report, and critically evaluate the final report.

## 🚀 Overview

The system takes a research topic from the user and processes it through a multi-stage AI pipeline:

```text
User Research Topic
        ↓
   Search Agent
        ↓
   Tavily Web Search
        ↓
   Reader Agent
        ↓
   Web Scraping
        ↓
   Writer Chain
        ↓
 Research Report
        ↓
   Critic Chain
        ↓
 Score + Feedback
```

Each component has a specific responsibility, making the research process more organized and reliable.

## ✨ Features

- 🔎 **Web Search Agent** — searches the web for recent and relevant information using Tavily.
- 📖 **Reader Agent** — selects a relevant webpage and extracts detailed information.
- 📝 **Research Writer** — generates a structured research report from the collected information.
- 🔍 **Research Critic** — evaluates the generated report for accuracy, completeness, clarity, structure, evidence, and unsupported claims.
- 📊 **Report Scoring** — provides a score out of 10 along with detailed feedback.
- 🤖 **LLM-powered agents** — uses Groq's GPT-OSS model through LangChain.
- 🌐 **Web Scraping** — uses Requests and BeautifulSoup to extract readable webpage content.

## 🏗️ Project Structure

```text
Multi-Agent Research System/
│
├── agents.py
├── create_pipeline.py
├── tools.py
├── requirements.txt
├── .env
└── README.md
```

### `create_pipeline.py`

Acts as the main entry point and controls the complete research pipeline.

Responsibilities:

1. Accept the research topic.
2. Create and run the Search Agent.
3. Create and run the Reader Agent.
4. Generate the research report.
5. Generate critic feedback.
6. Store all outputs in a shared state dictionary.

### `agents.py`

Contains the AI agents and LLM chains:

- Search Agent
- Reader Agent
- Writer Chain
- Critic Chain

### `tools.py`

Contains the tools used by the agents:

- `web_search()` — searches the web using Tavily.
- `scrap_url()` — downloads and extracts readable text from webpages.

## 🔄 How It Works

### 1. User Input

The application asks for a research topic:

```text
Enter research topic: Generative AI
```

The topic is passed to:

```python
run_research_pipeline(topic)
```

### 2. Search Agent

The Search Agent receives the topic and uses the `web_search` tool.

```text
Research Topic
      ↓
Search Agent
      ↓
web_search()
      ↓
Tavily
      ↓
Search Results
```

The search tool returns:

- Title
- URL
- Search snippet

### 3. Reader Agent

The Reader Agent receives the search results and selects a relevant URL.

It then uses:

```python
scrap_url(url)
```

The webpage is downloaded using `requests` and parsed using BeautifulSoup.

Unnecessary HTML elements such as:

- `script`
- `style`
- `nav`
- `header`
- `footer`
- `aside`
- `form`

are removed before extracting the readable text.

### 4. Writer Chain

The search results and scraped webpage content are combined:

```text
SEARCH RESULTS
+
DETAILED SCRAPED CONTENT
        ↓
    Writer LLM
        ↓
 Research Report
```

The generated report contains:

1. Title
2. Introduction
3. Main findings
4. Important evidence
5. Conclusion

### 5. Critic Chain

The generated report is passed to a separate critic chain.

The critic evaluates:

- Accuracy
- Completeness
- Clarity
- Structure
- Evidence
- Unsupported claims

It produces:

```text
Score: X/10

Feedback:
...
```

## 🧠 Technologies Used

- **Python**
- **LangChain**
- **Groq**
- **GPT-OSS-20B**
- **Tavily**
- **BeautifulSoup**
- **Requests**
- **Prompt Engineering**
- **Multi-Agent Architecture**
- **Web Scraping**

## 📦 Installation

Clone the repository:

```bash
git clone https://github.com/BAKINARENDAR/Multi-agent-Research-System.git
```

Move into the project:

```bash
cd Multi-agent-Research-System
```

Create a virtual environment:

```bash
python -m venv venv
```

Activate it on Windows:

```bash
venv\Scripts\activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

## 🔑 Environment Variables

Create a `.env` file in the project root:

```env
GROQ_API_KEY=your_groq_api_key
TAVILY_API_KEY=your_tavily_api_key
```

**Never commit your `.env` file or API keys to GitHub.**

Add this to `.gitignore`:

```gitignore
.env
venv/
.venv/
__pycache__/
*.pyc
```

## ▶️ Running the Project

Run:

```bash
python create_pipeline.py
```

Enter a research topic:

```text
Enter research topic: Latest developments in Generative AI
```

The system will execute:

```text
STEP 1 - SEARCH AGENT
        ↓
STEP 2 - READER AGENT
        ↓
STEP 3 - WRITER CHAIN
        ↓
STEP 4 - CRITIC CHAIN
```

The final output contains:

- Search results
- Scraped research content
- Generated research report
- Critic score
- Critic feedback

## 🎯 Why Multi-Agent Architecture?

Instead of asking one LLM to perform the entire research process, the system divides the task into specialized components.

```text
Search Agent
     ↓
Find information

Reader Agent
     ↓
Read information

Writer
     ↓
Create report

Critic
     ↓
Evaluate report
```

This separation of responsibilities makes the workflow easier to understand, maintain, and extend.

## 🔮 Future Improvements

- Add multiple Reader Agents for different sources.
- Add source credibility scoring.
- Use multiple search queries for better coverage.
- Add citation generation.
- Add report revision based on critic feedback.
- Add a Streamlit web interface.
- Add persistent research history.
- Add parallel agent execution.
- Add fact verification using multiple sources.

## 👨‍💻 Author

**Baki Narendar**

B.Tech Information Technology  
MLR Institute of Technology, Hyderabad

GitHub:  
https://github.com/BAKINARENDAR