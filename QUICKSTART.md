# Quick Start Guide

## Installation

```bash
# 1. Clone the repository
git clone https://github.com/howillli/ai-watermark-remover.git
cd ai-watermark-remover

# 2. Install dependencies
pip install -r requirements.txt
```

## Basic Examples

### Example 1: Remove Top-Left Watermark

```bash
python scripts/remove_watermark.py your_image.jpg --position topleft --method telea --radius 15 --padding 30
```

### Example 2: Remove Bottom-Right Watermark

```bash
python scripts/remove_watermark.py your_image.jpg --position bottomright --method telea --radius 15 --padding 30
```

### Example 3: Remove Custom Area

```bash
python scripts/remove_watermark.py your_image.jpg --area 100,100,300,80 --method telea
```

### Example 4: Interactive Selection

```bash
python scripts/remove_watermark_interactive.py your_image.jpg
```

## Common Use Cases

### AI-Generated Image Watermarks

Most AI tools place watermarks in corners. Use:

```bash
# Top-left (common for "AI Generated" text)
python scripts/remove_watermark.py image.jpg --position topleft --size medium

# Bottom-right (common for platform logos)
python scripts/remove_watermark.py image.jpg --position bottomright --size medium
```

### Multiple Watermarks

Process in steps:

```bash
# Step 1: Remove first watermark
python scripts/remove_watermark.py image.jpg --position topleft --output step1.jpg

# Step 2: Remove second watermark
python scripts/remove_watermark.py step1.jpg --position bottomright --output final.jpg
```

### Batch Processing

Process all images in a folder:

```bash
python scripts/batch_remove_watermarks.py /path/to/images --position bottomright --method telea
```

## Tips

1. **Start with default settings** - They work well for most cases
2. **Use `--method telea`** - Best quality for most watermarks
3. **Increase `--radius`** - For larger watermarks (try 15-20)
4. **Add `--padding`** - To ensure complete removal (try 30-50)
5. **Preview first** - Use `--preview` flag to check before saving

## Troubleshooting

**Problem:** Watermark still visible  
**Solution:** Increase `--size` to `large` or use custom `--area`

**Problem:** Blurry result  
**Solution:** Try `--method patch` for better quality

**Problem:** Wrong position  
**Solution:** Use interactive mode to select exact area

## Need Help?

- Check the full [README.md](README.md)
- See [examples](examples/) folder for reference
- Open an issue on GitHub
