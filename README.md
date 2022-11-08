# What is this?
A proof of concept plugin for the [`pants`](https://www.pantsbuild.org) build system to run [`yamllint`](https://github.com/adrienverge/yamllint) during a build.

# How?
Just add `yaml_source(source = '...')` or `yaml_sources()` rules to your `BUILD` files and run
```
./pants lint ::
```
to lint all files in the repository. Configuration for `yamllint` can be autodetected as `.yamllint`, `.yamllint.yaml` or `.yamllint.yaml` files or specified explicitly with the `config` key in `pants.toml`.

# What's missing?
- There are no `tailor` rules to make `pants` automatically add `yaml_sources()` rules.

# Who's to blame?
@vkleen! But most of the code is very similar to the `shellcheck` linter in core `pants`.
