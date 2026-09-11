
from typing import Dict, Any

from sentence_transformers import SentenceTransformer, util

from .extract_attributes import extract_attributes


MODEL_NAME = "all-MiniLM-L6-v2"

model = SentenceTransformer(MODEL_NAME)


# ---------------------------------------------------------
# Numeric comparison
# ---------------------------------------------------------

def values_are_equal(
    value_a: Any,
    value_b: Any,
    tolerance: float = 0.0,
) -> bool:
    """
    Compare two values.

    Numeric values use a tolerance.
    Strings use exact comparison.
    """

    if value_a is None or value_b is None:
        return False

    if isinstance(value_a, (int, float)) and isinstance(
        value_b, (int, float)
    ):
        return abs(value_a - value_b) <= tolerance

    return value_a == value_b


# ---------------------------------------------------------
# Semantic similarity
# ---------------------------------------------------------

def semantic_similarity(
    text_a: str,
    text_b: str,
) -> float:

    embeddings = model.encode(
        [text_a, text_b],
        convert_to_tensor=True,
    )

    score = util.cos_sim(
        embeddings[0],
        embeddings[1],
    ).item()

    return max(0.0, min(1.0, score))


# ---------------------------------------------------------
# Attribute comparison
# ---------------------------------------------------------

def get_category_fields(category: str):
    """
    Return important fields for each material category.
    """

    categories = {

        "BOLT": [
            ("material", 0.0),
            ("diameter_mm", 0.5),
            ("length_mm", 0.5),
        ],

        "BALL_VALVE": [
            ("material", 0.0),
            ("size_mm", 1.0),
            ("pressure_rating_psi", 0.0),
            ("connection_type", 0.0),
        ],

        "BEARING": [
            ("bearing_number", 0.0),
            ("seal_type", 0.0),
            ("bearing_type", 0.0),
            ("material", 0.0),
        ],

        "PIPE": [
            ("material", 0.0),
            ("diameter_mm", 1.0),
            ("wall_thickness_mm", 0.2),
            ("pipe_type", 0.0),
        ],
    }

    return categories.get(category, [])


def attribute_similarity(
    attrs_a: Dict[str, Any],
    attrs_b: Dict[str, Any],
) -> float:

    category_a = attrs_a.get(
        "category",
        "UNKNOWN",
    )

    category_b = attrs_b.get(
        "category",
        "UNKNOWN",
    )

    # Different categories cannot match.
    if (
        category_a != "UNKNOWN"
        and category_b != "UNKNOWN"
        and category_a != category_b
    ):
        return 0.0

    category = (
        category_a
        if category_a != "UNKNOWN"
        else category_b
    )

    fields = get_category_fields(category)

    if not fields:
        return 0.0

    matched = 0.0
    available = 0.0

    for field, tolerance in fields:

        value_a = attrs_a.get(field)
        value_b = attrs_b.get(field)

        # Ignore a field if neither side has information.
        if value_a is None and value_b is None:
            continue

        available += 1.0

        if values_are_equal(
            value_a,
            value_b,
            tolerance,
        ):
            matched += 1.0

    if available == 0:
        return 0.0

    return matched / available


# ---------------------------------------------------------
# Critical mismatch detection
# ---------------------------------------------------------

def critical_mismatch(
    attrs_a: Dict[str, Any],
    attrs_b: Dict[str, Any],
) -> bool:

    category_a = attrs_a.get(
        "category",
        "UNKNOWN",
    )

    category_b = attrs_b.get(
        "category",
        "UNKNOWN",
    )

    # Category mismatch
    if category_a != category_b:
        return True

    category = category_a

    # -----------------------------------------------------
    # BOLT
    # -----------------------------------------------------

    if category == "BOLT":

        if (
            attrs_a.get("material") is not None
            and attrs_b.get("material") is not None
            and attrs_a["material"]
            != attrs_b["material"]
        ):
            return True

        diameter_a = attrs_a.get("diameter_mm")
        diameter_b = attrs_b.get("diameter_mm")

        if (
            diameter_a is not None
            and diameter_b is not None
            and abs(diameter_a - diameter_b) > 0.5
        ):
            return True

        length_a = attrs_a.get("length_mm")
        length_b = attrs_b.get("length_mm")

        if (
            length_a is not None
            and length_b is not None
            and abs(length_a - length_b) > 0.5
        ):
            return True

    # -----------------------------------------------------
    # BALL VALVE
    # -----------------------------------------------------

    elif category == "BALL_VALVE":

        # Material
        if (
            attrs_a.get("material") is not None
            and attrs_b.get("material") is not None
            and attrs_a["material"]
            != attrs_b["material"]
        ):
            return True

        # Size
        size_a = attrs_a.get("size_mm")
        size_b = attrs_b.get("size_mm")

        if (
            size_a is not None
            and size_b is not None
            and abs(size_a - size_b) > 1.0
        ):
            return True

        # Pressure rating
        pressure_a = attrs_a.get(
            "pressure_rating_psi"
        )

        pressure_b = attrs_b.get(
            "pressure_rating_psi"
        )

        if (
            pressure_a is not None
            and pressure_b is not None
            and pressure_a != pressure_b
        ):
            return True

        # Connection
        connection_a = attrs_a.get(
            "connection_type"
        )

        connection_b = attrs_b.get(
            "connection_type"
        )

        if (
            connection_a is not None
            and connection_b is not None
            and connection_a != connection_b
        ):
            return True

    # -----------------------------------------------------
    # BEARING
    # -----------------------------------------------------

    elif category == "BEARING":

        # Bearing number is critical.
        number_a = attrs_a.get(
            "bearing_number"
        )

        number_b = attrs_b.get(
            "bearing_number"
        )

        if (
            number_a is not None
            and number_b is not None
            and number_a != number_b
        ):
            return True

        # Seal type can be functionally significant.
        seal_a = attrs_a.get(
            "seal_type"
        )

        seal_b = attrs_b.get(
            "seal_type"
        )

        if (
            seal_a is not None
            and seal_b is not None
            and seal_a != seal_b
        ):
            return True

        # Bearing type
        bearing_type_a = attrs_a.get(
            "bearing_type"
        )

        bearing_type_b = attrs_b.get(
            "bearing_type"
        )

        if (
            bearing_type_a is not None
            and bearing_type_b is not None
            and bearing_type_a != bearing_type_b
        ):
            return True

    # -----------------------------------------------------
    # PIPE
    # -----------------------------------------------------

    elif category == "PIPE":

        # Material
        if (
            attrs_a.get("material") is not None
            and attrs_b.get("material") is not None
            and attrs_a["material"]
            != attrs_b["material"]
        ):
            return True

        # Diameter
        diameter_a = attrs_a.get(
            "diameter_mm"
        )

        diameter_b = attrs_b.get(
            "diameter_mm"
        )

        if (
            diameter_a is not None
            and diameter_b is not None
            and abs(diameter_a - diameter_b) > 1.0
        ):
            return True

        # Wall thickness
        thickness_a = attrs_a.get(
            "wall_thickness_mm"
        )

        thickness_b = attrs_b.get(
            "wall_thickness_mm"
        )

        if (
            thickness_a is not None
            and thickness_b is not None
            and abs(
                thickness_a - thickness_b
            ) > 0.2
        ):
            return True

        # Pipe type
        pipe_a = attrs_a.get(
            "pipe_type"
        )

        pipe_b = attrs_b.get(
            "pipe_type"
        )

        if (
            pipe_a is not None
            and pipe_b is not None
            and pipe_a != pipe_b
        ):
            return True

    return False


# ---------------------------------------------------------
# Main material comparison
# ---------------------------------------------------------

def compare_materials(
    text_a: str,
    text_b: str,
) -> Dict[str, Any]:

    attrs_a = extract_attributes(text_a)
    attrs_b = extract_attributes(text_b)

    semantic_score = semantic_similarity(
        text_a,
        text_b,
    )

    attr_score = attribute_similarity(
        attrs_a,
        attrs_b,
    )

    final_score = (
        semantic_score * 0.40
        + attr_score * 0.60
    )

    is_critical_mismatch = critical_mismatch(
        attrs_a,
        attrs_b,
    )

    # Critical engineering differences should prevent
    # a high-confidence identical/equivalent result.
    if is_critical_mismatch:
        final_score = min(
            final_score,
            0.60,
        )

        classification = "DIFFERENT"

    elif final_score >= 0.90:
        classification = "IDENTICAL"

    elif final_score >= 0.75:
        classification = "EQUIVALENT"

    elif final_score >= 0.55:
        classification = "NEAR_DUPLICATE"

    else:
        classification = "DIFFERENT"

    return {
        "text_a": text_a,
        "text_b": text_b,
        "attributes_a": attrs_a,
        "attributes_b": attrs_b,
        "semantic_score": round(
            semantic_score,
            4,
        ),
        "attribute_score": round(
            attr_score,
            4,
        ),
        "final_score": round(
            final_score,
            4,
        ),
        "critical_mismatch": is_critical_mismatch,
        "classification": classification,
    }


# ---------------------------------------------------------
# Pretty printing
# ---------------------------------------------------------

def print_result(
    result: Dict[str, Any],
) -> None:

    print("\n" + "=" * 60)

    print("\nMATERIAL A:")
    print(result["text_a"])

    print("\nATTRIBUTES A:")
    print(result["attributes_a"])

    print("\nMATERIAL B:")
    print(result["text_b"])

    print("\nATTRIBUTES B:")
    print(result["attributes_b"])

    print(
        f"\nSemantic Score    : "
        f"{result['semantic_score']:.2%}"
    )

    print(
        f"Attribute Score   : "
        f"{result['attribute_score']:.2%}"
    )

    print(
        f"Final Score       : "
        f"{result['final_score']:.2%}"
    )

    print(
        f"Critical Mismatch : "
        f"{result['critical_mismatch']}"
    )

    print(
        f"Classification     : "
        f"{result['classification']}"
    )


# ---------------------------------------------------------
# Test cases
# ---------------------------------------------------------

if __name__ == "__main__":

    examples = [

        # Same bolt
        (
            "HEX BOLT M10 X 50 SS304",
            "SS 304 HEXAGONAL BOLT 10MM X 50MM",
        ),

        # Different bolt material
        (
            "HEX BOLT M10 X 50 SS304",
            "HEX BOLT M10 X 50 SS316",
        ),

        # Same valve
        (
            "SS316 FLANGED BALL VALVE 2 INCH 150 PSI",
            "2 IN FLG BALL VALVE SS316 150 PSI",
        ),

        # Equivalent valve representation
        (
            "SS316 FLANGED BALL VALVE 2 INCH 150 PSI",
            "BALL VALVE 50MM FLANGED SS316 150 PSI",
        ),

        # Different pipe material
        (
            "SEAMLESS PIPE SS304 50MM X 3MM",
            "SEAMLESS SS316 PIPE 50MM X 3MM",
        ),

        # Different bearing number
        (
            "BEARING 6205 ZZ",
            "BEARING 6206 ZZ",
        ),
    ]

    for text_a, text_b in examples:

        result = compare_materials(
            text_a,
            text_b,
        )

        print_result(result)

