# Lab 2 Write-up: Note-Taking App with PostgreSQL & AI Features

**Student ID**: 25050695g  
**Course**: COMP5241  
**Date**: October 18, 2025

---

## Table of Contents
1. [Project Overview](#project-overview)
2. [Task 1: Database Migration to PostgreSQL](#task-1-database-migration-to-postgresql)
3. [Task 2: LLM Translation Feature](#task-2-llm-translation-feature)
4. [Task 3: LLM Summarization Feature](#task-3-llm-summarization-feature)
5. [Challenges & Solutions](#challenges--solutions)
6. [Key Learnings](#key-learnings)
7. [Conclusion](#conclusion)

---

## Project Overview

This lab focused on enhancing a Flask-based note-taking application with three major improvements:
1. **Database Migration**: Migrate from SQLite to PostgreSQL (Supabase)
2. **AI Translation**: Implement LLM-powered translation feature using GitHub Models API
3. **AI Summarization**: Add intelligent content summarization capability

**Technology Stack**:
- Backend: Flask 3.1.1, SQLAlchemy 2.0.41, psycopg2-binary
- Database: PostgreSQL (Supabase Cloud)
- AI/LLM: OpenAI Python SDK with GitHub Models API (gpt-4o-mini)
- Frontend: Vanilla JavaScript, HTML5, CSS3

---

## Task 1: Database Migration to PostgreSQL

### 1.1 Initial Setup

**Objective**: Replace SQLite with cloud-hosted PostgreSQL database using Supabase.

**Step 1: Database Configuration Module**

Created `src/config.py` to centralize database configuration:

```python
def get_database_uri():
    """Get database URI with priority: DATABASE_URL > VERCEL > local SQLite"""
    # Priority 1: DATABASE_URL environment variable
    if 'DATABASE_URL' in os.environ:
        return os.environ['DATABASE_URL']
    
    # Priority 2: Vercel PostgreSQL
    if os.environ.get('VERCEL'):
        # ... Vercel configuration
    
    # Priority 3: Local SQLite (fallback)
    return 'sqlite:///database/app.db'
```

**Step 2: Update Main Application**

Modified `src/main.py` to use the new configuration:

```python
from dotenv import load_dotenv
from src.config import get_database_config

load_dotenv()
app.config.update(get_database_config())
```

**Step 3: Update Dependencies**

Added PostgreSQL support to `requirements.txt`:
```
psycopg2-binary
python-dotenv==1.0.0
```

### 1.2 Supabase Connection Issues

#### Challenge 1: DNS Resolution Error

**Error Log**:
```
could not translate host name "db.nnsimjodhlleqxssaigd.supabase.co" to address: 
nodename nor servname provided, or not known
```

**Root Cause**: Direct connection hostname was not resolving properly.

**Solution**: Switch to Connection Pooling URL instead of direct connection.

#### Challenge 2: Password Format Issue

**Initial Attempt**:
```bash
DATABASE_URL=postgresql://postgres:[Xxw981126!]@...
```

**Error**: Brackets in password caused parsing issues.

**Solution**: Remove brackets from password:
```bash
DATABASE_URL=postgresql://postgres:Xxw981126!@...
```

#### Challenge 3: Wrong Pooling Server

**Error Log**:
```
connection to server at "aws-0-ap-southeast-1.pooler.supabase.com" (13.213.32.43), 
port 6543 failed: FATAL: tenant or user not found
```

**Root Cause**: Using `aws-0` instead of `aws-1` in the pooling URL.

**Solution**: Updated to correct server:
```bash
# Wrong:
aws-0-ap-southeast-1.pooler.supabase.com

# Correct:
aws-1-ap-southeast-1.pooler.supabase.com
```

#### Challenge 4: Username Format for Connection Pooling

**Error**: `FATAL: tenant or user not found`

**Root Cause**: Connection Pooling requires different username format.

**Solution**: Use `postgres.PROJECT_ID` format:
```bash
# Direct connection username:
postgres

# Connection Pooling username:
postgres.nnsimjodhlleqxssaigd
```

#### Challenge 5: Password Update

**Issue**: Password was changed in Supabase dashboard.

**Old Password**: `Xxw981126!`  
**New Password**: `EwmvE3PTsaAP10bD`

**Final Working Configuration**:
```bash
DATABASE_URL=postgresql://postgres.nnsimjodhlleqxssaigd:EwmvE3PTsaAP10bD@aws-1-ap-southeast-1.pooler.supabase.com:6543/postgres
```

### 1.3 Testing & Validation

**Created Comprehensive Test Suite** (`test_supabase.py`):

```python
def test_connection():
    """Test 1: Database connection"""
    # Test database connectivity
    
def test_tables_exist():
    """Test 2: Verify tables exist"""
    # Check User and Note tables
    
def test_user_operations():
    """Test 3: User CRUD operations"""
    # Create, read, update, delete users
    
def test_note_operations():
    """Test 4: Note CRUD operations"""
    # Create, read, update, delete notes
    
def test_multiple_notes():
    """Test 5: Multiple notes handling"""
    # Test batch operations
```

**Test Results**:
```bash
$ python test_supabase.py

Testing Supabase PostgreSQL Database
=====================================

✓ Test 1: Database connection - PASSED
✓ Test 2: Tables exist - PASSED
✓ Test 3: User operations - PASSED
✓ Test 4: Note operations - PASSED
✓ Test 5: Multiple notes - PASSED

=====================================
🎉 All tests passed! Database is working correctly.
5/5 tests passed
```

### 1.4 Diagnostic Tools Created

**Tool 1: `diagnose_connection.py`**
- DNS resolution testing
- Port connectivity check
- Database authentication test
- Table schema verification

**Tool 2: `verify_config.py`**
- Environment variable validation
- Connection string parsing
- Configuration display

**Tool 3: `migrate_to_supabase.py`**
- SQLite to PostgreSQL migration
- Data preservation
- User and Note transfer

---

## Task 2: LLM Translation Feature

### 2.1 Backend Implementation

**Step 1: LLM Module Setup** (`src/llm.py`)

```python
import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv() 
token = os.environ["GITHUB_TOKEN"]
endpoint = "https://models.github.ai/inference"
model = "gpt-4o-mini"

def call_llm_model(model_name, messages, temperature=1.0, top_p=1.0):
    """Generic LLM caller with configurable parameters"""
    client = OpenAI(base_url=endpoint, api_key=token)
    response = client.chat.completions.create(
        messages=messages,
        temperature=temperature,
        top_p=top_p,
        model=model_name
    )
    return response.choices[0].message.content
```

**Step 2: Translation Functions**

```python
def translate_text(text, target_language, source_language="auto"):
    """Translate single text to target language"""
    system_prompt = f"You are a professional translator. Translate to {target_language}. Only return translated text."
    
    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": text}
    ]
    
    return call_llm_model(model, messages, temperature=0.3, top_p=0.9)

def translate_note(title, content, target_language):
    """Translate both title and content"""
    translated_title = translate_text(title, target_language)
    translated_content = translate_text(content, target_language)
    
    return {
        "title": translated_title,
        "content": translated_content
    }
```

**Step 3: API Endpoint** (`src/routes/note.py`)

```python
@note_bp.route('/notes/translate', methods=['POST'])
def translate_note():
    """Translate note to target language"""
    try:
        from src.llm import translate_note as translate_note_llm
        
        data = request.json
        # Validate input
        if not data or 'title' not in data or 'content' not in data:
            return jsonify({'error': 'Required fields missing'}), 400
        
        # Call LLM
        translated = translate_note_llm(
            data['title'], 
            data['content'], 
            data['targetLanguage']
        )
        
        return jsonify(translated), 200
    except Exception as e:
        return jsonify({'error': f'Translation failed: {str(e)}'}), 500
```

### 2.2 Frontend Implementation

**UI Components** (HTML):

```html
<!-- Translation Controls -->
<div class="translate-controls">
    <label>🌐 Translate to:</label>
    <select class="translate-select" id="targetLanguage">
        <option value="">Select Language</option>
        <option value="Chinese">Chinese (中文)</option>
        <option value="English">English</option>
        <option value="Spanish">Spanish (Español)</option>
        <!-- ... more languages -->
    </select>
    <button class="btn btn-translate" id="translateBtn">🔄 Translate</button>
</div>
```

**CSS Styling**:

```css
.btn-translate {
    background: #667eea;
    color: white;
}

.translate-controls {
    display: flex;
    align-items: center;
    gap: 10px;
    padding: 15px;
    background: #f8f9fa;
    border-radius: 10px;
}

.translating {
    opacity: 0.6;
    pointer-events: none;
}
```

**JavaScript Logic**:

```javascript
async translateNote() {
    const title = document.getElementById('noteTitle').value;
    const content = document.getElementById('noteContent').value;
    const targetLanguage = document.getElementById('targetLanguage').value;

    // Validation
    if (!targetLanguage) {
        this.showMessage('Please select a target language', 'error');
        return;
    }

    // Show loading state
    translateBtn.disabled = true;
    translateBtn.innerHTML = '🔄 Translating...';

    const response = await fetch('/api/notes/translate', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ title, content, targetLanguage })
    });

    const translated = await response.json();
    
    // Update UI with translated content
    document.getElementById('noteTitle').value = translated.title;
    document.getElementById('noteContent').value = translated.content;
}
```

### 2.3 OpenAI Library Installation Issue

#### Challenge: Missing `openai` Module

**Error Log**:
```
Error translating: Translation failed: No module named 'openai'
```

**Root Cause Analysis**:
- Application running in conda base environment (Python 3.13)
- `openai` package was initially installed in system Python (3.9.6)
- Package not available in conda environment

**Diagnostic Steps**:

```bash
# Check Python environment
$ python --version
Python 3.13.6

# Check for openai in conda
$ conda list | grep openai
# (no output - not installed)

# Verify which Python is running
$ which python
/opt/miniconda3/bin/python
```

**Solution**:

```bash
# Install openai in conda environment
$ pip install openai

Collecting openai
  Downloading openai-2.5.0-py3-none-any.whl (999 kB)
Successfully installed openai-2.5.0 anyio-4.11.0 httpx-0.28.1 ...

# Verify installation
$ python -c "import openai; print(f'OpenAI version: {openai.__version__}')"
OpenAI version: 2.5.0
```

**Updated `requirements.txt`**:
```
openai>=1.0.0
```

### 2.4 Environment Configuration

**`.env` file**:
```bash
# Supabase PostgreSQL
DATABASE_URL=postgresql://postgres.nnsimjodhlleqxssaigd:EwmvE3PTsaAP10bD@aws-1-ap-southeast-1.pooler.supabase.com:6543/postgres

# GitHub Models API
GITHUB_TOKEN=github_pat_11AJ75QJQ0UpuPO9mo6dDU_...

# Flask
SECRET_KEY=asdf#FGSgvasgf$5$WGT
FLASK_ENV=development
```

**`.env.example`** (for version control):
```bash
DATABASE_URL=postgresql://postgres:your_password@...
GITHUB_TOKEN=your_github_token_here
SECRET_KEY=your_secret_key
FLASK_ENV=development
```

### 2.5 Testing Translation Feature

**Test Cases**:

1. **English to Chinese**:
   - Input: "Hello, World!"
   - Output: "你好，世界！"

2. **Chinese to English**:
   - Input: "这是一个笔记应用"
   - Output: "This is a note-taking application"

3. **Long Content Translation**:
   - Successfully translated multi-paragraph content
   - Preserved formatting and meaning

**Performance**:
- Average response time: 2-4 seconds
- Model: gpt-4o-mini (fast and cost-effective)
- Temperature: 0.3 (more deterministic translations)

---

## Task 3: LLM Summarization Feature

### 3.1 Backend Implementation

**Step 1: Summarization Functions** (`src/llm.py`)

```python
def summarize_text(text, summary_length="medium"):
    """Summarize text with configurable length"""
    length_instructions = {
        "short": "Provide a concise summary in 1-2 sentences.",
        "medium": "Provide a balanced summary in 3-5 sentences.",
        "long": "Provide a comprehensive summary in a detailed paragraph."
    }
    
    instruction = length_instructions.get(summary_length, length_instructions["medium"])
    
    system_prompt = f"""You are an expert at summarizing text. {instruction}
Be clear, accurate, and maintain the original meaning."""
    
    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": f"Please summarize:\n\n{text}"}
    ]
    
    return call_llm_model(model, messages, temperature=0.5, top_p=0.9)

def summarize_note(title, content, summary_length="medium"):
    """Generate summary of note content"""
    # Combine title and content for better context
    full_text = f"Title: {title}\n\nContent: {content}"
    summary = summarize_text(full_text, summary_length)
    
    return {"summary": summary}
```

**Step 2: API Endpoint** (`src/routes/note.py`)

```python
@note_bp.route('/notes/summarize', methods=['POST'])
def summarize_note():
    """Generate summary using LLM"""
    try:
        from src.llm import summarize_note as summarize_note_llm
        
        data = request.json
        if not data or 'title' not in data or 'content' not in data:
            return jsonify({'error': 'Required fields missing'}), 400
        
        summary_length = data.get('summaryLength', 'medium')
        
        # Validate summary length
        if summary_length not in ['short', 'medium', 'long']:
            return jsonify({'error': 'Invalid summaryLength'}), 400
        
        result = summarize_note_llm(
            data['title'], 
            data['content'], 
            summary_length
        )
        
        return jsonify(result), 200
    except Exception as e:
        return jsonify({'error': f'Summarization failed: {str(e)}'}), 500
```

### 3.2 Frontend Implementation

**UI Components**:

```html
<!-- Summarization Controls -->
<div class="summary-controls">
    <label>📝 Summarize:</label>
    <select class="summary-select" id="summaryLength">
        <option value="short">Short (1-2 sentences)</option>
        <option value="medium" selected>Medium (3-5 sentences)</option>
        <option value="long">Long (detailed)</option>
    </select>
    <button class="btn btn-summarize" id="summarizeBtn">✨ Generate Summary</button>
</div>

<!-- Summary Result Display -->
<div class="summary-result" id="summaryResult">
    <h4>📋 Summary:</h4>
    <p id="summaryText"></p>
</div>
```

**CSS Styling**:

```css
.btn-summarize {
    background: #17a2b8;
    color: white;
}

.summary-controls {
    display: flex;
    align-items: center;
    gap: 10px;
    padding: 15px;
    background: #e8f4f8;
    border-radius: 10px;
}

.summary-result {
    margin-top: 15px;
    padding: 15px;
    background: #e8f4f8;
    border-left: 4px solid #17a2b8;
    border-radius: 8px;
    display: none; /* Hidden by default */
}

.summary-result.show {
    display: block;
}
```

**JavaScript Logic**:

```javascript
async summarizeNote() {
    const title = document.getElementById('noteTitle').value;
    const content = document.getElementById('noteContent').value;
    const summaryLength = document.getElementById('summaryLength').value;

    if (!content.trim()) {
        this.showMessage('Please enter content to summarize', 'error');
        return;
    }

    // Show loading state
    summarizeBtn.disabled = true;
    summarizeBtn.innerHTML = '✨ Generating...';

    const response = await fetch('/api/notes/summarize', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
            title: title || 'Untitled',
            content: content,
            summaryLength: summaryLength
        })
    });

    const result = await response.json();
    
    // Display summary
    document.getElementById('summaryText').textContent = result.summary;
    document.getElementById('summaryResult').classList.add('show');
    
    this.showMessage('✨ Summary generated!', 'success');
}
```

**Auto-hide Summary on Note Switch**:

```javascript
async selectNote(noteId) {
    // ... load note content
    
    // Hide summary when switching notes
    document.getElementById('summaryResult').classList.remove('show');
}

createNewNote() {
    // ... create new note
    
    // Hide summary for new note
    document.getElementById('summaryResult').classList.remove('show');
}
```

### 3.3 Testing Summarization Feature

**Test Case 1: Short Summary**

*Input*:
```
Title: Machine Learning Basics
Content: Machine learning is a subset of artificial intelligence that enables 
systems to learn and improve from experience without being explicitly programmed. 
It focuses on developing computer programs that can access data and use it to 
learn for themselves. The process begins with data observation, looking for 
patterns, and making better decisions in the future.
```

*Output (Short)*:
```
Machine learning is an AI subset that allows systems to learn from experience 
without explicit programming, focusing on pattern recognition and data-driven 
decision making.
```

**Test Case 2: Medium Summary**

*Same Input*

*Output (Medium)*:
```
Machine learning is a subset of artificial intelligence that enables systems to 
learn and improve from experience autonomously. It focuses on developing programs 
that can access and learn from data independently. The process involves observing 
data, identifying patterns, and using these insights to make improved decisions 
over time. This approach allows computers to enhance their performance without 
requiring explicit programming for every scenario.
```

**Test Case 3: Long Summary**

*Same Input*

*Output (Long)*:
```
Machine learning represents a crucial subset of artificial intelligence that 
fundamentally changes how systems operate by enabling them to learn and improve 
from experience without requiring explicit programming for every task. The core 
focus of machine learning is the development of sophisticated computer programs 
that can autonomously access data sources and utilize this information to 
continuously learn and adapt. The machine learning process follows a systematic 
approach: it begins with careful observation of data, then analyzes this 
information to identify meaningful patterns and relationships, and finally 
leverages these discovered patterns to make increasingly better decisions in 
future scenarios. This self-improving capability represents a paradigm shift 
from traditional programming approaches.
```

---

## Challenges & Solutions

### Challenge 1: Database Connection Pooling

**Problem**: Direct Supabase connection was unreliable with DNS resolution issues.

**Solution**: 
- Use Connection Pooling URL instead of direct connection
- Format: `postgresql://postgres.PROJECT_ID:PASSWORD@aws-1-ap-southeast-1.pooler.supabase.com:6543/postgres`
- Provides better connection management and reliability

**Lesson Learned**: Cloud databases often provide multiple connection methods; Connection Pooling is preferred for web applications.

### Challenge 2: Python Environment Management

**Problem**: Package installed in wrong Python environment.

**Investigation Process**:
1. Checked which Python is running: `which python`
2. Verified conda environment: `conda list`
3. Compared with system Python: `/Library/Developer/CommandLineTools/usr/bin/python3`

**Solution**: Always install packages in the active environment where the application runs.

**Lesson Learned**: Use virtual environments and verify active environment before installing packages.

### Challenge 3: API Error Handling

**Problem**: LLM API calls could fail due to network issues, rate limits, or invalid inputs.

**Solution**: Implemented comprehensive error handling:

```python
try:
    result = call_llm_model(...)
    return result
except Exception as e:
    raise Exception(f"Translation failed: {str(e)}")
```

**Frontend Error Display**:
```javascript
catch (error) {
    this.showMessage(`Error: ${error.message}`, 'error');
}
```

**Lesson Learned**: Always handle API failures gracefully with user-friendly error messages.

### Challenge 4: UI/UX Consistency

**Problem**: Multiple AI features needed consistent design language.

**Solution**:
- Created reusable CSS classes for controls
- Consistent color scheme:
  - Translation: Purple (#667eea)
  - Summarization: Teal (#17a2b8)
  - Both use similar layout structure
- Unified loading states with `.translating` and `.summarizing` classes

**Lesson Learned**: Establish design patterns early for scalable UI development.

### Challenge 5: State Management

**Problem**: Summary display persisting when switching between notes.

**Solution**: Hide summary result on note switch:
```javascript
// In selectNote() and createNewNote()
document.getElementById('summaryResult').classList.remove('show');
```

**Lesson Learned**: Consider all state changes when implementing new features.

---

## Key Learnings

### 1. Database Migration Best Practices

- **Use Environment Variables**: Never hardcode database credentials
- **Connection Pooling**: Essential for cloud databases
- **Fallback Strategy**: Implement graceful degradation (PostgreSQL → SQLite)
- **Test Thoroughly**: Create comprehensive test suite before production deployment

### 2. LLM Integration

- **Model Selection**: gpt-4o-mini provides good balance of speed, cost, and quality
- **Temperature Tuning**:
  - Translation: 0.3 (more deterministic)
  - Summarization: 0.5 (balanced creativity)
- **Prompt Engineering**: Clear, specific system prompts improve output quality
- **Error Handling**: LLM APIs can fail; always have fallbacks

### 3. Frontend Development

- **Progressive Enhancement**: Add features without breaking existing functionality
- **Loading States**: Always show feedback during async operations
- **Responsive Design**: Use flexbox/grid for adaptable layouts
- **User Feedback**: Clear success/error messages improve UX

### 4. Development Workflow

- **Incremental Development**: Build and test one feature at a time
- **Version Control**: Commit after each working feature
- **Documentation**: Write docs as you code, not after
- **Testing**: Automated tests catch issues early

### 5. Cloud Services

- **Supabase**: Excellent PostgreSQL hosting with generous free tier
- **GitHub Models**: Free API access for testing and development
- **Environment Separation**: Development vs. Production configurations

---

## Conclusion

This lab successfully demonstrated the integration of modern cloud services and AI capabilities into a full-stack web application. The migration from SQLite to PostgreSQL (Supabase) provided scalability and cloud deployment readiness. The addition of LLM-powered translation and summarization features showcased practical applications of AI in user-facing products.

### Key Achievements

✅ **Database Migration**
- Successfully migrated to PostgreSQL on Supabase
- Implemented robust connection pooling
- Created comprehensive test suite (5/5 tests passing)
- Developed diagnostic tools for troubleshooting

✅ **Translation Feature**
- Integrated GitHub Models API with gpt-4o-mini
- Support for 10 languages
- Real-time translation with loading feedback
- Error handling and validation

✅ **Summarization Feature**
- Three configurable summary lengths
- Context-aware summarization (title + content)
- Clean UI with result display
- State management across note switches

### Technical Skills Gained

1. **Database Management**: PostgreSQL connection, SQLAlchemy ORM, connection pooling
2. **API Integration**: OpenAI SDK, RESTful API design, async operations
3. **Frontend Development**: Modern JavaScript, CSS animations, state management
4. **DevOps**: Environment configuration, debugging, cloud deployment preparation
5. **AI/LLM**: Prompt engineering, parameter tuning, error handling

### Future Enhancements

1. **Caching**: Implement Redis for frequently translated/summarized content
2. **Rate Limiting**: Add API rate limiting to prevent abuse
3. **Batch Operations**: Support batch translation/summarization
4. **More Languages**: Expand language support beyond current 10
5. **Custom Models**: Allow users to select different LLM models
6. **Export Feature**: Export notes with translations/summaries to PDF
7. **Collaborative Features**: Multi-user support with Supabase Auth
8. **Search Enhancement**: Add semantic search using embeddings

### Final Thoughts

This lab provided hands-on experience with real-world challenges in full-stack development, cloud integration, and AI implementation. The iterative problem-solving process—especially debugging the Supabase connection issues—reinforced the importance of systematic troubleshooting and comprehensive logging. The successful integration of multiple technologies (Flask, PostgreSQL, OpenAI, GitHub Models) demonstrates the ability to work with modern development stacks and create production-ready applications.

---

## Appendix: Error Logs & Resolution

### A.1 Database Connection Errors

**Error 1: DNS Resolution**
```
sqlalchemy.exc.OperationalError: (psycopg2.OperationalError) 
could not translate host name "db.nnsimjodhlleqxssaigd.supabase.co" 
to address: nodename nor servname provided, or not known
```
**Resolution**: Switched to Connection Pooling URL

**Error 2: Authentication Failure**
```
FATAL: password authentication failed for user "postgres"
```
**Resolution**: Removed brackets from password, updated to correct password

**Error 3: Tenant Not Found**
```
FATAL: tenant or user not found
hint: You might need to use the connection string from the connection pooling section.
```
**Resolution**: Changed username from `postgres` to `postgres.nnsimjodhlleqxssaigd`

### A.2 Python Package Errors

**Error: Missing OpenAI Module**
```
ModuleNotFoundError: No module named 'openai'
```
**Resolution**:
```bash
pip install openai
# Verified: OpenAI version: 2.5.0
```

### A.3 Application Errors

**Error: Port Already in Use**
```
Address already in use
Port 5001 is in use by another program.
```
**Resolution**:
```bash
lsof -ti:5001 | xargs kill -9
python src/main.py
```

---

## Repository Structure

```
note-taking-app-25050695g/
├── api/
│   └── index.py                    # Vercel serverless function
├── database/
│   └── app.db                      # SQLite fallback
├── src/
│   ├── config.py                   # Database configuration
│   ├── llm.py                      # LLM integration (translation, summarization)
│   ├── main.py                     # Flask application entry point
│   ├── models/
│   │   ├── note.py                 # Note model
│   │   └── user.py                 # User model
│   ├── routes/
│   │   ├── note.py                 # Note API endpoints
│   │   └── user.py                 # User API endpoints
│   └── static/
│       ├── favicon.ico
│       └── index.html              # Frontend SPA
├── .env                            # Environment variables (gitignored)
├── .env.example                    # Environment template
├── requirements.txt                # Python dependencies
├── test_supabase.py               # Database test suite
├── diagnose_connection.py         # Connection diagnostic tool
├── verify_config.py               # Configuration verification
├── migrate_to_supabase.py         # Migration script
├── lab2_writeup.md                # This document
└── README.md                       # Project documentation
```

---

**End of Write-up**
