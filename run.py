from app import app, socketio

if __name__ == '__main__':
  print 'Server running'
  socketio.run(app, host='0.0.0.0', port=5000)
