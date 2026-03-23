"""Basic smoke tests."""


def test_package_imports() -> None:
    """Check core imports."""
    import final_fyp_aarvis.main  # noqa: F401
    import final_fyp_aarvis.api.server  # noqa: F401
    import final_fyp_aarvis.agent.graph  # noqa: F401
