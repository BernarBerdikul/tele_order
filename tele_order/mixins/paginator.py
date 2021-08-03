from django.core.paginator import Paginator
from django.utils.functional import cached_property
from django.db import connection
import logging

OBJECTS_PER_PAGE_IN_ADMIN = 100


class LargeTablePaginator(Paginator):
    """ Default paginator for admin page """
    @cached_property
    def count(self):
        query = self.object_list.query
        if not query.where:
            try:
                cursor = connection.cursor()
                cursor.execute(
                    'SELECT reltuples FROM pg_class WHERE relname = %s',
                    [query.model._meta.db_table]
                )
                return int(cursor.fetchone()[0])
            except Exception as e:  # noqa
                logging.warning(e)

        return super().count
