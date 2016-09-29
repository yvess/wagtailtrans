import factory

from wagtailtrans import models
from tests.factories import language


class TranslatedPageFactory(factory.DjangoModelFactory):
    language = factory.SubFactory(language.LanguageFactory)
    title = 'Foo Bar'
    depth = 0
    path = 'home/one'

    class Meta:
        model = models.TranslatedPage

    @classmethod
    def _create(cls, *args, **kwargs):
        try:
            return models.TranslatedPage.objects.get(title=kwargs['title'])
        except models.TranslatedPage.DoesNotExist:
            if kwargs['depth'] == 0:
                return args[0].add_root(**kwargs)
            else:
                raise NotImplementedError()


def create_page_tree(*items):
    """Shortcut to create a page tree 3 levels deep"""
    if not items:
        items = ['english homepage', 'subpage1', 'subpage2']

    rootpage = TranslatedPageFactory(title=items[0])
    for item in items[1:]:
        rootpage = rootpage.add_child(title=item)
    return rootpage