from models import Post, LinkPost, ImagePost, TextPost, User

if __name__ == '__main__':
    user = User.objects(first_name="Ross")
    user.delete()