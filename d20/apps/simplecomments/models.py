from django.db import models
from django.conf import settings
from django.contrib.contenttypes import generic
from django.contrib.contenttypes.models import ContentType
from django.utils.translation import ugettext_lazy as _
from django.utils.encoding import force_text

PATH_SEPARATOR = getattr(settings, 'COMMENT_PATH_SEPARATOR', '/')
PATH_DIGITS = getattr(settings, 'COMMENT_PATH_DIGITS', 10)

class CommentManager(models.Manager):

    def for_model(self, model):
        """
        QuerySet for all comments for a particular model (either an instance or
        a class).
        """
        ct = ContentType.objects.get_for_model(model)
        qs = self.get_query_set().filter(content_type=ct)
        if isinstance(model, models.Model):
            qs = qs.filter(object_pk=force_text(model._get_pk_val()))
        return qs

class Comment(models.Model):

    # Content-object field
    content_type = models.ForeignKey(ContentType, verbose_name=_('content type'), related_name="content_type_set_for_%(class)s")
    object_pk = models.TextField(_('object ID'))
    content_object = generic.GenericForeignKey(ct_field="content_type", fk_field="object_pk")
    user = models.ForeignKey(settings.AUTH_USER_MODEL)
    comment = models.TextField(_('comment'))
    submit_date = models.DateTimeField(_('date/time submitted'), auto_now_add=True)
    parent = models.ForeignKey('self', null=True, blank=True, default=None, related_name='children', verbose_name='Parent')
    last_child = models.ForeignKey('self', null=True, blank=True, verbose_name="Last child")
    tree_path = models.TextField(_('Tree path'), editable=False, db_index=True)

    objects = CommentManager()

    @property
    def depth(self):
        return len(self.tree_path.split(PATH_SEPARATOR))

    @property
    def root_id(self):
        return int(self.tree_path.split(PATH_SEPARATOR)[0])

    @property
    def root_path(self):
        return Comment.objects.filter(pk__in=self.tree_path.split(PATH_SEPARATOR)[:-1])

    @property
    def name(self):
        return self.user.username
    
    def __str__(self):
        return "%s: %s..." % (self.name, self.comment[:50])

    def save(self, *args, **kwargs):
        skip_tree_path = kwargs.pop('skip_tree_path', False)
        super(Comment, self).save(*args, **kwargs)
        if skip_tree_path:
            return None

        tree_path = unicode(self.pk).zfill(PATH_DIGITS)
        if self.parent:
            tree_path = PATH_SEPARATOR.join((self.parent.tree_path, tree_path))

            self.parent.last_child = self
            Comment.objects.filter(pk=self.parent_id).update(last_child=self)

        self.tree_path = tree_path
        Comment.objects.filter(pk=self.pk).update(tree_path=self.tree_path)

    def delete(self, *args, **kwargs):
        # Fix last child on deletion.
        if self.parent_id:
            try:
                prev_child_id = Comment.objects \
                                .filter(parent=self.parent_id) \
                                .exclude(pk=self.pk) \
                                .order_by('-submit_date') \
                                .values_list('pk', flat=True)[0]
            except IndexError:
                prev_child_id = None
            Comment.objects.filter(pk=self.parent_id).update(last_child=prev_child_id)
        super(Comment, self).delete(*args, **kwargs)

    class Meta(object):
        ordering = ('tree_path',)
        db_table = 'comments_comment'
        verbose_name = _('Comment')
        verbose_name_plural = _('Comments')
