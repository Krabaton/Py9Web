import pika

credentials = pika.PlainCredentials('guest', 'guest')
connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost', port=5672, credentials=credentials))
channel = connection.channel()

channel.queue_declare(queue='hello')

if __name__ == '__main__':

    channel.basic_publish(exchange='', routing_key='hello', body='Hello group web 9'.encode())
    print(" [x] Sent 'Hello World!'")
    connection.close()
