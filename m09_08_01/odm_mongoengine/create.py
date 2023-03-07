from models import Post, LinkPost, ImagePost, TextPost, User

if __name__ == '__main__':
    ross = User(email='ross@example.com', first_name='Ross', last_name='Lawley').save()

    post1 = TextPost(title='Fun with MongoEngine', author=ross)
    post1.content = 'Took a look at MongoEngine today, looks pretty cool.'
    post1.tags = ['mongodb', 'mongoengine']
    post1.save()

    post2 = LinkPost(title='MongoEngine Documentation', author=ross)
    post2.link_url = 'http://docs.mongoengine.com/'
    post2.tags = ['mongoengine']
    post2.save()

    steve = User(email='steve@example.com', first_name='Steve', last_name='Buscemi').save()
    post3 = ImagePost(title='Foto', author=steve)
    post3.image_path = 'https://images.mubicdn.net/images/cast_member/2321/cache-463-1602494874/image-w856.jpg?size=800x'
    post3.tags = ['actor']
    post3.save()
