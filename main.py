#FastAPI Imports
from fastapi import FastAPI
from typing import List
import strawberry
from sqlalchemy import select
from strawberry.asgi import GraphQL

from database import db
from models import Users


@strawberry.type
class User:
    id: int
    name: str
    
@strawberry.type
class Query:
    @strawberry.field
    async def users(self) -> List[User]:
        users = []
        data = await db.execute(select(Users))
        data = data.scalars().all()
        for user_data in data:
            print(user_data.name)
            user = User(id=user_data.id, name=user_data.name)
            users.append(user)
        return users

    @strawberry.field
    async def user(self, id: int) -> User:
        data = await db.execute(select(Users).where(Users.id==id))
        user_data = data.scalars().one_or_none()
        print(user_data.id,user_data.name)
        if user_data:
            return User(id=user_data.id, name=user_data.name)
        else:
            return None
    
    # @strawberry.field
    # async def create_user(self, name: str) -> User:
    #     user_data = User(id=3,name=name)
    #     db.add(user_data)
    #     # try:
    #     await db.commit()
    #     # except Exception:
    #     #     await db.rollback()
    #     return User(id=user_data.id, name=user_data.name)
        
        
@strawberry.type
class UserMutation:
    @strawberry.mutation
    async def create_user(self, name: str) -> User:
        user_data = Users(id=3,name=name)
        db.add(user_data)
        try:
            await db.commit()
        except Exception:
            await db.rollback()
        return User(id=user_data.id, name=user_data.name)

    # @strawberry.mutation
    # def update_user(self, id: int, name: str) -> User:
    #     create your update logic
    #     pass

    # @strawberry.mutation
    # def delete_user(self, id: int) -> User:
    #     create your delete logic
    #     pass
    
schema = strawberry.Schema(query=Query,mutation=UserMutation)
#  mutation=Mutation



def init_app():
    db.init()
    app = FastAPI(
        title="Sample GraphQL APP",
        description="FastAPI GraphQL with Strawberry",
        version="1",
    )
    @app.on_event("startup")
    async def startup():
        pass
        # await db.create_all()
    @app.on_event("shutdown")
    async def shutdown():
        await db.close()
        
    app.mount("/graphql", GraphQL(schema, debug=True))
    

    return app
app = init_app()