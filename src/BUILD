py_library(
    name = "spacex_lib",
    srcs = ["spacex.py"],
    visibility = ["//visibility:public"],  # Make this library visible to all targets
    deps = [
        ":github_lib",
        ":logger_lib",
    ],
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
