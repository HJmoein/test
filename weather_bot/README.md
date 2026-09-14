# ربات هواشناسی تلگرام 🌤

ربات هواشناسی کامل و production-ready با Python 3.11+ و aiogram 3.x

## ویژگی‌ها

- 🌍 دریافت آب‌وهوای لحظه‌ای هر شهر (فارسی و انگلیسی)
- ⚖️ مقایسه همزمان دو شهر با `asyncio.gather`
- 🗣 ترجمه کامل وضعیت آب‌وهوا به فارسی با ایموجی
- 🗺 پشتیبانی از نام شهرهای فارسی (تهران، مشهد، اصفهان و...)
- 💾 ذخیره اطلاعات کاربران در SQLite به صورت async
- ⌨️ کیبورد فارسی جذاب با HTML formatting
- ⚡ کاملاً غیرهمزمان (async) بدون blocking

## نصب و راه‌اندازی

### 1. ساخت محیط مجازی

```bash
python -m venv venv
# ویندوز
venv\Scripts\activate
# لینوکس / مک
source venv/bin/activate
```

### 2. نصب وابستگی‌ها

```bash
pip install -r requirements.txt
```

### 3. تنظیم متغیرهای محیطی

```bash
# کپی فایل نمونه
copy .env.example .env   # ویندوز
# cp .env.example .env  # لینوکس / مک
```

فایل `.env` را ویرایش کنید:

```
BOT_TOKEN=توکن_ربات_از_BotFather
WEATHER_API_KEY=18631ee610164aa99c8125527261409
```

> توکن ربات را از [@BotFather](https://t.me/BotFather) در تلگرام دریافت کنید.

### 4. اجرای ربات

```bash
python -m app.main
```

یا از ریشه پروژه:

```bash
python app/main.py
```

## دستورات ربات

| دستور | توضیح |
|-------|--------|
| `/start` | شروع و نمایش منوی اصلی |
| `/help` | راهنما |
| `/compare شهر1 شهر2` | مقایسه دو شهر (مثال: `/compare تهران مشهد`) |
| `نام شهر` | ارسال نام شهر بدون دستور |

## ساختار پروژه

```
weather_bot/
├── app/
│   ├── main.py
│   ├── config.py
│   ├── handlers/
│   ├── services/
│   ├── database/
│   ├── keyboards/
│   └── utils/
├── data/
├── .env.example
├── requirements.txt
└── README.md
```

## تکنولوژی‌ها

- Python 3.11+
- aiogram 3.x
- aiohttp
- aiosqlite
- python-dotenv
- asyncio
