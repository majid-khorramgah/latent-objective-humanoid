from pathlib import Path
import numpy as np


# ============================================================
# Configuration
# ============================================================

PROJECT_ROOT = Path(__file__).resolve().parents[2]

NPZ_PATH = (
    PROJECT_ROOT
    / "data"
    / "processed"
    / "normalized"
    / "ACCAD"
    / "Female1General_c3d"
    / "A1 - Stand_poses.npz"
)


# ============================================================
# Helpers
# ============================================================

def print_header(title: str):
    print("\n" + "=" * 70)
    print(title)
    print("=" * 70)


def describe_array(name: str, x: np.ndarray):

    print(f"\n[{name}]")
    print(f"shape       : {x.shape}")
    print(f"dtype       : {x.dtype}")

    if x.size == 0:
        print("EMPTY")
        return

    x64 = x.astype(np.float64)

    print(f"min         : {np.min(x64):.8f}")
    print(f"max         : {np.max(x64):.8f}")
    print(f"mean        : {np.mean(x64):.8f}")
    print(f"std         : {np.std(x64):.8f}")

    print(f"nonzero     : {np.count_nonzero(x)} / {x.size}")

    if np.all(np.isfinite(x64)):
        print("finite      : YES")
    else:
        print("finite      : NO")


def check_binary(name: str, x: np.ndarray):

    unique = np.unique(x)

    print(f"\n{name} binary check")

    print(f"unique count: {len(unique)}")

    if len(unique) <= 20:
        print(f"unique      : {unique}")

    is_binary = np.all(
        np.isin(unique, [0, 1])
    )

    is_binary_pm = np.all(
        np.isin(unique, [-1, 0, 1])
    )

    print(f"binary 0/1  : {is_binary}")
    print(f"binary -1/0/1: {is_binary_pm}")


def frame_motion(x: np.ndarray):

    """
    Estimate frame-to-frame motion.

    Works for:
        [T,3]
        [T,J,3]
    """

    if x.shape[0] < 2:
        return None

    delta = np.diff(
        x.astype(np.float64),
        axis=0,
    )

    magnitude = np.linalg.norm(
        delta,
        axis=-1,
    )

    return magnitude


# ============================================================
# Main
# ============================================================

def main():

    print_header("MOTION CONTENT INSPECTION")

    print("PROJECT ROOT:")
    print(PROJECT_ROOT)

    print("\nFILE:")
    print(NPZ_PATH)

    if not NPZ_PATH.exists():
        raise FileNotFoundError(
            f"\nFile not found:\n{NPZ_PATH}"
        )

    with np.load(
        NPZ_PATH,
        allow_pickle=False,
    ) as data:

        print_header("AVAILABLE KEYS")

        for key in data.files:
            value = data[key]

            print(
                f"{key:35s}"
                f" shape={value.shape!s:18s}"
                f" dtype={value.dtype}"
            )

        # ======================================================
        # FULL
        # ======================================================

        full = data["full"]

        print_header("1. FULL — CANONICAL JOINT POSITIONS")

        describe_array(
            "full",
            full,
        )

        print(
            "\nInterpretation:"
        )

        print(
            "full contains normalized joint coordinates "
            "with shape [T,127,3]."
        )

        print(
            "Each frame has 127 joints and XYZ coordinates."
        )

        # Frame motion

        motion = frame_motion(full)

        if motion is not None:

            print(
                "\nFrame-to-frame joint motion:"
            )

            print(
                f"mean displacement : "
                f"{np.mean(motion):.8f}"
            )

            print(
                f"max displacement  : "
                f"{np.max(motion):.8f}"
            )

            print(
                f"nonzero frames    : "
                f"{np.count_nonzero(motion)}"
            )

        # ======================================================
        # ROOT POSITIONS
        # ======================================================

        root_positions = data[
            "root_positions"
        ]

        print_header(
            "2. ROOT POSITIONS — ORIGINAL GLOBAL POSITION"
        )

        describe_array(
            "root_positions",
            root_positions,
        )

        print(
            "\nFirst frame:"
        )

        print(
            root_positions[0]
        )

        print(
            "\nLast frame:"
        )

        print(
            root_positions[-1]
        )

        # ======================================================
        # ROOT DISPLACEMENT
        # ======================================================

        root_displacement = data[
            "root_displacement"
        ]

        print_header(
            "3. ROOT DISPLACEMENT"
        )

        describe_array(
            "root_displacement",
            root_displacement,
        )

        print(
            "\nFirst frame:"
        )

        print(
            root_displacement[0]
        )

        print(
            "\nLast frame:"
        )

        print(
            root_displacement[-1]
        )

        print(
            "\nTotal root displacement:"
        )

        total_displacement = np.linalg.norm(
            root_displacement[-1]
            - root_displacement[0]
        )

        print(
            f"{total_displacement:.8f}"
        )

        # ======================================================
        # ROOT VELOCITY
        # ======================================================

        root_velocity = data[
            "root_velocity"
        ]

        print_header(
            "4. ROOT VELOCITY"
        )

        describe_array(
            "root_velocity",
            root_velocity,
        )

        print(
            "\nFirst frame:"
        )

        print(
            root_velocity[0]
        )

        print(
            "\nMaximum velocity magnitude:"
        )

        velocity_magnitude = np.linalg.norm(
            root_velocity,
            axis=-1,
        )

        print(
            f"{np.max(velocity_magnitude):.8f}"
        )

        # ======================================================
        # NORMALIZED ROOT VELOCITY
        # ======================================================

        root_velocity_normalized = data[
            "root_velocity_normalized"
        ]

        print_header(
            "5. ROOT VELOCITY NORMALIZED"
        )

        describe_array(
            "root_velocity_normalized",
            root_velocity_normalized,
        )

        # ======================================================
        # BODY CONTACT
        # ======================================================

        body_contact = data[
            "body_contact"
        ]

        print_header(
            "6. BODY_CONTACT — CONTENT ANALYSIS"
        )

        describe_array(
            "body_contact",
            body_contact,
        )

        check_binary(
            "body_contact",
            body_contact,
        )

        print(
            "\nFirst frame:"
        )

        print(
            body_contact[0]
        )

        print(
            "\nSecond frame:"
        )

        if body_contact.shape[0] > 1:
            print(body_contact[1])

        # ======================================================
        # BODY CORE
        # ======================================================

        body_core = data[
            "body_core"
        ]

        print_header(
            "7. BODY_CORE"
        )

        describe_array(
            "body_core",
            body_core,
        )

        # ======================================================
        # HANDS
        # ======================================================

        hands = data[
            "hands"
        ]

        print_header(
            "8. HANDS"
        )

        describe_array(
            "hands",
            hands,
        )

        # ======================================================
        # FACE
        # ======================================================

        face = data[
            "face"
        ]

        print_header(
            "9. FACE"
        )

        describe_array(
            "face",
            face,
        )

        # ======================================================
        # BODY SCALE
        # ======================================================

        body_scale = data[
            "body_scale"
        ]

        print_header(
            "10. BODY SCALE"
        )

        print(
            f"value       : "
            f"{float(body_scale):.8f}"
        )

        # ======================================================
        # RECONSTRUCTION
        # ======================================================

        print_header(
            "11. RECONSTRUCTION CHECK"
        )

        print(
            "max abs error :",
            float(
                data[
                    "reconstruction_max_abs_error"
                ]
            ),
        )

        print(
            "mean abs error:",
            float(
                data[
                    "reconstruction_mean_abs_error"
                ]
            ),
        )

        print(
            "RMSE          :",
            float(
                data[
                    "reconstruction_rmse"
                ]
            ),
        )

        # ======================================================
        # FINAL SUMMARY
        # ======================================================

        print_header(
            "FINAL INTERPRETATION"
        )

        print(
            "Directly available:"
        )

        print(
            "  ✓ 127-joint positions"
        )

        print(
            "  ✓ Root global position"
        )

        print(
            "  ✓ Root displacement"
        )

        print(
            "  ✓ Root velocity / frame displacement"
        )

        print(
            "  ✓ Body core positions"
        )

        print(
            "  ✓ Hand positions"
        )

        print(
            "  ✓ Face positions"
        )

        print(
            "  ✓ Body scale"
        )

        print(
            "\nDerived from available data:"
        )

        print(
            "  → Joint velocity"
        )

        print(
            "  → Joint acceleration"
        )

        print(
            "  → Foot velocity"
        )

        print(
            "  → Joint/segment distances"
        )

        print(
            "  → Geometric angles"
        )

        print(
            "  → Body-part velocities"
        )

        print(
            "\nNOT automatically guaranteed:"
        )

        print(
            "  ? Contact probability"
        )

        print(
            "  ? Contact labels"
        )

        print(
            "  ? Motion phase"
        )

        print(
            "  ? Semantic motion labels"
        )

        print("\n" + "=" * 70)


if __name__ == "__main__":
    main()