import dataclasses


@dataclasses.dataclass
class DocCustom:
    content: list[dict]
    media_type: str = ""
    type: str = "content"


@dataclasses.dataclass
class DocPdf:
    data: str  # base64 encode pdf data
    title: str
    media_type: str = "application/pdf"
    type: str = "base64"


@dataclasses.dataclass
class DocText:
    data: str  # plain text data
    title: str
    media_type: str = "text/plain"
    type: str = "text"
