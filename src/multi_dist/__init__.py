from .multi_dist import multi_dist
from beet import Context


def beet_default(ctx: Context):
    ctx.require(multi_dist)
