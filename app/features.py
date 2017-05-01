from app.ml.models.constants import *

class Feature(object):
  def __init__(self, name, func):
    self.name = name
    self.func = func

  def apply(self, event):
    return self.func(event)

FEATURES = [
  Feature(DESCRIPTION_LENGTH, lambda e: len(e.description) if e.description is not None else 0),
  Feature(HAS_PROFILE_PICTURE, lambda e: 1 if e.profile_picture is not None else 0),
  Feature(HAS_LINKS, lambda e: 1 if e.description is not None and "http://" in e.description.lower() else 0),
  Feature(HAS_CATEGORY, lambda e: 1 if e.category is not None else 0),
  Feature(HAS_COVER_PICTURE, lambda e: 1 if e.cover_picture is not None else 0),
  Feature(HAS_EMAIL, lambda e: 1 if e.description is not None and "@" in e.description.lower() else 0),
  Feature(HAS_FOOD, lambda e: 1 if e.description is not None and \
    e.name is not None and "food" in e.description.lower().split() or "food" in e.name.lower().split() else 0),
  Feature(IS_FREE, lambda e: 1 if e.description is not None and \
    e.name is not None and "free" in e.description.lower().split() or "free" in e.name.lower().split() else 0)
]
