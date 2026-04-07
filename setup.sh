#!/bin/bash
# Quick setup script for Email Triage OpenEnv
# Run: bash setup.sh

set -e  # Exit on error

echo ""
echo "🚀 Setting up Email Triage OpenEnv..."
echo ""

# Colors for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# 1. Create virtual environment
echo -e "${BLUE}[1/4]${NC} Creating virtual environment..."
if [ ! -d "venv" ]; then
    python -m venv venv
    echo -e "${GREEN}✓${NC} Virtual environment created"
else
    echo -e "${GREEN}✓${NC} Virtual environment already exists"
fi

# 2. Activate venv (Unix-like)
echo -e "${BLUE}[2/4]${NC} Activating virtual environment..."
source venv/bin/activate
echo -e "${GREEN}✓${NC} Virtual environment activated"

# 3. Install dependencies
echo -e "${BLUE}[3/4]${NC} Installing dependencies..."
python -m pip install --upgrade pip setuptools wheel

# Install numpy first with pre-built wheels for compatibility
echo "Installing numpy 1.24.3 (model-compatible version)..."
python -m pip install --only-binary :all: numpy==1.24.3 || {
    echo -e "${YELLOW}WARNING${NC}: numpy install had issues, continuing..."
}

# Install remaining dependencies
python -m pip install --no-build-isolation --no-cache-dir -r requirements.txt || {
    echo -e "${YELLOW}WARNING${NC}: Some packages may have failed to install"
}
echo -e "${GREEN}✓${NC} Dependencies installed"

# 4. Train model (if not exists)
echo -e "${BLUE}[4/4]${NC} Checking for pre-trained model..."
if [ ! -f "ppo_email_triage.zip" ]; then
    echo "Training new model (this may take 5-10 minutes)..."
    python train.py || echo -e "${YELLOW}WARNING${NC}: Training may not have completed"
else
    echo -e "${GREEN}✓${NC} Pre-trained model found"
fi

echo ""
echo -e "${GREEN}✅ Setup complete!${NC}"
echo ""
echo "Next steps:"
echo "  1. Activate environment: source venv/bin/activate"
echo "  2. Run Gradio demo: python app_gradio.py"
echo "  3. Or run FastAPI: uvicorn app.main:app --reload"
echo ""
echo "Docker deployment:"
echo "  docker build -t email-triage:latest ."
echo "  docker run -p 7860:7860 email-triage:latest"
echo ""
