# Explicação dos erros em debug.py

1. Erro de sintaxe na entrada do preço do item 1
   - O comando `input(Preço do item 1? )` não usa aspas em torno da string de prompt, o que causa um erro de sintaxe.

2. Conversão incorreta do cupom de desconto
   - `desconto_cupom` é lido como string, mas em seguida é usado em operações matemáticas.
   - Para calcular o desconto corretamente, é necessário converter o valor para um número (`float` ou `int`).

3. Comparação inválida entre tipos diferentes
   - No `if desconto_cupom > 0:`, o código compara uma string com um número inteiro, o que gera erro de tipo.

4. Erro de indentação no bloco `if`
   - A linha `print(f" Desconto ({desconto_cupom:.0f}%): -R$ {desconto:.2f}")` deve estar indentada dentro do bloco `if`.

5. Saída incorreta do item 2
   - A linha `print(" Item 2:        R$ {total_item2:.2f}")` não está usando f-string, então ela exibe o texto literal em vez do valor calculado.
