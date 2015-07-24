# coding: utf-8
# pylint: disable=W0611
from .tables  import Table
from .columns import (BooleanColumn, Column, CheckBoxColumn, DateColumn,
                      DateTimeColumn, EmailColumn, FileColumn, LinkColumn,
                      TemplateColumn, URLColumn, TimeColumn)
from .config  import RequestConfig
from .utils   import A, Attrs
try:
    from .views import SingleTableMixin, SingleTableView
except ImportError:
    pass

try:
   from .columns.editablecolumn import EditableColumn
except ImportError:
   print("still cannot import your new column type EditableColumn")


__version__ = "1.0.4"
