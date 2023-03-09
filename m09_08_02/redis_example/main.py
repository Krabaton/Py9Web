import redis

client = redis.Redis(host='localhost', port=6379, username='default', password=None, db=1)

if __name__ == '__main__':
    client.set('foo', 'Foo')
    client.set('baz', 100)

    print(client.get('foo').decode())
    print(int(client.get('baz').decode()))

