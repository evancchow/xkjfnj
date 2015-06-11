with open("constitute_countries_links.csv", 'rb') as f:
    data = [i for i in f]

data = [i for i in data if "https://www.constituteproject.org/constitution" in i]

with open("constitution_links.csv", "wb") as f:
    for line in data:
        f.write(line)

        