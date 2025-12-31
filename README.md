# bestamoozscreener

MVP فیلترنویسی/اسکرینر بورس ایران با FastAPI (بک‌اند) و Next.js + Tailwind (فرانت‌اند). تمرکز روی فیلترها، لیست نتایج و API قابل توسعه بدون نیاز به احراز هویت.

## معماری و پوشه‌ها
```
backend/
  app/
    api/routes/        # مسیرهای FastAPI (فیلترها، نمادها، اسکرینر)
    core/              # تنظیمات
    db/                # اتصال و Seed پایگاه داده
    models/            # مدل‌های SQLAlchemy
    schemas/           # اسکیماهای Pydantic
    services/
      cache/           # کش ساده با TTL
      data_providers/  # Adapter داده بازار (Mock + Stub واقعی)
      filters/         # فیلترهای Plugin و رجیستری
      indicators.py    # اندیکاتورهای SMA/EMA/MACD
      screener.py      # موتور اسکرین
    deps.py            # وابستگی provider پیش‌فرض
  seed/                # داده Mock شامل 200 نماد فرضی
  requirements.txt
frontend/
  app/                 # صفحات Next.js (صفحه اصلی)
  components/          # کامپوننت‌ها (در صورت نیاز)
  tailwind.config.ts
  package.json
Dockerfile ها در backend/ و frontend/ موجود است.
```

## اجرا با Docker Compose
```bash
docker-compose up --build
```
- بک‌اند: http://localhost:8000
- فرانت‌اند: http://localhost:3000 (متصل به بک‌اند روی پورت 8000)

## اجرای جداگانه
### Backend
```bash
cd backend
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```
- پایگاه‌داده SQLite (`app.db`) و Seed اولیه از `backend/seed/symbols_seed.json` بارگذاری می‌شود.

### Frontend
```bash
cd frontend
npm install
npm run dev
```
- متغیر `NEXT_PUBLIC_API_URL` را در `.env.local` در صورت نیاز به URL متفاوت تنظیم کنید (پیش‌فرض: `http://localhost:8000`).

## API های اصلی
- `GET /api/filters` : دریافت تعریف فیلترها و پارامترها برای UI.
- `GET /api/symbols?search=&page=&page_size=` : لیست نمادها از پایگاه داده با صفحه‌بندی.
- `POST /api/screener/run` : اجرای فیلترها (بدنه `{ filters: [{ id, params }] }`).
- `GET /health` : وضعیت سرویس.

## داده بازار و حالت‌ها
- **Mode A (Mock):** فایل `backend/seed/symbols_seed.json` شامل 200 نماد فرضی به‌همراه تاریخچه 60 روزه است. Provider پیش‌فرض (`MockMarketDataProvider`) از این داده استفاده می‌کند و کش 60 ثانیه‌ای برای snapshot/history دارد.
- **Mode B (Real Adapter):** اسکلت `RealMarketDataAdapter` در `backend/app/services/data_providers/stub_provider.py` آماده اتصال به منبع واقعی (REST/SDK). پس از پیاده‌سازی متدها، می‌توانید وابستگی را در `app/deps.py` تغییر دهید تا از Provider واقعی استفاده شود.

## افزودن فیلتر جدید
1. یک کلاس جدید در `backend/app/services/filters/` بسازید و از `FilterBase` ارث ببرید.
2. `id`, `name`, `description` و `parameters` (از نوع `FilterParameter`) را تعریف کنید.
3. متد `evaluate(symbol_data)` را پیاده‌سازی کنید و خروجی `{ passed: bool, reason: str, score?: float }` برگردانید.
4. کلاس را در `AVAILABLE_FILTERS` داخل `backend/app/services/filters/registry.py` ثبت کنید.
5. در صورت نیاز به داده تاریخی/نمایی جدید، متدهای `MarketDataProvider` را گسترش دهید.
6. برای UI نیازی به تغییر کد نیست؛ `/api/filters` به‌روز می‌شود و صفحه از Schema جدید استفاده می‌کند.

## ساختار داده Symbol
- snapshot: `symbol`, `company_name`, `last_price`, `volume`, `trade_value`, `percent_change`, `last_updated`
- history: آرایه‌ای از `{ date, close, volume }`

## تست‌ها
```bash
cd backend
pytest
```

## نکات توسعه
- کش ساده در `services/cache/cache.py` با TTL پیش‌فرض 60 ثانیه فعال است.
- اندیکاتورهای کلیدی در `services/indicators.py` پیاده‌سازی شده‌اند (SMA/EMA/MACD).
- برای مهاجرت به Postgres، مقدار `database_url` را در `.env` یا متغیر محیطی تنظیم کنید و در `docker-compose` سرویس دیتابیس اضافه کنید.
