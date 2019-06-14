# Пояснительная записка

Данный проект реализует анонимный форум. Он может использоваться для обсуждения различных тем в соответствующих ветках (тредах).

## Функциональные требования

Проект должен обладать следующим функционалом:

1. Посмотреть все треды на форуме.

2. Посмотреть все сообщения в определённом треде.

3. Создать новый тред.

4. Добавить сообщение в тред.

### Схема БД

База данных будет содержать два вида сущностей -- посты (таблица posts) и треды (таблица table). Каждый тред обладает номером (thread\_id), заголовком (header) и открывающим тему сообщением (op\_text). Каждый пост обладает номером треда, к которому относится сообщение (thread\_id) и содержанием (text). При этом номер треда для поста ссылается на одноимённое поле в таблице threads.
