from tree_sitter import Language

Language.build_library(
    # Store the library in the `build` directory
    "/home/han/github/LinuxLLM/tree-sitter/tree-sitter-c.so",
    # Include one or more languages
    ["/home/han/github/tree-sitter-c"],
)
