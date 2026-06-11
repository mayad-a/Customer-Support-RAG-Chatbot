FROM python:3.12

# إعداد مجلد العمل
WORKDIR /code

# نسخ ملف المكتبات وتثبيتها
COPY ./requirements.txt /code/requirements.txt
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

# نسخ كل ملفات المشروع (الـ 6 ملفات) للمجلد
COPY . .

# إعطاء صلاحية لتشغيل سكريبت البداية
RUN chmod +x /code/startup.sh

# تشغيل الـ FastAPI على البورت المخصص لـ Hugging Face
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "7860"]