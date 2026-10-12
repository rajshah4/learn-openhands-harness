# Decision 001: resumable exports
Status: superseded by decision 002. This workshop history is simulated.

Our catalog already offers one-based page-number browsing. A background report
needs to resume an export without knowing its page number. Implement export
windows in toyapp/export_cursor.py. Return a frozen ExportWindow containing
records and resume_token. The token is a decimal zero-based offset. Consumers
import export_window from that module. Do not replace direct catalog browsing.
A unit test for the export module is sufficient for this first isolated caller.
See the supplied v1 source snapshot in docs/history/v1-export_cursor.py.
