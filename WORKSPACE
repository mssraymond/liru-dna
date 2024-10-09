load("@bazel_tools//tools/build_defs/repo:http.bzl", "http_archive")

http_archive(
    name = "rules_python",
    sha256 = "5868e73107a8e85d8f323806e60cad7283f34b32163ea6ff1020cf27abef6036",
    strip_prefix = "rules_python-0.25.0",
    url = "https://github.com/bazelbuild/rules_python/releases/download/0.25.0/rules_python-0.25.0.tar.gz",
)

load("@rules_python//python:repositories.bzl", "py_repositories", "python_register_toolchains")

py_repositories()

python_register_toolchains(
    name = "python3_9",
    python_version = "3.9",
)

load("@python3_9//:defs.bzl", "interpreter")  # @unused

load("@rules_python//python:pip.bzl", "pip_parse")

pip_parse(
    name = "my_deps",
    requirements_lock = "//:requirements.txt",
)

load("@my_deps//:requirements.bzl", "install_deps")
install_deps()

# http_archive(
#     name = "io_bazel_rules_docker",
#     urls = ["https://github.com/bazelbuild/rules_docker/archive/v0.17.0.tar.gz"],
#     strip_prefix = "rules_docker-0.17.0",
# )