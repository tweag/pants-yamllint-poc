from yamllint import yamllint
from yamllint.target_types import YamlSourceTarget, YamlSourcesGeneratorTarget


def rules():
    return [*yamllint.rules()]


def target_types():
    return [YamlSourceTarget, YamlSourcesGeneratorTarget]
