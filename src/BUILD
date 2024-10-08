py_library(
    name = "spacex_lib",
    srcs = ["spacex.py"],
    deps = [
        ":github_lib",
        ":logger_lib",
    ],
    visibility = ["//visibility:public"],  # Make this library visible to all targets
)

py_library(
    name = "github_lib",
    srcs = ["github.py"],
    visibility = ["//visibility:public"],  # Add visibility rule
)

py_library(
    name = "logger_lib",
    srcs = ["logger.py"],
    visibility = ["//visibility:public"],  # Add visibility rule
)
