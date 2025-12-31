# مرحله ساخت (Build Stage)
FROM node:18-alpine AS builder

WORKDIR /app

# کپی فایل‌های package برای استفاده از Docker cache
COPY package*.json ./

# استفاده از npm install به جای npm ci (برای سازگاری بهتر)
RUN npm install

# کپی تمام فایل‌های پروژه
COPY . .

# ساخت پروژه
RUN npm run build

# مرحله اجرا (Production Stage)
FROM node:18-alpine AS runtime

WORKDIR /app

# نصب serve به‌صورت global
RUN npm install --global serve

# کپی فایل‌های build شده از مرحله قبل
COPY --from=builder /app/dist ./dist

# تعریف پورت
EXPOSE 3000

# اجرای سرور
CMD ["serve", "-s", "dist", "-l", "3000"]
