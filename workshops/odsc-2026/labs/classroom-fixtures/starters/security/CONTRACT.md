This is a local teaching service, not a web server. Treat user, owner, title, doc_id and name as untrusted.
search must return only exact-title matches owned by owner. Treat SQL punctuation literally.
read_doc returns (title,) only for a matching owner and id, otherwise None.
read_export accepts relative paths resolving to files inside root, including nested files and internal symlinks. Absolute names and any resolved path outside root must raise PermissionError. External symlinks must be denied. Assume no concurrent filesystem changes.
safe_lookup is already parameterized. verify_signature uses a trusted key and hex string signature; its inputs have the documented types. Neither is a planted vulnerability. Denial of service and changing the trust assumptions are out of scope.
Preserve signatures and valid behavior; use only Python standard library. Do not introduce a network service.
