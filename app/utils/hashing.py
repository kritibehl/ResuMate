import hashlib


def normalize_text(value: str) -> str:
    return " ".join(value.split()).strip().lower()


def compute_input_fingerprint(document_text: str, reference_text: str) -> str:
    normalized = f"{normalize_text(document_text)}||{normalize_text(reference_text)}"
    digest = hashlib.sha256(normalized.encode("utf-8")).hexdigest()
    return f"sha256:{digest}"
