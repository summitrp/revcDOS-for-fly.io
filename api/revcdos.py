import os
from pathlib import Path
from fastapi import APIRouter, Response

api = APIRouter()

PACKED_FILE = Path(__file__).parent.parent / "revcdos.bin"

@api.get("/revcdos")
def get_revcdos():
    if not PACKED_FILE.exists():
        return {"error": "Packed file not found"}
    return Response(
        content=PACKED_FILE.read_bytes(),
        media_type="application/octet-stream"
    )
