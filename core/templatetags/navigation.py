from enum import Enum

from django import template
from django.conf import settings
from django.contrib.auth.models import User

register = template.Library()


class Database(Enum):
    SQLITE = "sqlite"
    MARIADB = "mariadb"
    UNKNOWN = "unknown"

    def __str__(self):
        return str(self.value)

    def __repr__(self):
        return str(self)


@register.inclusion_tag("core/tags/navigation.html", takes_context=True)
def navigation_header(context, user: User):
    # request = context["request"]
    return {"user": user, "dbtype": str(determine_database_type())}


def determine_database_type() -> Database:
    db_type = Database.UNKNOWN
    engine = settings.DATABASES["default"]["ENGINE"]
    if "sqlite" in engine:
        db_type = Database.SQLITE
    elif "mariadb" in engine:
        db_type = Database.MARIADB

    return db_type
