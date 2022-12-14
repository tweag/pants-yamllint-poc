# Copyright 2022 Pants project contributors (see CONTRIBUTORS.md).
# Licensed under the Apache License, Version 2.0 (see LICENSE).
from yamllint.rules import rules as yamllint_rules
from yamllint.target_types import YamlSourcesGeneratorTarget, YamlSourceTarget


def rules():
    return [*yamllint_rules()]


def target_types():
    return [YamlSourceTarget, YamlSourcesGeneratorTarget]
