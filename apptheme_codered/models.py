"""
Createable pages used in CodeRed CMS.
"""
from modelcluster.fields import ParentalKey
from coderedcms.forms import CoderedFormField
from coderedcms.models import (
    CoderedArticlePage,
    CoderedArticleIndexPage,
    CoderedEmail,
    CoderedFormPage,
    CoderedWebPage,
    CoderedPage,
)
from coderedcms.blocks import CONTENT_STREAMBLOCKS, HTML_STREAMBLOCKS

from django.db import models
from datetime import datetime, timedelta, date
from wagtail.snippets.models import register_snippet
from django.utils.translation import ugettext_lazy as _
from wagtail.core.fields import StreamField
from coderedcms.blocks import LAYOUT_STREAMBLOCKS
from wagtail.admin.edit_handlers import (
    FieldPanel,
    MultiFieldPanel,
    StreamFieldPanel)
from wagtail.core.models import Page

class ArticlePage(CoderedArticlePage):
    """
    Article, suitable for news or blog content.
    """
    class Meta:
        verbose_name = 'Article'
        ordering = ['-first_published_at', ]

    # Only allow this page to be created beneath an ArticleIndexPage.
    parent_page_types = ['apptheme_codered.ArticleIndexPage']

    template = 'coderedcms/pages/article_page.html'
    amp_template = 'coderedcms/pages/article_page.amp.html'
    search_template = 'coderedcms/pages/article_page.search.html'


class ArticleIndexPage(CoderedArticleIndexPage):
    """
    Shows a list of article sub-pages.
    """
    class Meta:
        verbose_name = 'Article Landing Page'

    # Override to specify custom index ordering choice/default.
    index_query_pagemodel = 'apptheme_codered.ArticlePage'

    # Only allow ArticlePages beneath this page.
    subpage_types = ['apptheme_codered.ArticlePage']

    template = 'coderedcms/pages/article_index_page.html'


class FormPage(CoderedFormPage):
    """
    A page with an html <form>.
    """
    class Meta:
        verbose_name = 'Form'

    template = 'coderedcms/pages/form_page.html'


class FormPageField(CoderedFormField):
    """
    A field that links to a FormPage.
    """
    class Meta:
        ordering = ['sort_order']

    page = ParentalKey('FormPage', related_name='form_fields')


class FormConfirmEmail(CoderedEmail):
    """
    Sends a confirmation email after submitting a FormPage.
    """
    page = ParentalKey('FormPage', related_name='confirmation_emails')


class WebPage(CoderedWebPage):
    """
    General use page with featureful streamfield and SEO attributes.
    Template renders all Navbar and Footer snippets in existance.
    """
    class Meta:
        verbose_name = 'Web Page'

    template = 'coderedcms/pages/web_page.html'

# CEDA/JASMIN custom classes below

class NewsClientPage(CoderedWebPage):
    """
    Page which acts as client to external feeds
    """
    class Meta:
        verbose_name = 'News client page'

class EventsClientPage(CoderedWebPage):
    """
    Page which acts as client to external feeds
    """
    class Meta:
        verbose_name = 'Events client page'

class CustomWebPage(CoderedWebPage):
    """
    Custom web page with alert for use as home page
    """
    class Meta:
        verbose_name = 'Custom web page'

    alert_message = StreamField(
        HTML_STREAMBLOCKS,
        null=True,
        blank=True,
        verbose_name=_('Alert message')
    )
    alert_level_choices = (
        ('alert-info', _('Default level')),
        ('alert-primary', _('primary')),
        ('alert-secondary', _('secondary')),
        ('alert-success', _('success')),
        ('alert-danger', _('danger')),
        ('alert-warning', _('warning')),
        ('alert-info', _('info')),
        ('alert-light', _('light')),
        ('alert-dark', _('dark')),
    )
    alert_level = models.CharField(
        default='',
        blank=True,
        max_length=255,
        verbose_name=_('Alert level'),
        choices=alert_level_choices,
        help_text=_('Level of alert (corresponds to Bootstrap css styles)')
    )
    alert_display_from = models.DateField(
        null=True,
        blank=True,
        default=date.today,
        verbose_name=_('Date alert is visible from'),
    )
    alert_display_to = models.DateField(
        null=True,
        blank=True,
        default=date.today,
        verbose_name=_('Display alert is visible to'),
    )

    @property
    def alert_is_current(self):
        today = date.today()
        if ( self.alert_display_from <= today <= self.alert_display_to ): 
            return True
        else:
            return False

    content_panels = CoderedWebPage.content_panels + [
        StreamFieldPanel('alert_message'),
        MultiFieldPanel(
            [
                FieldPanel('alert_display_from'),
                FieldPanel('alert_display_to'),
                FieldPanel('alert_level'),
            ],
        )
    ]