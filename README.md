# ImageHarvester

A desktop application for downloading and processing images from Bing, with filtering, conversion, and batch processing capabilities.

## Features

- Search and download images from Bing
- Filter images by minimum dimensions (400px)
- Convert images to JPG or PNG on the fly
- Batch processing with a queue system
- Configurable maximum images per search
- Rate limiting with customizable delay between requests

## Installation

```bash
# Clone the repository
git clone https://github.com/jopa79/RnD.git
cd RnD

# Create a virtual environment
python -m venv venv

# Activate the virtual environment
# On Windows
venv\Scripts\activate
# On macOS/Linux
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

## Usage

```bash
python -m image_harvester
```

## Development

```bash
# Run tests
python -m pytest
```

## License

MIT
