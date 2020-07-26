from django.db import models

#models - це як класи у пайтоні, тому ми їх тут створюємо.
#CharField.... - оці різні поля, які існують у проекті і які я створюю то їх шукати у документації, там усе описано дуже добре.
#blank='True' - це означає, що тобі не обовязково це потрібно, по дефолту воно стоїть як false.
#python manage.py migrate - ця штука забирає всі необхідні міграції, які показуються, коли запускаєш сервер.
#python manage.py makemigrations - ця штука передає все, що ми зробили у models.py до нашої DB, це необхідно робити кожного разу як ми щось прописуємо там.
#потім після цього запустимо знову сервер і побачимо, що потрібна міграція, то ми просто знову запустимо ...migrate тай усе.
#також потрібно додати наш клас у admin.py
#потім у views.py треба створити функцію і у ній передати інформацію у темплейт, тільки тоді буде видно інфу із тієї DB на сторінці сайту.

#після цього всього ми створюємо юзера, потім логінимся у нього і щоб побачити те, що ми накодили, треба це імпортувати у admin.py.

class Project(models.Model):
    title = models.CharField(max_length=100)
    description = models.CharField(blank=True, max_length=250)
    image = models.ImageField(upload_to='portfolio/images/')
    url = models.URLField(blank=True)

    def __str__(self):
        return self.title
