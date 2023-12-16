# Encrypted File
 Código que permite fazer uma criptografia simples, a partir de parâmetros passados em uma linha de comandos de um terminal

 Flags/Parâmetros | Significado
 ---|---
 -f ou --full | Determina que todo o arquivo será encriptado
 -r ou --re | Estabelece o padrão regex cujas strings correspondentes serão encriptadas
 -k ou --key | Determina a chave a qual será utilizada para a criptografia
 filename | O diretório do arquivo que será encriptado

 __Obs:__ As flags "-f" e "-r" não podem ser utilizadas juntas, uma vez que "-r" especifica apenas um padrão de string (e não o texto por completo). Caso ambos sejam definidos na linha do terminal, apenas o "-f" será compilado.

## Inspiração do Código

Esse código foi baseado no código iheartxor, criado por Alexander Hanel, o qual pode ser visto [Aqui](https://hooked-on-mnemonics.blogspot.com/p/iheartxor.html). Na verdade, ele possui mais diferenças de sintaxe (Atualizada para as versões do Python mais recentes) do que de semântica em relação ao do criador.

## Imagens

Algumas imagens foram adquiridas do site [Pexels.com](https://www.pexels.com/), o qual trabalha com imagens sem direitos autorais, para servir de teste. Elas podem acessadas clicando nos nomes de seus produtores a seguir: [Mali Maeder](https://www.pexels.com/pt-br/foto/cavalo-preto-correndo-em-campo-verde-cercado-de-arvores-101667/) e [Jonas Kakaroto](https://www.pexels.com/pt-br/foto/empt-chair-lot-2914419/.)
