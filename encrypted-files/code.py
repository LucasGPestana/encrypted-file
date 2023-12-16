import re
import sys, os
import argparse

"""
O código a seguir permite com que se possa encodar strings dentro de um arquivo que correspondem a um padrão regex estabelecido como parâmetro --re na linha de comando, ou todo seu conteúdo estabelecendo --full como parâmetro na linha de comando
"""

def valid_ascii(char):

  # Verifica se o caractere passado como parâmetro corresponde a um caractere ascii
  if char.isascii():

    return True
  
  else:

    return False

def xor(data, key):
  
  # Percorre todos os bytes em hexadecimal de data , concatenando à decode o caractere unicode correspondente ao XOR entre o valor decimal do byte em hexadecimal atual e a chave

  # Data é iterado pelos valores unicodes de cada byte em hexadecimal (Ou seja, byte será um str ou int)

  # Caso byte seja int, em vez de pegar o valor decimal do caractere unicode para realizar a operação XOR, e depois pegar o caractere unicode correspondente ao resultado da operação, a operação será realizada diretamente com o byte sem converter o decimal para caractere

  if not isinstance(data, int):

    decode = "".join([chr(ord(byte) ^ key) if not isinstance(byte, int) else chr(byte ^ key) for byte in data])
  
  else:

    decode = chr(data ^ key)
  
  return decode

def main(argv):

  usage = "(Uso) iheartxor.py [options] <file>"
  parser = argparse.ArgumentParser(usage=usage)
  
  # Flags adicionadas para referenciar os argumentos passados na linha de comando
  parser.add_argument("-k", "--key", action="store", dest="key", type=str, help="Static XOR key to use (Chave XOR estática para uso)")
  parser.add_argument("-f", "--full", action="store_true", dest="full", help="XOR full file (Arquivo XOR completo)")
  parser.add_argument("-r", "--re", action="store", dest="pattern", type=str, help="Regular Expression Pattern to search for (Padrão de Expressão Regular para pesquisa)")
  parser.add_argument("filename", action="store", help="File directory (Diretório do arquivo)")

  namespace = parser.parse_args()

  if len(argv) < 2:

    parser.print_help()

    return # None é retornado do main

  try:

    file = open(namespace.filename, "rb")

  except FileNotFoundError:

    print("[ERROR] FILE CAN NOT BE OPENED OR READ! ([ERRO] O ARQUIVO NÃO PODE SER ABERTO OU LIDO!)")

    file.close()

    return
  
  # Verifica se o parâmetro full foi passado e a chave XOR não
  if namespace.full == True and namespace.key == None:

    print("[ERROR] --FULL OPTION MUST INCLUDE XOR KEY ([ERRO] A FLAG --FULL DEVE INCLUIR UMA CHAVE XOR)")

    file.close()

    return
  
  if namespace.full == True and namespace.key != None:

    key = int(namespace.key, 16)

    print(xor(file.read(), key), file=open(f"encrypted-file{os.path.splitext(namespace.filename)[1]}", "w", encoding="utf-8"))

    file.close()

    return
  
  # Caso o parâmetro de padrão regex não seja passado
  if namespace.pattern == None:

    # A string corresponderá ao padrão definido se:
      # Apresentar um byte nulo na base hexadecimal no início
      # Não apresentar um byte nulo na base decimal imediatamente após esse anterior (Negação de lockahead)
      # Apresentar qualquer caractere após o primeiro byte nulo (No qual será sempre pego o mínimo de caracteres)
      # Finaliza com outro byte nulo na base hexadecimal
    regex = re.compile(r"\x00(?!\x00).+?\x00".encode())
  
  else:

    try:

      regex = re.compile(fr"{namespace.pattern}".encode())
    
    except Exception:

      print("[ERROR] INVALID REGULAR EXPRESSION PATTERN ([ERRO] PADRÃO DE EXPRESSÃO REGULAR INVÁLIDO)")

      file.close()

      return
  
  buff = ""

  # corresmatch = correspondence (Correspondência) match, que é um objeto Match
  for corresmatch in regex.finditer(file.read()):

    if len(corresmatch.group()) < 8:

      continue

    if namespace.key == None:

      # Para cada chave entre 0x1 (1 em decimal) e 0xFF (255 em decimal)
      for key in range(1, 256):

        # Para cada byte (Correspondente a dois caracteres hexadecimais) dentro da substring byte-like correspondente ao padrão regex
        for byte in corresmatch.group():

          if byte == "\x00":

            buff += byte
            continue

          else:

            # Como o byte corresponde a apenas um caractere (ascii ou não), quando for iterado na função xor, ele terá apenas uma repetição
            decode = xor(byte, key)

            if valid_ascii(decode):

              buff = ""

              break

            else:

              buff += decode

        # Se o buffer não estiver vazio, a posição do primeiro elemento da string correspondente no texto do arquivo será mostrado em hexadecimal, assim como a chave (também em hexadecimal) e o buffer (com os bytes decodados)
        # O buffer será esvaziado para o próximo valor da chave a ser considerado
        if buff != "":

          print(f"{hex(corresmatch.start())} key {hex(key)} {buff}", file=open(f"encrypted-file{os.path.splitext(namespace.filename)[1]}", "w", encoding="utf-8"))

          buff = ""

    else:

      # Converte a chave para o valor de base decimal correspondente ao mesmo valor na base hexadecimal
      key = int(namespace.key, 16)

      for byte in corresmatch.group():
        
        # Caso o byte da string (byte-like) correspondente ao regex seja nulo, ele será apenas adicionado ao buffer
        if byte == "\x00":

          buff += byte
          continue
        
        # Caso o byte da string (byte-like) não seja nula, esse byte será encodado com o operador XOR, a partir da chave estabelecida como parâmetro
        else:

          decode = xor(byte, key)

          # Caso seja encontrado um byte dentro da string que não é um caractere ascii, o buffer será esvaziado e sairá do laço
          # Caso contrário, o byte decodado será adicionado ao buffer e o laço dos bytes na string correspondente será continuado
          if not valid_ascii(decode):

            buff = ""
            break

          else:

            buff += decode

      if buff != "":

        print(f"{hex(corresmatch.start())} key {hex(key)} {buff}", file=open(f"encrypted-file{os.path.splitext(namespace.filename)[1]}", "w", encoding="utf-8"))

  
  file.close()

  return

if __name__ == "__main__":

  main(sys.argv[1:])







  






