from model_mommy import mommy
from model_mommy.random_gen import gen_string
from ..fields import TextFieldTranslatable
from ..fields import CharFieldTranslatable

mommy.generators.add(TextFieldTranslatable, gen_string)
mommy.generators.add(CharFieldTranslatable, gen_string)
