from app import app, socketio, db
import app.store as s

if __name__ == '__main__':
  s.store_venues('events.json', db)
  print 'App live at http://0.0.0.0:5000'
  socketio.run(app, host='0.0.0.0', port=5000, debug=True)
