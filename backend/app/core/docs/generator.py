"""
Documentation Generator
PGF Protocol: DOC_002
Gate: GATE_8
Version: 1.0.0
"""

from pathlib import Path
from typing import Dict, Any, List
import asyncio
import logging
from datetime import datetime

from fastapi import FastAPI
from .framework import (
    DocGenerator,
    Documentation,
    DocType,
    DocFormat,
    DocSection
)

class DocumentationGenerator:
    """Documentation generator for the Vedic Astrology System"""
    
    def __init__(self, app: FastAPI):
        self.app = app
        self.doc_generator = DocGenerator(app)
        self._setup_logging()
    
    def _setup_logging(self) -> None:
        """Setup logging"""
        logging.basicConfig(
            level=logging.INFO,
            format="%(asctime)s [%(levelname)s] %(message)s",
            handlers=[
                logging.FileHandler("docs/generation.log"),
                logging.StreamHandler()
            ]
        )
        self.logger = logging.getLogger(__name__)
    
    async def generate_all(self) -> Dict[str, Documentation]:
        """Generate all documentation"""
        self.logger.info("Starting documentation generation")
        start_time = datetime.utcnow()
        
        try:
            # Generate API documentation
            self.logger.info("Generating API documentation")
            api_docs = self.doc_generator.generate_api_docs()
            
            # Generate code documentation
            self.logger.info("Generating code documentation")
            code_docs = self.doc_generator.generate_code_docs(
                Path("app")
            )
            
            # Generate architecture documentation
            self.logger.info("Generating architecture documentation")
            arch_docs = self.doc_generator.generate_architecture_docs()
            
            # Calculate generation time
            duration = (datetime.utcnow() - start_time).total_seconds()
            self.logger.info(f"Documentation generation completed in {duration:.2f}s")
            
            return {
                "api": api_docs,
                "code": code_docs,
                "architecture": arch_docs
            }
            
        except Exception as e:
            self.logger.error(f"Documentation generation failed: {str(e)}")
            raise
    
    def generate_readme(self, docs: Dict[str, Documentation]) -> None:
        """Generate main README file"""
        readme_content = f"""# Vedic Astrology System

## Overview
This is a modern Vedic Astrology system built with FastAPI and React, providing accurate astrological calculations and analysis.

## Documentation
- [API Documentation](docs/api/api_docs.md)
- [Code Documentation](docs/code/code_docs.md)
- [Architecture Documentation](docs/architecture/architecture_docs.md)

## Features
- Accurate planetary calculations
- Astrological pattern analysis
- Modern, responsive UI
- High-performance backend
- Comprehensive security

## Quick Start
1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Run the application:
   ```bash
   uvicorn app.main:app --reload
   ```

3. Visit the API documentation:
   ```
   http://localhost:8000/docs
   ```

## Development
- Python 3.8+
- FastAPI
- SQLAlchemy
- React
- TypeScript

## Testing
Run tests with:
```bash
python -m pytest
```

## License
MIT License

## Documentation Generation
Last generated: {datetime.utcnow().isoformat()}
"""
        
        with open("README.md", "w") as f:
            f.write(readme_content)
        
        self.logger.info("Generated README.md")

async def generate_docs(app: FastAPI) -> None:
    """Generate all documentation"""
    generator = DocumentationGenerator(app)
    docs = await generator.generate_all()
    generator.generate_readme(docs)

if __name__ == "__main__":
    from app.main import app
    asyncio.run(generate_docs(app))
