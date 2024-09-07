from app.prisma import prisma

class User:
    def __init__(self, username: str, email: str, hashed_password: str):
        self.username = username
        self.email = email
        self.password = hashed_password

    async def save(self):
        return await prisma.user.create(
            data={
                'username': self.username,
                'email': self.email,
                'password': self.password,
            }
        )
