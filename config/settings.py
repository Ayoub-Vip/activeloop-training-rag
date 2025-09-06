from pathlib import Path
from dataclasses import dataclass, field


@dataclass
class ParserParams:
	chunks_size: int = 512
	chunks_ovelap: int = 48
