import pandas as pd


MODEL_DISPLAY_NAMES = {
    "resnet18": "ResNet18",
    "resnet34": "ResNet34",
    "resnet50": "ResNet50",
    "resnet101": "ResNet101",
    "convnext_tiny": "ConvNeXt-Tiny",
    "mobilenetv3_small_100": "MobileNetV3-Small",
    "mobilenet_v3_small": "MobileNetV3-Small",
    "mobilenet_v2": "MobileNetV2",
    "shufflenet_v2_x1_0": "ShuffleNetV2",
    "vit_base_patch16_224": "ViT-B/16",
    "vit_b_16": "ViT-B/16",
    "efficientnet_b3": "EfficientNet-B3",
}


def format_model_name(model_name: str) -> str:
    """Convert internal model names into cleaner display names."""

    if model_name is None or pd.isna(model_name):
        return "Not Applicable"

    cleaned_name = str(model_name).strip()
    return MODEL_DISPLAY_NAMES.get(cleaned_name.lower(), cleaned_name)


def split_edge_models(edge_model: str) -> list[str]:
    """Split edge-model combinations written with + or commas."""

    cleaned = str(edge_model).replace(",", "+")
    return [
        format_model_name(model.strip())
        for model in cleaned.split("+")
        if model.strip()
    ]
