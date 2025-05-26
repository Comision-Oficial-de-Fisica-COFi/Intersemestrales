from pprint import pprint
import json, csv

unaccent_list = [('á', 'a'), ('é', 'e'), ('í', 'i'), ('ó', 'o'), ('ú', 'u')]
def unaccent(string):
    for original, replacement in unaccent_list:
        string = string.replace(original, replacement)
    return string

carrera = 'biomedica'
filename = f'cursos_{carrera}_raw.txt'

subjects_dict = {}
subjects_names = [['semestre', 'area', 'creditos', 'nombre']]
with open(filename, 'r') as f:
	data = f.readlines()

area = None
for line in data:
	line = line.replace('\n', '')
	if line == '': continue
	if "SEMESTRE" in line or "OPTATIVAS" in line or "PROFUNDIZACIÓN" in line:
		if "SEMESTRE" in line:
			area = "obligatoria"
			semestre = line.replace('SEMESTRE', '').replace(' ', '').lower()
		if "OPTATIVAS" in line:
			semestre = 'optativa'
		if "PROFUNDIZACIÓN" in line:
			semestre = 'profundizacion'
		key = unaccent(line)
		subjects_dict[key] = []
		continue
	if "--" in line:
		area = line.replace('--', '')
		continue
	creditos, nombre = int(line.split(' ')[0]), ' '.join(line.split(' ')[1:])
	nombre = unaccent(nombre.lower().replace('\n', '').strip())
	subjects_dict[key].append({'nombre': nombre, 'creditos': creditos, 'area': area})
	subjects_names.append([semestre, area, creditos, nombre])

with open(f'cursos_{carrera}_dict.json', 'w') as file:
	json.dump(subjects_dict, file, indent=4)

with open(f'cursos_{carrera}_nombres.csv', 'w', newline='') as file:
	writer = csv.writer(file)
	writer.writerows(subjects_names)
