import typing as tp

from fastapi import FastAPI, Query

app = FastAPI()


@app.get('/check')
async def check_item(user_id: int, item_id: tp.List[str] = Query(None)):
    return []
