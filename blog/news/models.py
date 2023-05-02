from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _
from django.template.defaultfilters import slugify
from PIL import Image
from mptt.models import MPTTModel, TreeForeignKey
from django.core.validators import validate_ipv46_address


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name=_('User'))
    avatar = models.ImageField(upload_to='photos/avatars/%Y/%m/%d/', verbose_name='User avatar', blank=False,
                               default='photos/default_user_avatar.png',
                               help_text=_('Only .png format. Less than 0.5mb.'))
    bio = models.TextField(blank=True, max_length=500, verbose_name=_('information'))
    first_name = models.CharField(max_length=60, blank=True, null=True)
    last_name = models.CharField(max_length=60, blank=True, null=True)
    email = models.EmailField(max_length=100, blank=True, null=True)
    karma = models.BigIntegerField(verbose_name="Total karma", default=0)

    def save(self, *args, **kwargs):
        super().save()
        img = Image.open(self.avatar.path)
        # resize image
        if img.height > 300 or img.width > 300:
            output_size = (300, 300)
            img.thumbnail(output_size)
            img.save(self.avatar.path)


class Category(models.Model):
    title = models.CharField(max_length=255, unique=True)
    photo = models.ImageField(upload_to='photos/categories/%Y/%m/%d/', verbose_name='Photo for category', blank=True,
                              null=True)
    slug = models.SlugField(max_length=255, verbose_name='Url', unique=True)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('category', kwargs={"slug": self.slug})

    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'
        ordering = ['title']

    def save(self, *args, **kwargs):
        created = not self.pk
        super().save(*args, **kwargs)
        if not self.slug:
            self.slug = slugify(self.title)
        if created:
            Tag.objects.create(title=str(self.title).lower(), slug=self.slug)


class Tag(models.Model):
    title = models.CharField(max_length=50, unique=True)
    slug = models.SlugField(max_length=50, verbose_name='Url', unique=True)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('tag', kwargs={"slug": self.slug})

    class Meta:
        verbose_name = 'Tag'
        verbose_name_plural = 'Tags'
        ordering = ['title']

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.title = str(self.title).lower()
        if not self.slug:
            self.slug = slugify(self.title)


class Post(models.Model):
    class AttrStatus(models.TextChoices):
        APPROVED = 'APPROVED'
        DELETED = 'DELETED'

    title = models.CharField(max_length=150, verbose_name='Title')
    slug = models.SlugField(max_length=255, verbose_name='Url', unique=True)
    author = models.ForeignKey(User, on_delete=models.DO_NOTHING, verbose_name='Author')
    content = models.TextField(blank=True, verbose_name='Content')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Publication date')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Updated')
    photo = models.ImageField(upload_to='photos/%Y/%m/%d/', verbose_name='Photo', blank=True,
                              default='photos/default_blog_image.jpg')
    is_published = models.BooleanField(default=True, verbose_name='Published')
    category = models.ForeignKey('Category', on_delete=models.PROTECT, verbose_name='Category')
    tags = models.ManyToManyField(Tag, blank=True, related_name='posts')
    views = models.IntegerField(default=0)
    status = models.CharField(max_length=15, choices=AttrStatus.choices,
                              default=AttrStatus.APPROVED,
                              verbose_name=_('Status'))
    likes = models.PositiveBigIntegerField(default=0)
    dislikes = models.PositiveBigIntegerField(default=0)
    rating = models.IntegerField(default=0)
    link = models.URLField(max_length=200, unique=True, blank=True, null=True, default=None,
                           verbose_name=_('Instagram link'))

    def get_absolute_url(self):
        return reverse('post', kwargs={"slug": self.slug})

    def get_absolute_author_url(self):
        return reverse('author', kwargs={"pk": self.author.pk})

    def __str__(self):
        return f"{self.title}, {self.author}, {self.category}, {self.slug}, {self.tags}"

    class Meta:
        verbose_name = 'Post'
        verbose_name_plural = 'Posts'
        ordering = ['-created_at']

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        return super().save(*args, **kwargs)

    def set_like_or_dislike(self, is_like: bool = False, is_dislike: bool = False) -> None:
        if is_like:
            self.likes += 1
            self.rating += 1
        elif is_dislike:
            self.dislikes += 1
            self.rating -= 1
        self.save()


class Comment(MPTTModel):
    class AttrStatus(models.TextChoices):
        VISIBLE = 'VISIBLE'
        INVISIBLE = 'INVISIBLE'
        DELETED = 'DELETED'

    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    user_submitter = models.ForeignKey(User, on_delete=models.DO_NOTHING, related_name='comment_user_submitter',
                                       verbose_name=_('User submitter'))
    text = models.TextField(max_length=250, verbose_name=_('Comment text'))
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_('Date of creation'))
    parent = TreeForeignKey('self', blank=True, null=True, on_delete=models.CASCADE,
                            verbose_name='Parent comment', related_name='child')
    status = models.CharField(max_length=15, choices=AttrStatus.choices,
                              default=AttrStatus.VISIBLE,
                              verbose_name='Status')
    rating = models.IntegerField(default=0, verbose_name=_('Rating'))
    count_of_likes = models.PositiveIntegerField(default=0, verbose_name='Count of likes')
    count_of_dislikes = models.PositiveIntegerField(default=0, verbose_name='Count of dislikes')

    class MPTTMeta:
        order_insertion_by = ['created_at']

    class Meta:
        verbose_name = _('Comment')
        verbose_name_plural = _('Comments')
        ordering = ['created_at']

    def __str__(self):
        return self.text

    def set_like_or_dislike(self, is_like: bool = False, is_dislike: bool = False) -> None:
        if is_like:
            self.count_of_likes += 1
            self.rating += 1
        elif is_dislike:
            self.count_of_dislikes += 1
            self.rating -= 1
        self.save()

    def hide_comment(self) -> None:
        if self.status != self.AttrStatus.INVISIBLE:
            self.status = self.AttrStatus.INVISIBLE
            self.save()

    def delete_comment(self) -> None:
        if self.status != self.AttrStatus.DELETED:
            self.status = self.AttrStatus.DELETED
            self.save()


class Favorites(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='%(class)s',
                             verbose_name=_('User'))

    class Meta:
        abstract = True

    @classmethod
    def add_or_delete_favorite(cls, user, obj):
        raise NotImplementedError('You must specify add_or_delete_favorite method')


class FavoritePost(Favorites):
    obj = models.ForeignKey(Post, on_delete=models.CASCADE, verbose_name=_('Post'))

    def __str__(self):
        return f'User:{self.user}, Favorite Post:{self.obj}'

    @classmethod
    def add_or_delete_favorite(cls, user, obj):
        favorite, created = cls.objects.get_or_create(user=user, obj_id=obj.pk)
        if not created:
            favorite.delete()


class FavoriteCategory(Favorites):
    obj = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name=_('Category'))

    def __str__(self):
        return f'User:{self.user}, Favorite Category:{self.obj}'

    @classmethod
    def add_or_delete_favorite(cls, user, obj):
        favorite, created = cls.objects.get_or_create(user=user, obj_id=obj.pk)
        if not created:
            favorite.delete()


class NewsType(models.Model):
    type_of_news: str = models.CharField(max_length=100, verbose_name=_('News type'))

    class Meta:
        verbose_name = _('News Type')
        verbose_name_plural = _('News Types')

    def __str__(self):
        return f'{self.type_of_news}'


class Newsletter(models.Model):
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING, related_name='user_newsletter_subscriber', null=True,
                             blank=True, verbose_name=_('User'))
    is_subscribed = models.BooleanField(default=False, verbose_name='Is user subscribed?')
    email = models.EmailField(max_length=150, unique=True, null=True)
    choices = models.ManyToManyField(NewsType, blank=True, verbose_name=_('News choice'))
    date = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = _('Newsletter')
        verbose_name_plural = _('Newsletters')

    def __str__(self):
        return f'User:{self.user}, Email: {self.email}, Subscribed: {self.is_subscribed}, Type of news: {self.choices}'


class ActionTrack(models.Model):
    class AttrUserStatus(models.TextChoices):
        POST_PUBLISHER = 'Post publisher'
        JUST_USER = 'Just user'
        STAFF = 'Staff'
        ANONYMOUS = 'Anonymous'

    class AttrPage(models.TextChoices):
        # Reviews

        # Main pages
        PAGE_INDEX = 'Main(Index) page'
        PAGE_COMMUNITY = 'Community page'

        # Form pages
        POST_PROFILE = 'Post profile(with comments) page'
        POST_SUBMIT = 'Post submit page'

        # Profile pages
        USER_PROFILE = 'User profile page'
        USER_PROFILE_SUMMARY = 'User profile summary page'
        USER_PROFILE_PUBLICATIONS = 'User profile publications page'
        USER_PROFILE_PLATFORM = 'User profile platform page'
        LOGIN = 'Login page'
        REGISTRATION = 'Registration page'
        RESET_PASSWORD = 'Password reset view'
        CHANGE_PASSWORD = 'Password change view'

        # Other
        API_POST = 'Post API'
        API_COMMENT_RATING = 'Comment API rating'
        POST_DELETED = 'Post status -> DELETED'
        API_FAVORITE = 'Favorite API'
        API_LIKE_DISLIKE = 'Like/Dislike API'
        KARMA = 'Karma'

    class AttrAction(models.TextChoices):
        VIEW = 'View'  # using into CBV
        GO_TO = 'Redirect'
        GET_OBJECT = 'Get object'

        SUBMIT_POST = 'Submit post'

        POST_VIEW = 'View post'
        POST_RATING_PLUS = 'Post rating plus 1'
        POST_RATING_MINUS = 'Post rating minus 1'

        COMMENT_RATING_PLUS = 'Comment rating liked'
        COMMENT_RATING_MINUS = 'Comment rating disliked'
        CREATE_NEW_CHILD_COMMENT = 'Create new child comment'

    class AttrReason(models.TextChoices):
        OBJECT_NOT_EXIST = 'Object not exist'
        HAVENT_PERMISSIONS = 'Haven\'t permissions'
        OBJECT_STATUS_ONLY_OWNER = 'Only owner can view (Object status) status'
        FORM_INVALID = 'Form invalid'

        OBJECT_SUBMIT_SPAM = 'Object submit spam'

        POST_ALREADY_VIEWED = 'Coupon views change unsuccessfully. Already viewed'
        POST_RATING_ALREADY_CHANGED = 'Coupon rating change unsuccessfully. Already changed'

        COMMENT_RATING_ALREADY_CHANGED = 'Comment rating change unsuccessfully. Already changed'

    date = models.DateTimeField(auto_now_add=True, verbose_name=_('Date of action'))
    ip = models.GenericIPAddressField(protocol='both', unpack_ipv4=True, null=True, blank=None,
                                      validators=[validate_ipv46_address], verbose_name=_('Ip'))
    user = models.ForeignKey(User, null=True, default=None, on_delete=models.SET_NULL, related_name='User',
                             verbose_name=_('User'))
    user_status = models.CharField(max_length=40, choices=AttrUserStatus.choices, verbose_name=_('User status'))
    page = models.CharField(max_length=100, choices=AttrPage.choices, verbose_name=_('Page'))
    page_url = models.URLField(max_length=500, verbose_name=_('Page URL'))
    action = models.CharField(max_length=100, choices=AttrAction.choices, verbose_name=_('Action'))
    action_reason = models.CharField(max_length=100, null=True, choices=AttrReason.choices, verbose_name=_('Reason'))
    details = models.TextField(null=True, blank=True, verbose_name=_('Details'))

    http_referer = models.TextField(null=True, verbose_name=_('Referer'))
    session_key = models.TextField(null=True, verbose_name=_('Session key'))
    user_agent = models.TextField(null=True, verbose_name=_('User agent'))

    def __str__(self):
        return f'Action id:{self.pk}, at: {self.date}, user_status={self.user_status}, {self.action} on {self.page},' \
               f' reason={self.action_reason}, ' \
               f'details={self.details}'

    def save(self, *args, **kwargs):
        super(ActionTrack, self).save(*args, **kwargs)
