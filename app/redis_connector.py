import redis

class RedisConnector(object):
  """Redis connector object"""

  def __init__(self, **kwargs):
    # Grab connection credentials
    host     = kwargs.get('host', 'localhost')
    port     = kwargs.get('port', 6379)
    db       = kwargs.get('db', 0)
    password = kwargs.get('password', None)

    # Establish a connection
    self.connection = redis.StrictRedis(host=host, port=port, db=db, password=password)


RedisConnector().connection.set('lol', {'my': 'name', 'is': 'joe'})
print RedisConnector().connection.get('lol')
