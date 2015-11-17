from haystack import indexes
from .models import CharacterSheet

class CharacterSheetIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)
    pub_date = indexes.DateTimeField(model_attr='created')

    def get_model(self):
        return CharacterSheet

    def index_queryset(self, using=None):
        #Used when the entire index for model is updated.
        return self.get_model().objects.filter(pub_date__lte=datetime.datetime.now())
