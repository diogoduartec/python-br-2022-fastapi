from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse
from schemas import UserSchema, UserInputSchema, DefaultResponseSchema, FavoriteSchema
from repositories import AssetAsyncRepository, UserRepository, FavoriteRepository, AssetSyncRepository
from typing import List
from asyncio import gather

default_responses={400: {'model': DefaultResponseSchema}}

user_routers = APIRouter(prefix='/user', responses=default_responses)


@user_routers.post('/', description='Create user', responses={201: {'model': DefaultResponseSchema}}, tags=['User'])
async def create_user(user: UserInputSchema):
    try:
        UserRepository.create(user.dict())
        return JSONResponse(
            content={'detail': 'Successfully created'},
            status_code=201
        )
    except Exception as error:
        raise HTTPException(
            status_code=400,
            detail={'message': str(error)}
        )

@user_routers.get('/list', description='List Users', responses={200: {'model': List[UserSchema]}}, tags=['User'])
async def list_users():
    try:
        return JSONResponse(content=UserRepository.list(), status_code=200)
    except Exception as error:
         raise HTTPException(
            status_code=400,
            detail=str(error)
        )


@user_routers.put('/{user_id}', description='Update user', tags=['User'])
async def update_user(user_id: str, user: UserInputSchema):
    try:
        UserRepository.update(user_id, user.dict())
        return JSONResponse(
            content={'detail': 'Successfully udpated'},
            status_code=200
        )
    except Exception as error:
        raise HTTPException(
            status_code=400,
            detail=str(error)
        )

@user_routers.delete('/{user_id}', description='Delete user', tags=['User'])
async def delete_user(user_id: str):
    try:
        UserRepository.delete((user_id))
        return JSONResponse(
            content={'detail': 'Successfully deleted'},
            status_code=200
        )
    except Exception as error:
        raise HTTPException(
            status_code=400,
            detail=str(error)
        )


@user_routers.post('/favorites', tags=['Favorite'])
async def add_favorite(favorite: FavoriteSchema):
    try:
        FavoriteRepository.add(favorite.dict())
        return JSONResponse(
            content={'detail': 'Favorited successfully added'},
            status_code=200
        )
    except Exception as error:
        raise HTTPException(
            status_code=400,
            detail=str(error)
        )


@user_routers.delete('/favorites/{user_id}', tags=['Favorite'])
async def remove_favorite(user_id: str, symbol: str = None):
    try:
        favorite = {'user_id': user_id}
        if symbol:
            favorite['symbol'] = symbol
        FavoriteRepository.remove(favorite)
        return JSONResponse(
            content={'detail': 'Favorited successfully removed'},
            status_code=200
        )
    except Exception as error:
        raise HTTPException(
            status_code=400,
            detail=str(error)
        )


@user_routers.get('/favorites/{user_id}', responses={200: {'model': List[FavoriteSchema]}}, tags=['Favorite'])
async def remove_favorite(user_id: str, symbol: str = None):
    try:
        return JSONResponse(
            content=FavoriteRepository.list(user_id, symbol=symbol),
            status_code=200
        )
    except Exception as error:
        raise HTTPException(
            status_code=400,
            detail=str(error)
        )

@user_routers.get('/daily-summary/{user_id}', tags=['Daily summary'])
async def daily_summary(user_id: str):
    try:
        favorites = FavoriteRepository.list(user_id)
        result = [AssetSyncRepository.daily_summary(favorite['symbol']) for favorite in favorites]
        return JSONResponse(
            content=result,
            status_code=200
        )
    except Exception as error:
        raise HTTPException(
            status_code=400,
            detail=str(error)
        )


@user_routers.get('/daily-summary/async/{user_id}', tags=['Daily summary'])
async def daily_summary(user_id: str):
    try:
        favorites = FavoriteRepository.list(user_id)
        tasks = [AssetAsyncRepository.daily_summary(favorite['symbol']) for favorite in favorites]
        result = await gather(*tasks)
        return JSONResponse(
            content=result,
            status_code=200
        )
    except Exception as error:
        raise HTTPException(
            status_code=400,
            detail=str(error)
        )
