import pika

credentials = pika.PlainCredentials('guest', 'guest')
connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost', port=5672, credentials=credentials))
channel = connection.channel()

channel.exchange_declare(exchange='logs', exchange_type='fanout')

if __name__ == '__main__':

    channel.basic_publish(exchange='logs', routing_key='', body='Hello group web 9'.encode())
    connection.close()
