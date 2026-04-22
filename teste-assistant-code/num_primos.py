import math


def eh_primo(n: int) -> bool:
    """Verifica se um inteiro n é número primo."""
    if n <= 1:
        return False
    if n <= 3:
        return True
    if _e_multiplo_de_dois_ou_tres(n):
        return False
    return _nao_tem_divisor_ate_raiz(n)


def _e_multiplo_de_dois_ou_tres(n: int) -> bool:
    return n % 2 == 0 or n % 3 == 0


def _nao_tem_divisor_ate_raiz(n: int) -> bool:
    limite = math.isqrt(n)
    for i in range(5, limite + 1, 6):
        if n % i == 0 or n % (i + 2) == 0:
            return False
    return True


if __name__ == "__main__":
    numeros = [1, 2, 3, 4, 16, 17, 19, 20]
    for numero in numeros:
        resultado = "primo" if eh_primo(numero) else "não primo"
        print(f"{numero} -> {resultado}")
