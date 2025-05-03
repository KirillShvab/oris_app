from typing import Tuple


def rho_temperature(M, t):
    V0 = 22.413  # мольный объем

    return M / (V0 * (1 + 0.00367 * t))


def calculate_nkpr_zone(m: float, rho: float, c_nkpr: float) -> Tuple[float, float]:
    """
    Рассчитывает радиус R_{НКПР} и высоту Z_{НКПР}.

    Formula:
        R_{НКПР} = 7.8 * (m / (rho * C_{НКПР})) ** 0.33
        Z_{НКПР} = 0.26 * (m / (rho * C_{НКПР})) ** 0.33

    Args:
        m (float): Масса горючего вещества (ГГ или паров ЛВЖ), кг.
        rho (float): Плотность горючего вещества (ГГ или паров ЛВЖ) при расчетной температуре, кг/м³.
        c_nkpr (float): Нижний концентрационный предел распространения пламени, % об.

    Returns:
        Tuple[float, float]: Радиус R_{НКПР} (м) и высота Z_{НКПР} (м).

    Raises:
        ValueError: Если один из аргументов <= 0.
    """
    if m <= 0 or rho <= 0 or c_nkpr <= 0:
        raise ValueError("Все входные параметры должны быть положительными числами.")

    coefficient = pow((m / (rho * c_nkpr)), 0.33)
    r_nkpr = 7.80 * coefficient
    z_nkpr = 0.26 * coefficient
    return r_nkpr, z_nkpr


if __name__ == "__main__":
    try:
        r, z = calculate_nkpr_zone(m=100, rho=1.2, c_nkpr=5.0)
        print(f"R_НКПР: {r:.2f} м, Z_НКПР: {z:.2f} м")
    except ValueError as e:
        print(f"Ошибка: {e}")
