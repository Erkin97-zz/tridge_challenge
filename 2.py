# python3
import csv
import re

attributes = set()
products = set()
items = list()

# edited version of in function
def is_word_in_text(word: str, text: str):
  word = word.lower().strip()
  text = text.lower().strip()
  begin = 0
  size_w = len(word)
  size_t = len(text)

  while(True):
    pos = text.find(word, begin)
    if (pos == -1):
      break
    # check if found is not substring
    if (pos != 0 and text[pos - 1].isspace() or pos == 0):
      if (pos + size_w < size_t and text[pos + size_w].isspace() or pos + size_w == size_t):
        return True
      else: # check plural suffix 's' and 'es'
        if (text[pos + size_w] == 's'):
          if (pos + size_w + 1 < size_t and text[pos + size_w + 1].isspace() or pos + size_w + 1 == size_t):
            return True
        elif (text[pos + size_w] == 'e'):
          pos += 1
          if (text[pos + size_w] == 's'):
            if (pos + size_w + 1 < size_t and text[pos + size_w + 1].isspace() or pos + size_w + 1 == size_t):
              return True
          pos -= 1
    begin = pos + size_w
      
  return False

def initialize():
  with open('attributes.csv') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    F = True
    for row in csv_reader:
      if (F):
        F = not F #skip first line
        continue
      products.add(row[0])
      attributes.add(row[1])

  with open('products.csv') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    F = True
    for row in csv_reader:
      if (F):
        F = not F #skip first line
        continue
      products.add(row[0])
  
  with open('data.csv') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    F = True
    for row in csv_reader:
      if (F):
        F = not F #skip first line
        continue
      items.append(row[0])

def find_product(item):
  for product in products:
    if (is_word_in_text(product, item)):
      return product

# extract all attributes for item
def find_attr(item):
  item = item.lower().strip()
  all_attr = set()

  for attr in attributes:
    if is_word_in_text(attr, item):
      all_attr.add(attr.strip())
    else: # check for similar attributes ->> main_attr(=atrr1=atrr2=atrr3)
      similar_attr_re = re.search(r'\((.*?)\)', attr)
      if (similar_attr_re == None):
        continue
      similar_attr_re = similar_attr_re.group(1)
      main_attr = attr.replace('(' + similar_attr_re + ')','')

      if is_word_in_text(main_attr, item):
        all_attr.add(main_attr.strip())
      else:
        if (similar_attr_re[0] == '='):
          similar_attr_re = similar_attr_re[1:]
        similar_attr_list = similar_attr_re.split('=')
        for similar_attr in similar_attr_list:
          if is_word_in_text(similar_attr, item):
            all_attr.add(main_attr.strip())

  attr_str_result = '' # follow format for attributes
  for attr in all_attr:
    attr_str_result += attr + " \\ "
  return attr_str_result[:-3]

if __name__ == '__main__':
  initialize()
  attributes.remove('')
  products.remove('')

  with open('data_parsed.csv', mode='w', newline='') as data_file:
    data_writer = csv.writer(data_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)  
    data_writer.writerow(["Data", "Product", "Attributes"])
    for item in items:
      product = find_product(item)
      attr = find_attr(item)
      data_writer.writerow([item, product, attr])