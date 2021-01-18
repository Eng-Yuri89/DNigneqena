from haystack import indexes

from catalog.models.models import Product


class ProductIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)
    title = indexes.CharField(model_attr='title')
    keywords = indexes.CharField(model_attr='keywords')
    price = indexes.CharField()
    content_auto = indexes.EdgeNgramField(model_attr='slug')
    photo_url = indexes.CharField()
    url = indexes.CharField()

    def prepare_photo_url(self, obj):
        return obj.image_field.path

    def prepare_price(self, obj):
        return obj.price

    def get_model(self):
        return Product

    def prepare_url(self, obj):
        return obj.id

    def index_queryset(self, using=None):
        """Used when the entire index for model is updated."""
        return self.get_model().objects.all()
