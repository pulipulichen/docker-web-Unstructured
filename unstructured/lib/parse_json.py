
import json

def parse_json(metadata):
  parsed_json = {}

  # ======================
  # Parse metadata JSON if provided
  if metadata:
      try:
          parsed_json = json.loads(metadata)
      except json.JSONDecodeError:
          parsed_json = {"error": "Invalid JSON format in metadata"}
  
  return parsed_json