# coding: utf-8
from __future__ import absolute_import, unicode_literals
from django.utils.safestring import mark_safe
from django_tables2.utils import AttributeDict
import warnings
from .base import Column, library


@library.register
class EditableColumn(Column):
    """
    A subclass of `.Column` that renders as a contenteditable input.

    This class implements some sensible defaults:

    - HTML input's ``name`` attribute is the :term:`column name` (can override
      via *attrs* argument).
    - *orderable* defaults to `False`.

    .. note::

    I think doing it this way means you will need ajax/ahah something similar to save the resulting data to your db.

    In addition to *attrs* keys supported by `.Column`, the following are
    available:

    - *input*     -- ``<input>`` elements in both ``<td>`` and ``<th>``.
    - *th__input* -- Replaces *input* attrs in header cells.
    - *td__input* -- Replaces *input* attrs in body cells.
    """
    def __init__(self, attrs=None, **extra):
        # For backwards compatibility, passing in a normal dict effectively
        # should assign attributes to the `<input>` tag.
        valid = set(("input", "th__input", "td__input", "th", "td", "cell"))
        if attrs and not set(attrs) & set(valid):
            # if none of the keys in attrs are actually valid, assume it's some
            # old code that should be be interpreted as {"td__input": ...}
            warnings.warn('attrs keys must be one of %s, interpreting as {"td__input": %s}'
                          % (', '.join(valid), attrs), DeprecationWarning)
            attrs = {"td__input": attrs}
        # This is done for backwards compatible too, there used to be a
        # ``header_attrs`` argument, but this has been deprecated. We'll
        # maintain it for a while by translating it into ``head.checkbox``.
        if "header_attrs" in extra:
            warnings.warn('header_attrs argument is deprecated, '
                          'use attrs={"th__input": ...} instead',
                          DeprecationWarning)
            attrs.setdefault('th__input', {}).update(extra.pop('header_attrs'))

        kwargs = {'orderable': False, 'attrs': attrs}
        kwargs.update(extra)
        super(EditableColumn, self).__init__(**kwargs)

    # @property
    # def header(self):
    #     """ May want to get rid of this, don't actually want the header to be the same type as the column contents.
    #     :return:
    #     """
    #     default = {'type': 'contenteditable'}
    #     general = self.attrs.get('input')
    #     specific = self.attrs.get('th__input')
    #     attrs = AttributeDict(default, **(specific or general or {}))
    #     return mark_safe('<input %s/>' % attrs.as_html())

    def render(self, value, bound_column):  # pylint: disable=W0221
        default = {
            'type': 'contenteditable',
            'name': bound_column.name,
            'value': value
        }
        general = self.attrs.get('input')
        specific = self.attrs.get('td__input')
        attrs = AttributeDict(default, **(specific or general or {}))
        return mark_safe('<input %s/>' % attrs.as_html())
