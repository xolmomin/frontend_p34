import hmac
import hashlib
import urllib.parse
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from aiogram import Bot, Dispatcher
import uvicorn

BOT_TOKEN = "8329233522:AAGJWMJuYZPe2z1Qj-siN5glrk9bYu60r4U"

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()
app = FastAPI()


def check_webapp_signature(init_data: str) -> bool:
    """Telegram WebApp initData xavfsizlik tekshiruvi"""
    parsed = dict(urllib.parse.parse_qsl(init_data, strict_parsing=True))
    hash_str = parsed.pop("hash")

    data_check_string = "\n".join([f"{k}={v}" for k, v in sorted(parsed.items())])
    secret_key = hashlib.sha256(BOT_TOKEN.encode()).digest()

    h = hmac.new(secret_key, data_check_string.encode(), hashlib.sha256).hexdigest()
    return h == hash_str


@app.post("/buy")
async def buy(request: Request):
    data = await request.json()
    product_id = data.get("product_id")
    init_data = data.get("initData")

    if not check_webapp_signature(init_data):
        return JSONResponse({"status": "error", "message": "Invalid initData"}, status_code=403)

    parsed = dict(urllib.parse.parse_qsl(init_data, strict_parsing=True))
    user = parsed.get("user")

    return {"status": "success", "message": f"Buyurtma qabul qilindi! Product ID: {product_id}, User: {user}"}


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
