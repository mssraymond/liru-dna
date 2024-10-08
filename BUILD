# Define a python_binary rule for running your Python scripts
py_binary(
    name = "run_liru",
    srcs = ["pg_ingest.py"],  # adjust for your script location
    deps = [
        "@rules_python//python:pip_import",
        "//requirements.txt",
    ],
)

# Use docker rules to build and run Docker containers
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

py_test(
    name = "unit_tests",
    srcs = ["test.py"],
    main = "test.py",
    deps = [
        "//src:spacex_lib",
    ],
    data = ["secrets.yml", "test_output/test_result.txt"],
    args = ["--bazel"],
)
