from fastapi.middleware.cors import CORSMiddleware

def app_cors(app):

  # 允許跨域請求 (CORS)
  app.add_middleware(
      CORSMiddleware,
      allow_origins=["*"],  # 允許所有來源
      allow_credentials=True,
      allow_methods=["*"],
      allow_headers=["*"],
  )
