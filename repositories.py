import requests
from fastapi import HTTPException
import mongomock
from aiohttp import ClientSession
from datetime import date, timedelta
from bson.objectid import ObjectId

client = mongomock.MongoClient()
db = client['mocked_db']

users = db['users']
favorites = db['favorites']

class UserRepository:
    def create(user: dict):
        users.insert_one(user)

    def update(user_id: str, data: dict):
        users.update_one({'_id': ObjectId(user_id)}, {"$set": data})
    
    def delete(user_id: str):
        users.delete_one({'_id': ObjectId(user_id)})

    def list():
        result = list(users.find())
        for item in result:
            item['user_id'] = str(item.pop('_id'))
        return result
    
    def get_by_id(user_id: str):
        result = users.find_one({'_id': ObjectId(user_id)})
        if result:
            result['user_id'] = str(result.pop('_id'))
        return result


class FavoriteRepository:
    def add(favorite: dict):
        user = UserRepository.get_by_id(favorite['user_id'])
        if not user:
            raise ValueError('Invalid user given')
        favorites.insert_one(favorite)

    def remove(favorite: dict):
        user = UserRepository.get_by_id(favorite['user_id'])
        if not user:
            raise ValueError('Invalid user given')
        favorites.delete_one(favorite)

    def list(user_id: str, symbol: str = None):
        favorite = {'user_id': user_id}
        if symbol:
            favorite['symbol'] = symbol
        result = list(favorites.find(favorite))
        for item in result:
            del item['_id']
        return result

class AssetSyncRepository:
    def daily_summary(symbol: str):
        yesterday = date.today() - timedelta(days=1)
        response = requests.get(f'https://www.mercadobitcoin.net/api/{symbol}/day-summary/{yesterday.year}/{yesterday.month}/{yesterday.day}/')
        
        if response.status_code != 200:
            raise HTTPException(status_code=400, detail=f'given status_code from external api: {response.status_code}, {response.text}')
        
        data = response.json()
        
        return {
            'highest': data['highest'],
            'lowest': data['lowest'],
            'symbol': symbol
        }

class AssetAsyncRepository:
    async def daily_summary(symbol: str):
        async with ClientSession() as session:
            yesterday = date.today() - timedelta(days=1)
            url = f'https://www.mercadobitcoin.net/api/{symbol}/day-summary/{yesterday.year}/{yesterday.month}/{yesterday.day}/'
            response = await session.get(url)
            data = await response.json()
            return {
                'highest': data['highest'],
                'lowest': data['lowest'],
                'symbol': symbol
            }
