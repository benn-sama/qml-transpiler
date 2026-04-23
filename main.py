from src.transpiler import Transpiler
import sys

#sys.argv[i]

if __name__ == "__main__":
  if len(sys.argv) < 2:
    raise Exception("No file provided!")
  
  transpiler = Transpiler()
  read_file  = sys.argv[1]
  write_file = sys.argv[2]
  

  try:
    with open(read_file, 'r') as f:
      read_file = f.read()
  except:
    raise Exception("File not found!")

  json = transpiler.parse(read_file)
  if json is None:
    raise Exception("An error has occurred!")

  write_file += ".json"
  with open(write_file, 'w') as f:
    f.write(json)