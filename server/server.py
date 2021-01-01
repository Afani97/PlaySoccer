from app import create_app, db
from app.models import User, Event, Sport

# to run gunicorn => 'gunicorn -w 4 server:app --bind=127.0.0.1:5000'
app = create_app()


@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'User': User, 'Event': Event, 'Sport': Sport}
