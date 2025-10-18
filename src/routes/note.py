from flask import Blueprint, jsonify, request
from src.models.note import Note, db

note_bp = Blueprint('note', __name__)

@note_bp.route('/notes', methods=['GET'])
def get_notes():
    """Get all notes, ordered by most recently updated"""
    notes = Note.query.order_by(Note.updated_at.desc()).all()
    return jsonify([note.to_dict() for note in notes])

@note_bp.route('/notes', methods=['POST'])
def create_note():
    """Create a new note"""
    try:
        data = request.json
        if not data or 'title' not in data or 'content' not in data:
            return jsonify({'error': 'Title and content are required'}), 400
        
        note = Note(title=data['title'], content=data['content'])
        db.session.add(note)
        db.session.commit()
        return jsonify(note.to_dict()), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@note_bp.route('/notes/<int:note_id>', methods=['GET'])
def get_note(note_id):
    """Get a specific note by ID"""
    note = Note.query.get_or_404(note_id)
    return jsonify(note.to_dict())

@note_bp.route('/notes/<int:note_id>', methods=['PUT'])
def update_note(note_id):
    """Update a specific note"""
    try:
        note = Note.query.get_or_404(note_id)
        data = request.json
        
        if not data:
            return jsonify({'error': 'No data provided'}), 400
        
        note.title = data.get('title', note.title)
        note.content = data.get('content', note.content)
        db.session.commit()
        return jsonify(note.to_dict())
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@note_bp.route('/notes/<int:note_id>', methods=['DELETE'])
def delete_note(note_id):
    """Delete a specific note"""
    try:
        note = Note.query.get_or_404(note_id)
        db.session.delete(note)
        db.session.commit()
        return '', 204
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@note_bp.route('/notes/search', methods=['GET'])
def search_notes():
    """Search notes by title or content"""
    query = request.args.get('q', '')
    if not query:
        return jsonify([])
    
    notes = Note.query.filter(
        (Note.title.contains(query)) | (Note.content.contains(query))
    ).order_by(Note.updated_at.desc()).all()
    
    return jsonify([note.to_dict() for note in notes])

@note_bp.route('/notes/translate', methods=['POST'])
def translate_note():
    """Translate note title and content to target language"""
    try:
        from src.llm import translate_note as translate_note_llm
        
        data = request.json
        if not data or 'title' not in data or 'content' not in data or 'targetLanguage' not in data:
            return jsonify({'error': 'Title, content, and targetLanguage are required'}), 400
        
        title = data['title']
        content = data['content']
        target_language = data['targetLanguage']
        
        if not title.strip() and not content.strip():
            return jsonify({'error': 'Cannot translate empty note'}), 400
        
        # Call LLM translation function
        translated = translate_note_llm(title, content, target_language)
        
        return jsonify(translated), 200
        
    except Exception as e:
        return jsonify({'error': f'Translation failed: {str(e)}'}), 500

@note_bp.route('/notes/summarize', methods=['POST'])
def summarize_note():
    """Generate a summary of note content using LLM"""
    try:
        from src.llm import summarize_note as summarize_note_llm
        
        data = request.json
        if not data or 'title' not in data or 'content' not in data:
            return jsonify({'error': 'Title and content are required'}), 400
        
        title = data['title']
        content = data['content']
        summary_length = data.get('summaryLength', 'medium')  # default to medium
        
        if not content.strip():
            return jsonify({'error': 'Cannot summarize empty content'}), 400
        
        # Validate summary length
        if summary_length not in ['short', 'medium', 'long']:
            return jsonify({'error': 'summaryLength must be "short", "medium", or "long"'}), 400
        
        # Call LLM summarization function
        result = summarize_note_llm(title, content, summary_length)
        
        return jsonify(result), 200
        
    except Exception as e:
        return jsonify({'error': f'Summarization failed: {str(e)}'}), 500

