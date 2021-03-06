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
    CoderedWebPage
)
from wagtail.core.fields import StreamField
from coderedcms.blocks import LAYOUT_STREAMBLOCKS


class ArticlePage(CoderedArticlePage):
    """
    Article, suitable for news or blog content.
    """
    class Meta:
        verbose_name = 'Article'
        ordering = ['-first_published_at', ]

    # Customise the set of blocks available within body's StreamField
    body = StreamField(LAYOUT_STREAMBLOCKS, null=True, blank=True)
    
    # Only allow this page to be created beneath an ArticleIndexPage.
    parent_page_types = ['apptheme_codered.ArticleIndexPage']

    template = 'coderedcms/pages/article_page.html'
    amp_template = 'coderedcms/pages/article_page.amp.html'
    search_template = 'coderedcms/pages/article_page.search.html'
    search_db_include = True


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
    search_db_include = True


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
    search_db_include = True

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