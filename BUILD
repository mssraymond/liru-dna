py_binary(
    name = "run_liru",
    srcs = ["pg_ingest.py"],
    deps = [
        "//requirements.txt",
        "@rules_python//python:pip_import",
    ],
)

load("@my_deps//:requirements.bzl", "requirement")

py_test(
    name = "unit_tests",
    srcs = ["test.py"],
    args = ["--bazel"],
    data = [
        "secrets.yml",
        "test_output/test_result.txt",
    ],
    main = "test.py",
    deps = [
        "//src:spacex_lib",
        requirement("requests"),
        requirement("PyYAML"),
    ],
    python_version = "PY3",
    srcs_version = "PY3",
)

# docker_build(
#     name = "docker_image",
#     # Add Dockerfile or other instructions
#     dockerfile = "Dockerfile",
# )

# docker_run(
#     name = "postgres_container",
#     image = ":docker_image",
#     ports = ["5432:5432"],
# )