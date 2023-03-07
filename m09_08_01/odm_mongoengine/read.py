from models import Post, LinkPost, ImagePost, TextPost, User

if __name__ == '__main__':
    posts = Post.objects()

    for post in posts:
        print(post.to_mongo().to_dict())
    for post in Post.objects(tags='mongodb'):
        print(post.title)

    users = User.objects()
    for user in users:
        print(user.to_mongo().to_dict())

    posts = Post.objects(pk='640790cf89910665c0959f82')
    for post in posts:
        print(post.to_mongo().to_dict())
