from dotenv import load_dotenv
from anthropic import Anthropic

load_dotenv()
claude_client = Anthropic()

async def process_pdf_statement(pdf_statement: bytes):
    pass