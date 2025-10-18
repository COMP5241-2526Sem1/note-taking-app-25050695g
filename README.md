# NoteTaker - Personal Note Management Application

A modern, responsive web application for managing personal notes with a beautiful user interface and full CRUD functionality.

## 🌟 Features

- **Create Notes**: Add new notes with titles and rich content
- **Edit Notes**: Update existing notes with real-time editing
- **Delete Notes**: Remove notes you no longer need
- **Search Notes**: Find notes quickly by searching titles and content
- **Auto-save**: Notes are automatically saved as you type
- **Responsive Design**: Works perfectly on desktop and mobile devices
- **Modern UI**: Beautiful gradient design with smooth animations
- **Real-time Updates**: Instant feedback and updates

## 🚀 Live Demo

The application is deployed and accessible at: **https://3dhkilc88dkk.manus.space**

### Vercel Deployment

This application is ready to be deployed to Vercel. See [VERCEL_DEPLOYMENT.md](VERCEL_DEPLOYMENT.md) for detailed deployment instructions.

**Quick Deploy:**
1. Push code to GitHub
2. Import project on Vercel: https://vercel.com/
3. Deploy with one click

**Note:** For production use on Vercel, consider using an external database (PostgreSQL, MySQL) instead of SQLite. See deployment guide for details.

## 🛠 Technology Stack

### Frontend
- **HTML5**: Semantic markup structure
- **CSS3**: Modern styling with gradients, animations, and responsive design
- **JavaScript (ES6+)**: Interactive functionality and API communication

### Backend
- **Python Flask**: Web framework for API endpoints
- **SQLAlchemy**: ORM for database operations
- **Flask-CORS**: Cross-origin resource sharing support

### Database
- **SQLite**: Lightweight, file-based database for local development
- **PostgreSQL**: Production database via Supabase (cloud-hosted)
- **Flexible Configuration**: Automatic environment detection

## 📁 Project Structure

```
notetaking-app/
├── src/
│   ├── models/
│   │   ├── user.py          # User model (template)
│   │   └── note.py          # Note model with database schema
│   ├── routes/
│   │   ├── user.py          # User API routes (template)
│   │   └── note.py          # Note API endpoints
│   ├── static/
│   │   ├── index.html       # Frontend application
│   │   └── favicon.ico      # Application icon
│   ├── database/
│   │   └── app.db           # SQLite database file
│   └── main.py              # Flask application entry point
├── venv/                    # Python virtual environment
├── requirements.txt         # Python dependencies
└── README.md               # This file
```

## 🔧 Local Development Setup

### Prerequisites
- Python 3.11+
- pip (Python package manager)
- (Optional) Supabase account for PostgreSQL database

### Installation Steps

1. **Clone or download the project**
   ```bash
   python -m venv venv
   ```

2. **Activate the virtual environment**
   ```bash
   source venv/bin/activate
   ```

   Remark: On Windows, use `venv\Scripts\activate`

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **(Optional) Configure Supabase PostgreSQL**
   ```bash
   # Copy environment template
   cp .env.example .env
   
   # Edit .env and add your Supabase connection string
   # DATABASE_URL=postgresql://postgres:password@host:5432/postgres
   ```
   
   See [SUPABASE_QUICK_START.md](SUPABASE_QUICK_START.md) for detailed setup instructions.

5. **Run the application**
   ```bash
   python src/main.py
   ```

6. **Access the application**
   - Open your browser and go to `http://localhost:5001`

### Database Options

The application supports three database configurations:

1. **Supabase PostgreSQL** (Recommended for production)
   - Set `DATABASE_URL` in `.env` file
   - Persistent cloud storage
   - See [SUPABASE_QUICK_START.md](SUPABASE_QUICK_START.md)

2. **Local SQLite** (Default for development)
   - No configuration needed
   - Data stored in `database/app.db`
   - Fast and easy for local development

3. **In-memory SQLite** (Vercel without external DB)
   - Automatic on Vercel deployment
   - Data resets between deployments

## 📡 API Endpoints

### Notes API
- `GET /api/notes` - Get all notes
- `POST /api/notes` - Create a new note
- `GET /api/notes/<id>` - Get a specific note
- `PUT /api/notes/<id>` - Update a note
- `DELETE /api/notes/<id>` - Delete a note
- `GET /api/notes/search?q=<query>` - Search notes

### Request/Response Format
```json
{
  "id": 1,
  "title": "My Note Title",
  "content": "Note content here...",
  "created_at": "2025-09-03T11:26:38.123456",
  "updated_at": "2025-09-03T11:27:30.654321"
}
```

## 🎨 User Interface Features

### Sidebar
- **Search Box**: Real-time search through note titles and content
- **New Note Button**: Create new notes instantly
- **Notes List**: Scrollable list of all notes with previews
- **Note Previews**: Show title, content preview, and last modified date

### Editor Panel
- **Title Input**: Edit note titles
- **Content Textarea**: Rich text editing area
- **Save Button**: Manual save option (auto-save also available)
- **Delete Button**: Remove notes with confirmation
- **Real-time Updates**: Changes reflected immediately

### Design Elements
- **Gradient Background**: Beautiful purple gradient backdrop
- **Glass Morphism**: Semi-transparent panels with backdrop blur
- **Smooth Animations**: Hover effects and transitions
- **Responsive Layout**: Adapts to different screen sizes
- **Modern Typography**: Clean, readable font stack

## 🔒 Database Schema

### Notes Table
```sql
CREATE TABLE note (
    id INTEGER PRIMARY KEY AUTO_INCREMENT,
    title VARCHAR(200) NOT NULL,
    content TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### Users Table (Template)
```sql
CREATE TABLE user (
    id INTEGER PRIMARY KEY AUTO_INCREMENT,
    username VARCHAR(80) UNIQUE NOT NULL,
    email VARCHAR(120) UNIQUE NOT NULL
);
```

## 🗄️ Database Management

### Testing Database Connection
```bash
python test_supabase.py
```

### Migrating Data (SQLite → PostgreSQL)
```bash
python migrate_to_supabase.py
```

### Verifying Configuration
```bash
python verify_config.py
```

### Database Documentation
- [SUPABASE_QUICK_START.md](SUPABASE_QUICK_START.md) - Quick setup guide
- [SUPABASE_SETUP.md](SUPABASE_SETUP.md) - Detailed configuration
- [DATABASE_UPDATE.md](DATABASE_UPDATE.md) - Migration notes
- [IMPLEMENTATION_REPORT.md](IMPLEMENTATION_REPORT.md) - Technical details

## 🚀 Deployment

### Vercel Deployment (Recommended)

This application is configured for Vercel deployment. See detailed instructions in [VERCEL_DEPLOYMENT.md](VERCEL_DEPLOYMENT.md).

**Quick steps:**
1. Set up Supabase PostgreSQL database (see [SUPABASE_QUICK_START.md](SUPABASE_QUICK_START.md))
2. Push code to GitHub
3. Import project on [Vercel](https://vercel.com/)
4. Add environment variable: `DATABASE_URL` (your Supabase connection string)
5. Deploy automatically

**Important:** For production use on Vercel:
- ✅ **Recommended**: Use Supabase PostgreSQL for persistent data storage
- ⚠️ **Alternative**: Use in-memory SQLite (data resets on each deployment)

### Traditional Deployment

The application is also configured for traditional deployment with:
- CORS enabled for cross-origin requests
- Host binding to `0.0.0.0` for external access
- Production-ready Flask configuration
- Persistent SQLite database (local only)

## 🔧 Configuration

### Environment Variables
- `DATABASE_URL`: PostgreSQL connection string (optional, for Supabase)
- `FLASK_ENV`: Set to `development` for debug mode
- `SECRET_KEY`: Flask secret key for sessions

### Database Configuration

The application automatically selects the database based on environment:

1. **DATABASE_URL is set** → Use PostgreSQL (Supabase)
2. **VERCEL environment** → Use in-memory SQLite
3. **Local development** → Use `database/app.db`

Create a `.env` file for local configuration:
```env
DATABASE_URL=postgresql://postgres:password@host:5432/postgres
SECRET_KEY=your_secret_key
FLASK_ENV=development
```

**Security**: Never commit `.env` file to version control!

## 📱 Browser Compatibility

- Chrome/Chromium (recommended)
- Firefox
- Safari
- Edge
- Mobile browsers (iOS Safari, Chrome Mobile)

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## 📄 License

This project is open source and available under the MIT License.

## 🆘 Support

For issues or questions:
1. Check the browser console for error messages
2. Verify the Flask server is running
3. Ensure all dependencies are installed
4. Check network connectivity for the deployed version

## 🎯 Future Enhancements

Potential improvements for future versions:
- User authentication and multi-user support
- Note categories and tags
- Rich text formatting (bold, italic, lists)
- File attachments
- Export functionality (PDF, Markdown)
- Dark/light theme toggle
- Offline support with service workers
- Note sharing capabilities

---

**Built with ❤️ using Flask, SQLite, and modern web technologies**

