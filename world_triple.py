import csv

id_name = '<http://www.kbqa.com/alltime_world_2020_04_04/id_{}> <http://www.kbqa.com/alltime_world_2020_04_04/properties#name> "{}".'

id_lastUpdateTime = "<http://www.kbqa.com/alltime_world_2020_04_04/id_{}> <http://www.kbqa.com/alltime_world_2020_04_04/properties#lastUpdateTime> <http://www.kbqa.com/alltime_world_2020_04_04/{}> ."
lastUpdateTime_num = '<http://www.kbqa.com/alltime_world_2020_04_04/{}> <http://www.kbqa.com/alltime_world_2020_04_04/properties#lastUpdateTime_num> "{}".'

id_total_confirm = "<http://www.kbqa.com/alltime_world_2020_04_04/id_{}> <http://www.kbqa.com/alltime_world_2020_04_04/properties#total_confirm> <http://www.kbqa.com/alltime_world_2020_04_04/{}> ."
total_confirm_num = '<http://www.kbqa.com/alltime_world_2020_04_04/{}> <http://www.kbqa.com/alltime_world_2020_04_04/properties#total_confirm_num> "{}"^^<http://www.w3.org/2001/XMLSchema#integer> .'

id_total_suspect = "<http://www.kbqa.com/alltime_world_2020_04_04/id_{}> <http://www.kbqa.com/alltime_world_2020_04_04/properties#total_suspect> <http://www.kbqa.com/alltime_world_2020_04_04/{}> ."
total_suspect_num = '<http://www.kbqa.com/alltime_world_2020_04_04/{}> <http://www.kbqa.com/alltime_world_2020_04_04/properties#total_suspect_num> "{}"^^<http://www.w3.org/2001/XMLSchema#integer> .'

id_total_heal = "<http://www.kbqa.com/alltime_world_2020_04_04/id_{}> <http://www.kbqa.com/alltime_world_2020_04_04/properties#total_heal> <http://www.kbqa.com/alltime_world_2020_04_04/{}> ."
total_heal_num = '<http://www.kbqa.com/alltime_world_2020_04_04/{}> <http://www.kbqa.com/alltime_world_2020_04_04/properties#total_heal_num> "{}"^^<http://www.w3.org/2001/XMLSchema#integer> .'

id_total_dead = "<http://www.kbqa.com/alltime_world_2020_04_04/id_{}> <http://www.kbqa.com/alltime_world_2020_04_04/properties#total_dead> <http://www.kbqa.com/alltime_world_2020_04_04/{}> ."
total_dead_num = '<http://www.kbqa.com/alltime_world_2020_04_04/{}> <http://www.kbqa.com/alltime_world_2020_04_04/properties#total_dead_num> "{}"^^<http://www.w3.org/2001/XMLSchema#integer> .'

id_today_confirm = "<http://www.kbqa.com/alltime_world_2020_04_04/id_{}> <http://www.kbqa.com/alltime_world_2020_04_04/properties#today_confirm> <http://www.kbqa.com/alltime_world_2020_04_04/{}> ."
today_confirm_num = '<http://www.kbqa.com/alltime_world_2020_04_04/{}> <http://www.kbqa.com/alltime_world_2020_04_04/properties#today_confirm_num> "{}"^^<http://www.w3.org/2001/XMLSchema#integer> .'

id_today_suspect = "<http://www.kbqa.com/alltime_world_2020_04_04/id_{}> <http://www.kbqa.com/alltime_world_2020_04_04/properties#today_suspect> <http://www.kbqa.com/alltime_world_2020_04_04/{}> ."
today_suspect_num = '<http://www.kbqa.com/alltime_world_2020_04_04/{}> <http://www.kbqa.com/alltime_world_2020_04_04/properties#today_suspect_num> "{}"^^<http://www.w3.org/2001/XMLSchema#integer> .'

id_today_heal = "<http://www.kbqa.com/alltime_world_2020_04_04/id_{}> <http://www.kbqa.com/alltime_world_2020_04_04/properties#today_heal> <http://www.kbqa.com/alltime_world_2020_04_04/{}> ."
today_heal_num = '<http://www.kbqa.com/alltime_world_2020_04_04/{}> <http://www.kbqa.com/alltime_world_2020_04_04/properties#today_heal_num> "{}"^^<http://www.w3.org/2001/XMLSchema#integer> .'

id_today_dead = "<http://www.kbqa.com/alltime_world_2020_04_04/id_{}> <http://www.kbqa.com/alltime_world_2020_04_04/properties#today_dead> <http://www.kbqa.com/alltime_world_2020_04_04/{}> ."
today_dead_num = '<http://www.kbqa.com/alltime_world_2020_04_04/{}> <http://www.kbqa.com/alltime_world_2020_04_04/properties#today_dead_num> "{}"^^<http://www.w3.org/2001/XMLSchema#integer> .'

triples = []

i = 0 #计数器
f = open('alltime_world_2020_05_07.csv','r',encoding='utf-8')
reader = csv.reader(f)
for row in reader:
    i = i + 1

    id_name_str = id_name.format(i, row[0])
    triples.append(id_name_str)

    id_lastUpdateTime_str = id_lastUpdateTime.format(i, row[1])
    triples.append(id_lastUpdateTime_str)

    lastUpdateTime_num_str = lastUpdateTime_num.format(row[1], row[1])
    triples.append(lastUpdateTime_num_str)

    id_total_confirm_str = id_total_confirm.format(i, row[2])
    triples.append(id_total_confirm_str)

    total_confirm_num_str = total_confirm_num.format(row[2], row[2])
    triples.append(total_confirm_num_str)

    id_total_suspect_str = id_total_suspect.format(i, row[3])
    triples.append(id_total_suspect_str)

    total_suspect_num_str = total_suspect_num.format(row[3], row[3])
    triples.append(total_suspect_num_str)

    id_total_heal_str = id_total_heal.format(i, row[4])
    triples.append(id_total_heal_str)

    total_heal_num_str = total_heal_num.format(row[4], row[4])
    triples.append(total_heal_num_str)

    id_total_dead_str = id_total_dead.format(i, row[5])
    triples.append(id_total_dead_str)

    total_dead_num_str = total_dead_num.format(row[5], row[5])
    triples.append(total_dead_num_str)

    id_today_confirm_str = id_today_confirm.format(i, row[6])
    triples.append(id_today_confirm_str)

    today_confirm_num_str = today_confirm_num.format(row[6], row[6])
    triples.append(today_confirm_num_str)

    id_today_suspect_str = id_today_suspect.format(i, row[7])
    triples.append(id_today_suspect_str)

    today_suspect_num_str = today_suspect_num.format(row[7], row[7])
    triples.append(today_suspect_num_str)

    id_today_heal_str = id_today_heal.format(i, row[8])
    triples.append(id_today_heal_str)

    today_heal_num_str = today_heal_num.format(row[8], row[8])
    triples.append(today_heal_num_str)

    id_today_dead_str = id_today_dead.format(i, row[9])
    triples.append(id_today_dead_str)

    today_dead_num_str = today_dead_num.format(row[9], row[9])
    triples.append(today_dead_num_str)

filename = r'epidemic_world.txt'
with open(filename,"w+",encoding='utf-8') as fd:
    fd.write("\n".join(triples))
fd.close()