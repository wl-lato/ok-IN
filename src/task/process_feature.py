"""process_feature: feature preprocessor for Infinity Nikki.

Mirrors src/task/process_feature.py from ok-ww.
Registered in config.py as the `feature_processor` for template_matching.

This module handles alpha-channel mask extraction for icons.
The composite image (assets/images/0.png) fills transparency with solid color,
but game screenshots have different backgrounds. Masks make template matching
ignore the background and only compare the icon pixels.

Note: Alpha mask loading was moved here from DailyTask._setup_feature_masks().
The config.py registers this as the global feature_processor, so masks are loaded
automatically when FeatureSet initializes, not just when DailyTask.run() is called.
"""

import os

import cv2


def process_feature(feature_name: str, feature) -> None:
    """Apply preprocessing to a feature's template image.

    Called by FeatureSet._merge_features() when loading features.
    See ok-script FeatureSet for the calling convention.

    Args:
        feature_name: The name/label of the feature (may include namespace prefix).
        feature: The Feature object whose .mat and .mask will be set/modified.
    """
    _load_alpha_mask(feature_name, feature)


def _load_alpha_mask(feature_name: str, feature) -> None:
    """Load alpha-channel mask from original PNG and assign to feature.

    Args:
        feature_name: Name of the feature.
        feature: Feature object with .mat (template) and .mask attributes.
    """
    if feature.mask is not None:
        return  # Already has a mask

    # Strip namespace prefix if present (e.g. "import/feature_name")
    png_name = feature_name.split("/")[-1] if "/" in feature_name else feature_name

    # Try features/ directory
    features_dir = os.path.join(os.getcwd(), "features")
    png_path = os.path.join(features_dir, f"{png_name}.png")

    if not os.path.exists(png_path):
        return  # No original PNG found

    # Read PNG with alpha channel (IMREAD_UNCHANGED = -1)
    img = cv2.imread(png_path, cv2.IMREAD_UNCHANGED)
    if img is None:
        return

    # Check if image has alpha channel
    if len(img.shape) < 3 or img.shape[2] < 4:
        return  # No alpha channel

    # Extract alpha channel and create binary mask
    alpha = img[:, :, 3]
    mask = ((alpha > 127).astype("uint8")) * 255

    # If fully opaque, mask is not useful
    if mask.min() == 255:
        return

    # Resize mask to match template dimensions
    th, tw = feature.mat.shape[:2]
    if tw > 0 and th > 0:
        mask = cv2.resize(mask, (tw, th), interpolation=cv2.INTER_NEAREST)
        feature.mask = mask
