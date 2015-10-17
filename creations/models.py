import re

from django.core.urlresolvers import reverse
from django.db import models

from taggit.managers import TaggableManager
from private_media.storages import PrivateMediaStorage

from forthebirds.settings import MARKDOWN_PROMPT
from birds.models import Species
from utils.models import RealInstanceProvider


class Creation(models.Model, RealInstanceProvider):
    title = models.CharField(max_length=120)
    description = models.TextField(blank=True, help_text=MARKDOWN_PROMPT)
    species = models.ManyToManyField(Species, blank=True)
    tags = TaggableManager(blank=True)
    is_public = True
    is_image = False

    def is_research(self):
        class_name = self.__class__.__name__
        if class_name.lower() == 'research':
            return True
        else:
            return False

    def get_ancestors(self):
        ancestors = []

        if hasattr(self, 'category'):
            current = self.category
            ancestors.append(current)
            while current.parent:
                current = current.parent
                ancestors.append(current)

        else:
            class_name = self.__class__.__name__
            words = re.findall('[A-Z][^A-Z]*', class_name)
            ancestors.append(' '.join(words))

        ancestors.reverse()
        return ancestors

    def __unicode__(self):
        return self.title

    def get_absolute_url(self):
        return None

    def get_display_date(self):
        if hasattr(self, 'date_published'):
            return self.date_published
        else:
            return None


class RadioProgram(Creation):
    original_air_date = models.DateField(null=True, blank=True)
    file = models.FileField(null=True, blank=True, upload_to='radio')
    supplemental_content_url = models.URLField(blank=True)
    transcript = models.TextField(blank=True,
                                  help_text=MARKDOWN_PROMPT)

    class Meta:
        ordering = ['-original_air_date']

    def __unicode__(self):
        return 'Radio Program: ' + self.title

    def get_absolute_url(self):
        return reverse('creations.views.radio_program',
                       kwargs={'id': self.id})

    def get_display_date(self):
        return self.original_air_date


class Book(Creation):
    purchase_url = models.CharField(max_length=500, blank=True)
    photo = models.ImageField(null=True, blank=True, upload_to='books')
    publisher = models.CharField(max_length=100, blank=True)
    isbn_10 = models.CharField('ISBN 10', max_length=20, blank=True)
    isbn_13 = models.CharField('ISBN 13', max_length=20, blank=True)
    date_published = models.DateField(null=True, blank=True)

    class Meta:
        ordering = ['-date_published']

    def get_absolute_url(self):
        return reverse('creations.views.book', kwargs={'id': self.id})

    def __unicode__(self):
        return 'Book: ' + self.title


class Article(Creation):
    published_by = models.CharField(max_length=100, blank=True)
    date_published = models.DateField(null=True, blank=True)
    url = models.URLField(blank=True)
    file = models.FileField(null=True, blank=True, upload_to='articles')
    text = models.TextField(blank=True, help_text=MARKDOWN_PROMPT)

    class Meta:
        ordering = ['-date_published']

    def get_absolute_url(self):
        return reverse('creations.views.article', kwargs={'id': self.id})

    def __unicode__(self):
        return 'Article: ' + self.title


class SpeakingProgram(Creation):
    class Meta:
        ordering = ['title']

    def get_absolute_url(self):
        return reverse('creations.views.speaking_program',
                       kwargs={'id': self.id})

    def __unicode__(self):
        return 'Speaking Program: ' + self.title


class SpeakingPresentation(models.Model):
    program = models.ForeignKey(SpeakingProgram)
    title = models.CharField(max_length=120)
    date = models.DateField(null=True, blank=True)
    description = models.TextField(blank=True, help_text=MARKDOWN_PROMPT)
    file = models.FileField(null=True, blank=True,
                            upload_to='presentations',
                            storage=PrivateMediaStorage())

    def __unicode__(self):
        return 'Speaking Presentation File: ' + self.title


class BlogPost(Creation):
    url = models.URLField(blank=True)

    class Meta:
        ordering = ['title']

    def get_absolute_url(self):
        return self.url

    def __unicode__(self):
        return 'Blog Post: ' + self.title


class WebPage(Creation):
    slug = models.SlugField(max_length=255)
    date_published = models.DateField(null=True, blank=True)
    content = models.TextField(blank=True, help_text=MARKDOWN_PROMPT)

    class Meta:
        ordering = ['title']

    def get_absolute_url(self):
        return reverse('creations.views.webpage', kwargs={'slug': self.slug})

    def __unicode__(self):
        return 'Web Page: ' + self.title


class ExternalProject(Creation):
    url = models.URLField(blank=True)

    class Meta:
        ordering = ['title']

    def get_absolute_url(self):
        return self.url

    def __unicode__(self):
        return 'External Project: ' + self.title


class ResearchCategory(models.Model):
    name = models.CharField(max_length=100)
    notes = models.TextField(blank=True, help_text=MARKDOWN_PROMPT)
    parent = models.ForeignKey('self', null=True, blank=True)

    class Meta:
        ordering = ['name']
        verbose_name_plural = 'research categories'

    def __unicode__(self):
        return self.name


class Research(Creation):
    category = models.ForeignKey(ResearchCategory)
    date = models.DateField(null=True, blank=True)
    attribution = models.CharField(max_length=200, blank=True,
                                   help_text=MARKDOWN_PROMPT)
    url = models.URLField(blank=True)
    file = models.FileField(null=True, blank=True, upload_to='research')
    text = models.TextField(blank=True, help_text=MARKDOWN_PROMPT)
    is_public = models.BooleanField(default=False)

    class Meta:
        ordering = ['-date']
        verbose_name_plural = 'Research'

    def get_absolute_url(self):
        return reverse('creations.views.research', kwargs={'id': self.id})

    def __unicode__(self):
        return 'Research: ' + self.title


class ABAFieldGuideImage(Creation):
    image = models.ImageField(null=True, blank=True, upload_to='abafieldguide')
    is_public = False
    is_image = True

    class Meta:
        ordering = ['title']
        verbose_name = 'ABA Field Guide Image'
        verbose_name = 'ABA Field Guide Images'

    def __unicode__(self):
        return 'ABA Field Guide Image ' + self.title

    def get_absolute_url(self):
        return self.image.url
