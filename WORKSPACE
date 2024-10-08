# Define external repositories
load("@bazel_tools//tools/build_defs/repo:http.bzl", "http_archive")

# Example to pull Python dependencies
http_archive(
    name = "rules_python",
    url = "https://github.com/bazelbuild/rules_python/releases/download/0.2.0/rules_python-0.2.0.tar.gz",
    sha256 = "a12345..."
)

# Load docker rules for Bazel if you use Docker.
http_archive(
    name = "io_bazel_rules_docker",
    urls = ["https://github.com/bazelbuild/rules_docker/archive/v0.17.0.tar.gz"],
    strip_prefix = "rules_docker-0.17.0",
)
