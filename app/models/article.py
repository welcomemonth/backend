from app.prisma import prisma

class Article:
    def __init__(self, title: str, description: str, body: str, author_id: int):
        self.title = title
        self.description = description
        self.body = body
        self.author_id = author_id

    async def save(self):
        await prisma.article.create(
            data={
                'title': self.title,
                'description': self.description,
                'body': self.body,
                'author_id': self.author_id
            }
        )

class Comment:
    def __init__(self, body: str, article_id: int, author_id: int):
        self.body = body
        self.article_id = article_id
        self.author_id = author_id

    async def save(self):
        await prisma.comment.create(
            data={
                'body': self.body,
                'article_id': self.article_id,
                'author_id': self.author_id
            }
        )
