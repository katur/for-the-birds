import urllib

from django.core.urlresolvers import reverse
from django.db import models

from forthebirds.settings import MARKDOWN_PROMPT
from utils.http import http_response_url


"""
TODO: Migrating to eBird.

Limit parsing of eBird file to CATEGORY='species'.

Re: species naming fields:

    - id should be CharField(20), from eBird.SPECIES_CODE
    - absolute_position => taxon_order; should be DecimalField, from
      eBird.TAXON_ORDER. Note: this is not unique!!!
    - scientific_name from eBird.SCI_NAME
    - common_name from eBird.PRIMARY_COM_NAME
    - possibly also take eBird.en_IOC, another common name
    - possibly also take eBird.REPORT_AS (not sure what it is yet)
    - delete french_name
    - calculate slug frmo new common_name

Re: ancestry fields:

    - delete TaxonomicLevel class, TaxonomicGroup class, and Species.parent
    - add field `order`, from eBird.ORDER1
    - add field `family`, from eBird.FAMILY split before '('
    - add field `family_common` from eBird.FAMILY split after ')'
    - note: SPECIES_GROUP probably need not be used (seems like just
      an indicator for the first line where a new family starts)
"""


class TaxonomicLevel(models.Model):
    name = models.CharField(max_length=20)
    depth = models.PositiveSmallIntegerField()

    def __unicode__(self):
        return self.name


class TaxonomicGroup(models.Model):
    name = models.CharField(max_length=30, unique=True)
    common_name = models.CharField(max_length=50, blank=True)
    level = models.ForeignKey(TaxonomicLevel)
    parent = models.ForeignKey('self', null=True, blank=True)
    relative_position = models.PositiveSmallIntegerField(null=True,
                                                         blank=True)

    class Meta:
        ordering = ['level__depth', 'relative_position']

    def __unicode__(self):
        return self.common_name if self.common_name else self.name


class Species(models.Model):
    id = models.PositiveIntegerField(primary_key=True)
    absolute_position = models.PositiveSmallIntegerField(
        'Taxonomic position', null=True, blank=True)
    scientific_name = models.CharField(max_length=50, unique=True)
    common_name = models.CharField(max_length=50)
    slug = models.SlugField(max_length=50, unique=True)
    french_name = models.CharField(max_length=50)
    parent = models.ForeignKey(TaxonomicGroup)
    is_visible = models.BooleanField('Visible on website', default=True)
    has_abc_bird_of_the_week_url = models.BooleanField(default=False)
    has_cornell_all_about_birds_url = models.BooleanField(default=False)
    blurb = models.TextField(blank=True, help_text=MARKDOWN_PROMPT)
    main_photo_url = models.URLField(blank=True)
    main_sound_recording = models.ForeignKey(
        'creations.SoundRecording', null=True, blank=True,
        related_name='species_with_main_recording')
    nacc_is_accidental = models.NullBooleanField()
    nacc_is_hawaiian = models.NullBooleanField()
    nacc_is_introduced = models.NullBooleanField()
    nacc_is_nonbreeding = models.NullBooleanField()
    nacc_is_extinct = models.NullBooleanField()
    nacc_is_misplaced = models.NullBooleanField()
    nacc_annotation = models.TextField(blank=True)

    class Meta:
        ordering = ['absolute_position']
        verbose_name_plural = 'bird species'

    def __unicode__(self):
        return self.common_name + ' (' + self.scientific_name + ')'

    def get_absolute_url(self):
        return reverse('bird_url', args=[self.slug])

    def get_ancestors(self):
        ancestors = []
        parent = self.parent

        while parent:
            ancestors.append(parent)
            parent = parent.parent

        return ancestors

    def get_ancestor(self, ancestor_level_name):
        for ancestor in self.get_ancestors():
            if ancestor.level.name == ancestor_level_name:
                return ancestor
        return None

    def get_order(self):
        return self.get_ancestor('order')

    def get_family(self):
        return self.get_ancestor('family')

    def get_subfamily(self):
        return self.get_ancestor('subfamily')

    def get_genus(self):
        return self.get_ancestor('genus')

    def get_abc_bird_of_the_week_url(self):
        url_name = self.common_name.replace(' ', '-')
        url_name = url_name.replace("'", '')
        return 'http://abcbirds.org/bird/{}/'.format(url_name)

    def get_resolved_abc_bird_of_the_week_url(self):
        return http_response_url(self.get_abc_bird_of_the_week_url())

    def get_cornell_all_about_birds_url(self):
        url_name = self.common_name.replace(' ', '_')
        url_name = url_name.replace("'", '')
        return 'http://www.allaboutbirds.org/guide/{}'.format(url_name)

    def get_resolved_cornell_all_about_birds_url(self):
        url = http_response_url(self.get_cornell_all_about_birds_url())
        if url and 'search' in url:
            url = None
        return url

    def get_flickr_search_url(self):
        url = 'https://www.flickr.com/search?'
        get_params = {
            'user_id': '48014585@N00',
            'sort': 'date-taken-desc',
            'text': self.common_name,
        }
        return url + urllib.urlencode(get_params)

    def get_nacc_statuses(self):
        statuses = []
        if self.nacc_is_accidental:
            statuses.append('Accidental')
        if self.nacc_is_hawaiian:
            statuses.append('Hawaiian')
        if self.nacc_is_introduced:
            statuses.append('Introduced')
        if self.nacc_is_nonbreeding:
            statuses.append('Non-breeding')
        if self.nacc_is_extinct:
            statuses.append('Extinct')
        if self.nacc_is_misplaced:
            statuses.append('Misplaced')
        return statuses

    def important_field_differs(self, other):
        return (
            self.scientific_name != other.scientific_name or
            self.parent != other.parent or
            self.common_name != other.common_name or
            self.nacc_is_accidental != other.nacc_is_accidental or
            self.nacc_is_hawaiian != other.nacc_is_hawaiian or
            self.nacc_is_introduced != other.nacc_is_introduced or
            self.nacc_is_nonbreeding != other.nacc_is_nonbreeding or
            self.nacc_is_extinct != other.nacc_is_extinct or
            self.nacc_is_misplaced != other.nacc_is_misplaced
        )

    def update_aou_fields(self, other):
        self.scientific_name = other.scientific_name
        self.parent = other.parent
        self.common_name = other.common_name
        self.french_name = other.french_name
        self.nacc_annotation = other.nacc_annotation
        self.nacc_is_accidental = other.nacc_is_accidental
        self.nacc_is_hawaiian = other.nacc_is_hawaiian
        self.nacc_is_introduced = other.nacc_is_introduced
        self.nacc_is_nonbreeding = other.nacc_is_nonbreeding
        self.nacc_is_extinct = other.nacc_is_extinct
        self.nacc_is_misplaced = other.nacc_is_misplaced


class MinnesotaSpecies(models.Model):
    species = models.OneToOneField(Species, primary_key=True)
    include_in_book = models.NullBooleanField(default=None)
    mou_status = models.CharField('MOU status', max_length=50, blank=True)
    mou_breeding_status = models.NullBooleanField('MOU breeding status',
                                                  default=None)
    mou_annotation = models.CharField('MOU annotation', max_length=500,
                                      blank=True)

    class Meta:
        ordering = ['species__absolute_position']
        verbose_name_plural = 'Minnesota species'

    def __unicode__(self):
        return str(self.species)
