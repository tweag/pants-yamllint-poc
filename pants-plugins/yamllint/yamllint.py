from pants.backend.python.subsystems.python_tool_base import PythonToolBase
from pants.backend.python.target_types import PythonSourceField, ConsoleScript
from pants.core.goals.lint import LintTargetsRequest, LintResult, LintResults
from pants.engine.rules import collect_rules, rule, Get, MultiGet
from pants.engine.fs import Digest, MergeDigests
from pants.engine.target import Dependencies, FieldSet
from pants.option.option_types import StrOption, SkipOption
from pants.util.logging import LogLevel
from pants.core.util_rules.source_files import SourceFiles, SourceFilesRequest
from pants.engine.process import FallibleProcessResult, Process
from pants.engine.unions import UnionRule
from pants.backend.python.util_rules.pex import (
    Pex,
    PexProcess,
    PexRequest,
    PexRequirements,
)
from pants.util.strutil import pluralize

from yamllint.target_types import YamlSourceField

from dataclasses import dataclass
from typing import Any

import logging

logger = logging.getLogger(__name__)


class Yamllint(PythonToolBase):
    name = "Yamllint"
    options_scope = "yamllint"
    help = "A linter for YAML files"

    default_version = "yamllint==1.28.0"
    default_extra_requirements = []
    default_main = ConsoleScript("yamllint")

    register_interpreter_constraints = True
    default_interpreter_constraints = ["CPython>=3.6"]

    config = StrOption(
        "--config",
        default=None,
        advanced=True,
        help="yamllint config file",
    )

    skip = SkipOption("lint")


@dataclass(frozen=True)
class YamllintFieldSet(FieldSet):
    required_fields = (YamlSourceField,)
    sources: YamlSourceField


class YamllintRequest(LintTargetsRequest):
    field_set_type = YamllintFieldSet
    tool_subsystem = Yamllint
    name = "yamllint"


@rule(desc="Lint using yamllint", level=LogLevel.DEBUG)
async def run_yamllint(request: YamllintRequest, yamllint: Yamllint) -> LintResults:
    if yamllint.skip:
        return LintResults([], linter_name=request.name)

    sources_get = Get(
        SourceFiles,
        SourceFilesRequest(
            (field_set.sources for field_set in request.field_sets),
            for_sources_types=(YamlSourceField,),
        ),
    )
    yamllint_bin_get = Get(Pex, PexRequest, yamllint.to_pex_request())

    sources, yamllint_bin = await MultiGet(sources_get, yamllint_bin_get)

    input_digest = await Get(
        Digest,
        MergeDigests(
            (
                sources.snapshot.digest,
                yamllint_bin.digest,
            )
        ),
    )

    process_result = await Get(
        FallibleProcessResult,
        PexProcess(
            yamllint_bin,
            argv=[*sources.snapshot.files],
            input_digest=input_digest,
            description=f"Run yamllint on {pluralize(len(request.field_sets), 'file')}.",
            level=LogLevel.DEBUG,
        ),
    )
    result = LintResult.from_fallible_process_result(process_result)

    return LintResults([result], linter_name=request.name)


def rules():
    return [*collect_rules(), UnionRule(LintTargetsRequest, YamllintRequest)]