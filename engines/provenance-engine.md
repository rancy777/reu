# Provenance Engine

Every artifact/log/claim should be traceable:
case_id → input hash → tool/version → command/config (when safe to disclose) → environment → output → analyst inference → source.

Do not mutate the original sample. Derived artifacts receive new hashes and parent links.
