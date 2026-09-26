# Module: files

File and resource classes: upload, dangerous processing, download authorization,
path/file handling, archive/parser issues.

ID:FILES-UPLOAD
WHEN:[file upload surface]
SURFACE:[upload endpoints, multipart fields, avatar/attachment/import]
OBSERVE:[extension/content-type enforcement; server storage; retrieval]
HYPOTHESIS:[unrestricted upload (type spoof) or unsafe processing on retrieval]
TEST:[benign non-malicious file variant (content vs extension vs declared type) with control]
ADAPT:[extension, MIME, magic bytes, double extension, path components]
CONFIRM:[server stores/executes/serves file inconsistent with validation, with control]
IMPACT:[rce_potential|stored_xss|data]
STOP:[no actual payload could execute; no webshell; benign marker only]
RELATED:[FILES-PROCESS,CLIENT-SXSS,INJ-CMD]

ID:FILES-PROCESS
WHEN:[uploaded content parsed/processed server-side]
SURFACE:[image/pdf/xml/archive parsing, import pipelines]
HYPOTHESIS:[dangerous processing (parser vulns: image/archive/xml, decompression, magic)]
TEST:[crafted benign parser-stressing variant vs control]
ADAPT:[parser type, magic bytes, recursion/size]
CONFIRM:[parser error/behavior difference attributable to input]
IMPACT:[rce_potential|availability|data]
STOP:[no payload delivery; avoid av. blowup]
RELATED:[FILES-UPLOAD,INJ-XML]

ID:FILES-DOWNLOAD
WHEN:[download/file access]
SURFACE:[download/export endpoints, signed URLs, ?file=, CDN paths]
HYPOTHESIS:[unauthorized access to files not owned]
TEST:[own file baseline → second controlled file reference]
ADAPT:[id/path/owner reference]
CONFIRM:[access to file you may not access, with control]
IMPACT:[data_read]
RELATED:[AUTHZ-BOLA,WEB-PATHTRAV]

ID:FILES-PATH
WHEN:[filename/path derived from input]
SURFACE:[download, save, temp filename, export, archive member selection]
HYPOTHESIS:[path traversal / insecure filename handling]
TEST:[controlled path component vs control]
ADAPT:[../, separators, encoding, absolute, symlink] 
CONFIRM:[path resolution outside intended dir, with control]
IMPACT:[data_read|write]
STOP:[read-only; no real-file overwrite]
RELATED:[WEB-PATHTRAV,INJ-OTHER]

ID:FILES-ARCHIVE
WHEN:[archive (zip/tar/rar) extracted]
SURFACE:[import/extract/expand features]
HYPOTHESIS:[zip-slip / archive path traversal / decompression bomb]
TEST:[benign archive with a safe marker path control]
ADAPT:[entry path, symlink entries, compression ratio]
CONFIRM:[entry written/expanded outside intended target or excessive, with control in a sandbox]
IMPACT:[arbitrary_write|availability]
STOP:[extract in a throwaway dir; no bomb]
RELATED:[FILES-PROCESS,WEB-PATHTRAV]