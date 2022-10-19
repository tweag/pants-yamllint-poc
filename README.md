# What is this?
A proof of concept plugin for the [`pants`](https://www.pantsbuild.org) build system to run [`yamllint`](https://github.com/adrienverge/yamllint) during a build.

# How?
Just add `yaml_source(source = '...')` or `yaml_sources()` rules to your `BUILD` files and run
```
./pants lint ::
```
to lint all files in the repository.

# What's missing?
- There are no `tailor` rules to make `pants` automatically add `yaml_sources()` rules.
- The plugin claims to support specifying a `yamllint` configuration file but actually doesn't yet.
- As a corollary, there is no autodiscovery of `yamllint` configuration yet.

# Who's to blame?
Viktor! But most of the code is very similar to the `shellcheck` linter in core `pants`.
