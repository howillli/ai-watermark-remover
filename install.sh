#!/bin/bash
# Installation script for AI Watermark Remover

echo "=== AI Watermark Remover - Installation ==="
echo ""

# Check Python
echo "Checking Python..."
if command -v python3 &> /dev/null; then
    PYTHON_VERSION=$(python3 --version)
    echo "✓ $PYTHON_VERSION"
else
    echo "✗ Python 3 is not installed"
    echo "  Please install Python 3.7 or higher"
    exit 1
fi
echo ""

# Check pip
echo "Checking pip..."
if command -v pip3 &> /dev/null; then
    echo "✓ pip3 is available"
else
    echo "✗ pip3 is not installed"
    exit 1
fi
echo ""

# Install dependencies
echo "Installing required packages..."
echo "This may take a few minutes..."
echo ""

pip3 install --user opencv-python opencv-contrib-python numpy pillow --quiet

if [ $? -eq 0 ]; then
    echo "✓ OpenCV and dependencies installed"
else
    echo "✗ Failed to install dependencies"
    exit 1
fi
echo ""

# Optional: scikit-image
echo "Installing optional packages (scikit-image)..."
pip3 install --user scikit-image --quiet

if [ $? -eq 0 ]; then
    echo "✓ scikit-image installed"
else
    echo "⚠ scikit-image installation failed (optional)"
fi
echo ""

# Verify installation
echo "Verifying installation..."
python3 -c "import cv2; print('✓ OpenCV version:', cv2.__version__)" 2>/dev/null
python3 -c "import numpy; print('✓ NumPy version:', numpy.__version__)" 2>/dev/null
python3 -c "import PIL; print('✓ Pillow version:', PIL.__version__)" 2>/dev/null
echo ""

echo "=== Installation Complete ==="
echo ""
echo "Quick test:"
echo "  python3 ~/.stepfun/skills/ai-watermark-remover/scripts/remove_watermark.py --help"
echo ""
