"""
QR Code Generator with Custom Logo
This script generates a QR code with a custom image (PNG/PDF) in the center.
"""

import argparse
import os
import warnings

import qrcode
from pdf2image import convert_from_path
from PIL import Image, ImageColor, ImageDraw


def is_white_color(color: str) -> bool:
    """Return True when the provided Pillow color resolves to pure white."""
    try:
        return ImageColor.getcolor(color, "RGBA")[:3] == (255, 255, 255)
    except ValueError:
        return False


def generate_qr_with_logo(
    url: str,
    logo_path: str,
    output_path: str = "qr_code_with_logo.png",
    qr_size: int = 10,
    border: int = 4,
    fill_color: str = "black",
    background_color: str = "white",
    transparent_background: bool = False,
    logo_background_color: str | None = None,
    logo_size_ratio: float = 0.3,
    logo_border_width: int = 5,
    logo_border_padding: int = 10,
    logo_border_color: str = "black",
) -> None:
    """
    Generate a QR code with a custom logo in the center.

    Args:
        url (str): The URL or text to encode in the QR code
        logo_path (str): Path to the logo image (PNG, JPG, or PDF)
        output_path (str): Path where the final QR code will be saved
        qr_size (int): Size of the QR code (1-40, higher = more dense)
        border (int): Width of the border around the QR code
        fill_color (str): Color of the QR modules
        background_color (str): Color of the QR background
        transparent_background (bool): Whether the QR background should be transparent
        logo_background_color (str | None): Background behind the logo area; defaults to transparent when the QR background is transparent, otherwise uses the QR background color
        logo_size_ratio (float): Ratio of logo size to QR code size (0.1-0.4 recommended)
        logo_border_width (int): Width of the border around the logo in pixels
        logo_border_padding (int): Space between logo and border in pixels
        logo_border_color (str): Color of the border around the logo
    """

    try:
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_H,
            box_size=qr_size,
            border=border,
        )

        qr.add_data(url)
        qr.make(fit=True)

        background = "transparent" if transparent_background else background_color
        qr_img = qr.make_image(fill_color=fill_color, back_color=background).convert(
            "RGBA"
        )

        if (
            transparent_background
            and os.path.splitext(output_path)[1].lower() in {".jpg", ".jpeg"}
        ):
            raise ValueError(
                "Transparent background requires an output format that supports alpha, such as PNG or WebP."
            )

        if logo_path.lower().endswith(".pdf"):
            try:
                logo = convert_from_path(logo_path)[0]
            except ImportError:
                raise ImportError(
                    "pdf2image library not installed. Install with: pip install pdf2image. Also requires poppler-utils: sudo apt-get install poppler-utils"
                )
        else:
            logo = Image.open(logo_path)

        logo = logo.convert("RGBA")

        qr_width, qr_height = qr_img.size
        logo_max_size = int(min(qr_width, qr_height) * logo_size_ratio)

        logo_aspect = logo.size[0] / logo.size[1]
        if logo.size[0] > logo.size[1]:
            new_width = logo_max_size
            new_height = int(logo_max_size / logo_aspect)
        else:
            new_height = logo_max_size
            new_width = int(logo_max_size * logo_aspect)

        logo = logo.resize((new_width, new_height), Image.Resampling.LANCZOS)

        total_border_size = logo_border_width + logo_border_padding
        logo_with_border_size = (
            logo.size[0] + 2 * total_border_size,
            logo.size[1] + 2 * total_border_size,
        )

        resolved_logo_background_color = logo_background_color
        if resolved_logo_background_color is None:
            resolved_logo_background_color = (
                "transparent" if transparent_background else background_color
            )

        if resolved_logo_background_color == "transparent":
            logo_background = (0, 0, 0, 0)
        else:
            logo_background = resolved_logo_background_color

        logo_composite = Image.new("RGBA", logo_with_border_size, logo_background)

        if logo_border_width > 0:
            draw = ImageDraw.Draw(logo_composite)

            for i in range(logo_border_width):
                draw.rectangle(
                    [
                        i,
                        i,
                        logo_with_border_size[0] - 1 - i,
                        logo_with_border_size[1] - 1 - i,
                    ],
                    outline=logo_border_color,
                )

        logo_paste_pos = (total_border_size, total_border_size)
        logo_composite.paste(logo, logo_paste_pos, mask=logo)

        composite_pos = (
            (qr_width - logo_composite.size[0]) // 2,
            (qr_height - logo_composite.size[1]) // 2,
        )

        if resolved_logo_background_color == "transparent":
            qr_img.paste(
                (0, 0, 0, 0),
                (
                    composite_pos[0],
                    composite_pos[1],
                    composite_pos[0] + logo_composite.size[0],
                    composite_pos[1] + logo_composite.size[1],
                ),
            )

        qr_img.paste(logo_composite, composite_pos, mask=logo_composite)

        qr_img.save(output_path, quality=95, optimize=False, dpi=(300, 300))
        print(f"QR code successfully generated: {output_path}")

    except FileNotFoundError:
        raise FileNotFoundError(f"Logo file not found at {logo_path}")
    except Exception as e:
        raise e


def main():
    parser = argparse.ArgumentParser(
        description="Generate QR codes with custom logos in the center."
    )

    # Required arguments
    parser.add_argument(
        "--url",
        type=str,
        default="https://valira.ai/",
        help="URL or text to encode in the QR code (default: https://valira.ai/)",
    )
    parser.add_argument(
        "--logo",
        type=str,
        default="data/input/Valira_AI_LOGO_Terciarni_Crn.png",
        help="Path to logo image (PNG, JPG, or PDF)",
    )
    parser.add_argument(
        "--output",
        type=str,
        default="data/output/qr_code_with_logo.png",
        help="Output path for the generated QR code",
    )

    # QR code parameters
    parser.add_argument(
        "--qr-size",
        type=int,
        default=20,
        help="Size of each QR code box (default: 20)",
    )
    parser.add_argument(
        "--border",
        type=int,
        default=4,
        help="Width of the border around the QR code in boxes (default: 4)",
    )
    parser.add_argument(
        "--fill-color",
        type=str,
        default="black",
        help="Color of the QR modules, for example black, white, or #0f766e (default: black)",
    )
    parser.add_argument(
        "--background-color",
        type=str,
        default="white",
        help="Color of the QR background when transparency is not enabled (default: white)",
    )
    parser.add_argument(
        "--transparent-background",
        action="store_true",
        help="Save the QR background as transparent. Use a format that supports alpha, such as PNG.",
    )
    parser.add_argument(
        "--logo-background-color",
        type=str,
        default=None,
        help="Background behind the logo area. Defaults to transparent when the QR background is transparent, otherwise uses the QR background color.",
    )

    # Logo parameters
    parser.add_argument(
        "--logo-size-ratio",
        type=float,
        default=0.25,
        help="Logo size as ratio of QR code size, 0.1-0.4 recommended (default: 0.25)",
    )
    parser.add_argument(
        "--logo-border-width",
        type=int,
        default=17,
        help="Width of the border around the logo in pixels (default: 17)",
    )
    parser.add_argument(
        "--logo-border-padding",
        type=int,
        default=2,
        help="Space between logo and border in pixels (default: 2)",
    )
    parser.add_argument(
        "--logo-border-color",
        type=str,
        default="white",
        help="Color of the border around the logo (default: white)",
    )

    args = parser.parse_args()

    if args.transparent_background and is_white_color(args.fill_color):
        warnings.warn(
            "White QR modules on a transparent background may appear invisible on white surfaces or in image viewers with a white canvas."
        )

    if not os.path.exists(args.logo):
        warnings.warn(f"Logo file '{args.logo}' not found.")
        warnings.warn("Please provide a valid logo file path using --logo argument.")
        warnings.warn("\nCreating a sample QR code without logo...")

        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_H,
            box_size=10,
            border=4,
        )
        qr.add_data(args.url)
        qr.make(fit=True)
        background = "transparent" if args.transparent_background else args.background_color
        img = qr.make_image(fill_color=args.fill_color, back_color=background)
        img.save("simple_qr_code.png")
        print("Simple QR code (without logo) saved as: simple_qr_code.png")
        return

    output_dir = os.path.dirname(args.output)
    if output_dir and not os.path.exists(output_dir):
        os.makedirs(output_dir)

    generate_qr_with_logo(
        url=args.url,
        logo_path=args.logo,
        output_path=args.output,
        qr_size=args.qr_size,
        border=args.border,
        fill_color=args.fill_color,
        background_color=args.background_color,
        transparent_background=args.transparent_background,
        logo_background_color=args.logo_background_color,
        logo_size_ratio=args.logo_size_ratio,
        logo_border_width=args.logo_border_width,
        logo_border_padding=args.logo_border_padding,
        logo_border_color=args.logo_border_color,
    )


if __name__ == "__main__":
    main()
