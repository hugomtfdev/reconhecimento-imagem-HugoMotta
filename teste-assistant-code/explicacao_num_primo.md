# Explicação Técnica do Código Python para Verificação de Número Primo

Este documento descreve o funcionamento da função `eh_primo` presente em `num_primos.py`.

## Objetivo

A função `eh_primo(n: int) -> bool` verifica se um número inteiro `n` é primo.

- Retorna `True` se `n` for primo
- Retorna `False` caso contrário

## Definição de número primo

Um número primo é um inteiro maior que 1 que possui exatamente dois divisores positivos: `1` e ele mesmo.

## Estrutura do código

### 1. Separação de responsabilidades

O código foi organizado em funções pequenas e legíveis:

- `eh_primo(n)` é a função pública que determina primalidade.
- `_e_multiplo_de_dois_ou_tres(n)` trata a eliminação inicial de divisores simples.
- `_nao_tem_divisor_ate_raiz(n)` verifica divisores maiores usando um laço eficiente.

### 2. Casos base

```python
if n <= 1:
    return False
if n <= 3:
    return True
```

- `n <= 1`: números menores ou iguais a 1 não são primos.
- `n <= 3`: `2` e `3` são primos e são aceitos rapidamente.

### 3. Eliminação rápida de múltiplos de 2 e 3

```python
if _e_multiplo_de_dois_ou_tres(n):
    return False
```

```python
def _e_multiplo_de_dois_ou_tres(n: int) -> bool:
    return n % 2 == 0 or n % 3 == 0
```

- Essa função torna o código mais legível ao expressar claramente a intenção.
- A verificação remove muitos casos não primos sem entrar no laço principal.

### 4. Verificação eficiente até a raiz quadrada

```python
def _nao_tem_divisor_ate_raiz(n: int) -> bool:
    limite = math.isqrt(n)
    for i in range(5, limite + 1, 6):
        if n % i == 0 or n % (i + 2) == 0:
            return False
    return True
```

- `math.isqrt(n)` calcula a raiz quadrada inteira de `n` sem conversão para float.
- `range(5, limite + 1, 6)` percorre apenas números na forma `6k - 1` e `6k + 1`.
- Assim, o algoritmo testa menos candidatos e fica mais eficiente.

### 5. Retorno final

```python
return _nao_tem_divisor_ate_raiz(n)
```

- Se nenhum divisor válido for encontrado até `sqrt(n)`, o número é primo.

## Bloco principal para demonstração

No final do arquivo há um bloco protegido por `if __name__ == "__main__":`:

```python
if __name__ == "__main__":
    numeros = [1, 2, 3, 4, 16, 17, 19, 20]
    for numero in numeros:
        resultado = "primo" if eh_primo(numero) else "não primo"
        print(f"{numero} -> {resultado}")
```

- Esse bloco permite executar o script diretamente.
- Ele testa a função com alguns exemplos e imprime se cada número é primo ou não.

## Vantagens da versão clean code

- Funções pequenas e bem nomeadas tornam o código mais fácil de entender.
- O uso de helpers melhora a leitura e separa a lógica de validação.
- `math.isqrt` evita cálculos em ponto flutuante e deixa a verificação mais precisa.

## Complexidade

- A complexidade do algoritmo é aproximadamente `O(sqrt(n) / 6)`.
- Isso significa que, para números grandes, o tempo cresce proporcionalmente à raiz quadrada do valor.
