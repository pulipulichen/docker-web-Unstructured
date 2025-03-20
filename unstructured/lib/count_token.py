import tiktoken
import os

token_encoder = tiktoken.encoding_for_model(os.getenv('UNSTRUCTED_TOKEN_ENCODER_MODEL', 'gpt-4o-mini'))

def count_token(text):
  if isinstance(text, list):
    text = "\n\n".join(text)
    # print(text)

  token_length = len(token_encoder.encode(text))
  # print(token_length)
  return token_length