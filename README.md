# QR Code Generator with Custom Logo

Generate QR codes with custom logos (PNG/JPG/PDF) in the center.

## Installation

```bash
pip install -r requirements.txt
```

For PDF support, install poppler-utils:
- **Linux**: `sudo apt-get install poppler-utils`
- **macOS**: `brew install poppler`
- **Windows**: Download from [poppler-windows](https://github.com/oschwartz10612/poppler-windows/releases/) and add bin/ to PATH

## Usage

### Basic Usage

```bash
python qr_generator.py --url "https://example.com" --logo "path/to/logo.png" --output "my_qr.png"
```

## Arguments

### Required/Basic Arguments

| Argument | Type | Default |Description |
|----------|------|---------|-------------|
| `--url` | str | | URL or text to encode in QR code |
| `--logo` | str | | Path to logo file (PNG, JPG, or PDF) |
| `--output` | str | data/output/qr_code_with_logo.png | Output path for generated QR code |

### QR Code Parameters

| Argument | Type | Default | Description |
|----------|------|---------|-------------|
| `--qr-size` | int | 20 | Size of each QR code box (higher = larger QR) |
| `--border` | int | 4 | Border width around QR code in boxes |

### Logo Parameters

| Argument | Type | Default | Description |
|----------|------|---------|-------------|
| `--logo-size-ratio` | float | 0.25 | Logo size as ratio of QR size (0.1-0.4 recommended) |
| `--logo-border-width` | int | 17 | Width of border around logo in pixels |
| `--logo-border-padding` | int | 2 | Space between logo and border in pixels |
| `--logo-border-color` | str | white | Color of border around logo |

## Examples

**Custom URL and logo:**
```bash
python qr_generator.py --url "https://mysite.com" --logo "mylogo.png"
```

**Full customization:**
```bash
python qr_generator.py \
  --url "https://mysite.com" \
  --logo "mylogo.png" \
  --output "custom_qr.png" \
  --qr-size 15 \
  --logo-size-ratio 0.3 \
  --logo-border-width 20 \
  --logo-border-color black
```
