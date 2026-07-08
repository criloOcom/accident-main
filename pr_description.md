🎯 **What:**
Fixed an insecure temporary file usage vulnerability (CWE-377) in `.dev/app/anonymize_doc.py`.

⚠️ **Risk:**
The script previously read from a hardcoded and predictable file path (`/tmp/original_assignation.txt`). This predictability exposes the system to symlink attacks, race conditions, and unauthorized data access/tampering by other local users on shared systems.

🛡️ **Solution:**
Refactored the script to accept the input file path as a command-line argument (`sys.argv[1]`) instead of hardcoding a predictable `/tmp` path. The script safely checks for the argument and exits with usage instructions if not provided. The `README.md` documentation has also been updated to reflect the new expected usage.
