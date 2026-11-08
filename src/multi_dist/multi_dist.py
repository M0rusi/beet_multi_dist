# Copyright 2026 morusi
# SPDX-License-Identifier: MIT

from beet import Context, PluginOptions, configurable
from beet.contrib.autosave import Autosave
from pydantic import RootModel
from typing import Literal
import logging

logger = logging.getLogger(__name__)


class Distribution_Options(PluginOptions):
    directory: str | None = None
    zipped: bool = False
    compression: Literal['none', 'deflate', 'bzip2', 'lzma'] | None = None
    compression_level: int | None = None
    overwrite: bool = False


class Options(RootModel[dict[str, Distribution_Options]]):
    pass


@configurable(validator=Options)
def multi_dist(ctx: Context, opts: Options):
    def _handler(ctx: Context):
        for pack in filter(None, ctx.packs):
            for dist_name, dist_opts in opts.root.items():
                logger.info(f"build dist '{dist_name}'")

                dist_name = ctx.template.render_string(dist_name)

                output_directory = (
                    ctx.directory / dist_opts.directory
                    if dist_opts.directory is not None else
                    ctx.output_directory
                )
                if output_directory is None:
                    continue

                pack.save(
                    path=output_directory / dist_name,
                    zipped=dist_opts.zipped,
                    compression=dist_opts.compression,
                    compression_level=dist_opts.compression_level,
                    overwrite=dist_opts.overwrite
                )

    ctx.inject(Autosave).add_output(_handler)
