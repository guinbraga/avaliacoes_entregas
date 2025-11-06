nomes_pizzaria = []

with open("pizzaria_nomes.txt") as f:
    for line in f:
        line = line.strip()
        nomes_pizzaria.append(line)

print(nomes_pizzaria)
