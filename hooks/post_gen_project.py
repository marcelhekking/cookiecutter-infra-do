file_content = """export DIGITALOCEAN_CONTEXT={{cookiecutter.do_context}}
export DO_PAT={{cookiecutter.do_pat}}
"""

envrc_file = ".envrc"

# Write the content to the `.envrc file` file
with open(envrc_file, "w") as file:
    file.write(file_content)

print(f"Created the file {envrc_file}")
