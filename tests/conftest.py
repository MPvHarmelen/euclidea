import os
from hypothesis import settings

# settings.register_profile("default", deadline=500, max_shrinks=100)
# settings.register_profile("default", deadline=1000, max_shrinks=100)
# settings.register_profile("default", deadline=None, max_shrinks=100)
settings.register_profile("default", max_examples=50, deadline=None, max_shrinks=100)
# settings.register_profile("default", max_examples=50, deadline=200, max_shrinks=100)
settings.load_profile(os.getenv(u'HYPOTHESIS_PROFILE', 'default'))
