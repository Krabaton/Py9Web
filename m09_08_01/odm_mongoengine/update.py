from bson import ObjectId

from models import Post, LinkPost, ImagePost, TextPost, User

if __name__ == '__main__':
    post = Post.objects(title='MongoEngine Documentation')
    print(post[0].to_mongo().to_dict())
    post.update(link_url='https://docs.mongoengine.org/apireference.html')
    print(post[0].to_mongo().to_dict())

