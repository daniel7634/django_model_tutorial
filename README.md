## Django Model 與 MySQL SQL 語法的對應
Django 是一個強大的 Web 框架，它提供了方便的 ORM 來操作資料庫。

## 準備 Django Model
首先，讓我們看一下我們要處理的 Django 模型：

```python
class Person(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=30)
    like_posts = models.ManyToManyField('Post', blank=True, related_name='liked_person')

class Profile(models.Model):
    id = models.AutoField(primary_key=True)
    person = models.OneToOneField('Person', on_delete=models.CASCADE, related_name='profile')
    phone = models.CharField(max_length=10)

class Post(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=20)
    likes = models.IntegerField(default=0)
    created_by = models.ForeignKey('Person', related_name='created_posts', on_delete=models.RESTRICT)
```
我們建立了三個資料表，並在其中使用了 Django 提供的三種關聯性：
1. `ForeignKey`
2. `OneToOneField`
3. `ManyToManyField`

## Django Model 關聯性的建立與 SQL 語法的關係
透過 `mysqldump` 語法，我們可以了解建立這幾個表格中關聯性的 SQL 語法。
讓我們從 `Post` 資料表中的 `ForeignKey` 開始：
```sql
CREATE TABLE `social_post` (
  `id` int NOT NULL AUTO_INCREMENT,
  `title` varchar(20) NOT NULL,
  `likes` int NOT NULL,
  `created_by_id` int NOT NULL,
  PRIMARY KEY (`id`),
  KEY `social_post_created_by_id_8eed651b_fk_social_person_id` (`created_by_id`),
  CONSTRAINT `social_post_created_by_id_8eed651b_fk_social_person_id` FOREIGN KEY (`created_by_id`) REFERENCES `social_person` (`id`)
) ENGINE=InnoDB
```
在預設情況下，建立 `ForeignKey` 會為該欄位**添加外鍵約束，同時會為其創建索引**。

接下來，我們看一下 `Profile` 資料表中的 `OneToOneField`：
```sql
CREATE TABLE `social_profile` (
  `id` int NOT NULL AUTO_INCREMENT,
  `phone` varchar(10) NOT NULL,
  `person_id` int NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `person_id` (`person_id`),
  CONSTRAINT `social_profile_person_id_0063488b_fk_social_person_id` FOREIGN KEY (`person_id`) REFERENCES `social_person` (`id`)
) ENGINE=InnoDB
```
與 `ForeignKey` 類似，預設情況下，它會為欄位**添加外鍵約束，並建立唯一索引**。

最後，我們來看一下 `Person` 資料表中的 `ManyToManyField`：
```sql
CREATE TABLE `social_person` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(30) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB

CREATE TABLE `social_person_like_posts` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `person_id` int NOT NULL,
  `post_id` int NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `social_person_like_posts_person_id_post_id_1fb6da5a_uniq` (`person_id`,`post_id`),
  KEY `social_person_like_posts_post_id_180d14c9_fk_social_post_id` (`post_id`),
  CONSTRAINT `social_person_like_posts_person_id_63b77bc2_fk_social_person_id` FOREIGN KEY (`person_id`) REFERENCES `social_person` (`id`),
  CONSTRAINT `social_person_like_posts_post_id_180d14c9_fk_social_post_id` FOREIGN KEY (`post_id`) REFERENCES `social_post` (`id`)
) ENGINE=InnoDB
```
可以看到，在這裡我們實際上**建立了另一個資料表**，並在其上建立了兩個外鍵，分別指向 `Persion(id)` 和 `Post(id)`。

## 三種關聯性在使用上的差異
接下來，我們將了解在 Django ORM 查詢中的使用差異。

`ForeignKey`：
```python
post = Post.objects.first()
post.created_by

# 反向查詢
person = Person.objects.first()
person.created_posts.all()
```

`OneToOneField`：
```python
profile = Profile.objects.first()
print(profile.person_id)
print(profile.person.name)

# 反向查詢
person = Person.objects.first()
print(person.profile.phone)
```

`ManyToManyField`
```python
person = Person.objects.first()
person.like_posts.all()

# 反向查詢
post = Post.objects.first()
post.liking_person.all()
```
