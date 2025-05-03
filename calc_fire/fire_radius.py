def calculate_flash_fire_radius(R_nkpr: float) -> float:
    """
    Рассчитывает радиус пожар-вспышки (R_F) на основе горизонтального размера взрывоопасной зоны (R_nkpr).

    Formula:
        R_F = 1.2 * R_nkpr

    Args:
        R_nkpr (float): Горизонтальный размер взрывоопасной зоны в метрах. Значение должно быть неотрицательным.

    Returns:
        float: Радиус пожар-вспышки в метрах.

    Raises:
        ValueError: Если R_nkpr является отрицательным.
    """
    if R_nkpr < 0:
        raise ValueError("R_nkpr должен быть неотрицательным.")
    return 1.2 * R_nkpr
