package guardrail

default allow = false

# Allow ready_file globally
allow if {
    input.tool == "read_file"
}

# Allow list_dir globally
allow if {
    input.tool == "list_dir"
}

# Allow delete_file only if path starts with /tmp/
allow if {
    input.tool == "delete_file"
    startswith(input.args.path, "/tmp/")
}

# Deny otherwise (implicit)
