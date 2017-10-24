from model_mommy import mommy
from model_mommy.random_gen import gen_string

from .fields import CharFieldTranslatable
from .fields import TextFieldTranslatable

mommy.generators.add(TextFieldTranslatable, gen_string)
mommy.generators.add(CharFieldTranslatable, gen_string)
