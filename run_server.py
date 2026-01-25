#!/usr/bin/env python3
"""
Script para iniciar o servidor AuthLook
"""
import os
import uvicorn

# Detectar se está em produção
IS_PRODUCTION = os.getenv("ENVIRONMENT", "development") == "production"

if __name__ == "__main__":
    if IS_PRODUCTION:
        # Modo produção: sem reload, workers múltiplos
        uvicorn.run(
            "backend.app:app",
            host="0.0.0.0",
            port=int(os.getenv("PORT", 8000)),
            reload=False,
            workers=int(os.getenv("WORKERS", 4)),
            log_level="info",
            access_log=True
        )
    else:
        # Modo desenvolvimento: com reload
        uvicorn.run(
            "backend.app:app",
            host="0.0.0.0",
            port=8000,
            reload=True,
            log_level="debug"
        )

