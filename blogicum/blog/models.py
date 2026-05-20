from django.db import models
from django.contrib.auth import get_user_model
from django.urls import reverse


User = get_user_model()


class PublishedManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(is_published=True)


class BaseModel(models.Model):
    is_published = models.BooleanField(
        default=True,
        verbose_name="Опубликовано",
        help_text="Снимите галочку, чтобы скрыть публикацию.",
    )
    created_at = models.DateTimeField(
        auto_now_add=True, verbose_name="Добавлено"
    )

    objects = models.Manager()
    published = PublishedManager()

    class Meta:
        abstract = True


class Category(BaseModel):
    title = models.CharField(
        max_length=256,
        verbose_name="Заголовок",
        help_text=""
    )
    description = models.TextField(verbose_name="Описание", help_text="")
    slug = models.SlugField(
        unique=True,
        verbose_name="Идентификатор",
        help_text=(
            "Идентификатор страницы для URL; разрешены символы латиницы, "
            "цифры, дефис и подчёркивание."
        ),
    )

    class Meta:
        verbose_name = "категория"
        verbose_name_plural = "Категории"

    def __str__(self):
        return self.title


class Location(BaseModel):
    name = models.CharField(
        max_length=256,
        verbose_name="Название места",
        help_text=""
    )

    class Meta:
        verbose_name = "местоположение"
        verbose_name_plural = "Местоположения"

    def __str__(self):
        return self.name


class Post(BaseModel):
    title = models.CharField(
        max_length=256,
        verbose_name="Заголовок",
        help_text=""
    )
    text = models.TextField(verbose_name="Текст", help_text="")
    pub_date = models.DateTimeField(
        verbose_name="Дата и время публикации",
        help_text=(
            "Если установить дату и время в будущем — "
            "можно делать отложенные публикации."
        ),
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name="Автор публикации",
        help_text="",
    )
    location = models.ForeignKey(
        Location,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="Местоположение",
        help_text="",
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True,
        verbose_name="Категория",
        help_text="",
    )
    image = models.ImageField(
        "Фото",
        upload_to="posts_images",
        blank=True,
    )

    class Meta:
        ordering = ("-pub_date",)
        verbose_name = "публикация"
        verbose_name_plural = "Публикации"

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("blog:post_detail", kwargs={"post_id": self.pk})


class Comment(models.Model):
    text = models.TextField("Текст")
    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
        related_name="comments",
        verbose_name="Публикация",
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="comments",
        verbose_name="Автор",
    )
    created_at = models.DateTimeField("Добавлено", auto_now_add=True)

    class Meta:
        ordering = ("created_at",)
        verbose_name = "комментарий"
        verbose_name_plural = "Комментарии"

    def __str__(self):
        return self.text[:50]
