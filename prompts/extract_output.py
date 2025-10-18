
from llama_index.core.prompts import RichPromptTemplate
# from ..pydantics.structured_output.base import BaseModel
from base import BasePrompt

class ExtractorPrompt(BasePrompt):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.prompt_tmplt = """\
            You are an agent that extracts data from a {{doc_type}} document.
            Do not use your prior knowlege, only the information you get from 
            the document.
            you are dealing with a '{{doc_class}}' document.
            """
            