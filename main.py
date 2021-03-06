import re
from flask import Flask
from flask import request, render_template, send_from_directory
import math



sch_weights = [0.5/7, 0.5/7, 0.5/7, 0.5/7, 0.5/7, 0.5/7, 0.5, 0.5/7]

mun_sch_weights = [1/7, 1/7, 1/7, 1/7, 1/7, 1/7, 0, 1/7]

lessons = {0: 'En', 1: 'Mat', 2: 'Deu', 3: 'Phy', 4: 'Bio', 5: 'Chemie'}

note_table = [138, 135, 132, 129, 126, 123, 120, 117, 114, 111, 108, 105, 102, 99, 96, 93, 90, 87, 84, 81, 78, 75,
              72, 69, 66, 63, 60, 57, 54, 51, 0]

app = Flask(__name__, static_url_path='/')


@app.route('/rickroll')
def rickroll():

    return render_template('rickroll.html')


@app.route('/robots.txt')
@app.route('/favicon.ico')
def static_from_root():
    return send_from_directory(app.static_folder, request.path[1:])



@app.route('/results', methods=['POST', 'GET'])
def results():
    if request.method == 'POST':
        results = request.form.to_dict().items()
        results_ = request.form.to_dict()

        entered_notes = []
        temp_lis = []
        print(results)

        if results_['mod'] == 'Halb':
            i = 0
            for key,value in results:
                if key == 'sch_abi':
                    break
                if i < 3:
                    temp_lis.append(value)
                    temp_lis.append(value)
                else:
                    temp_lis.append(value)
                i += 1

                if len(temp_lis) == 8:
                    i = 0
                    entered_notes.append(temp_lis)
                    temp_lis = []

        else:
            for key, value in results:
                if key == 'sch_abi':
                    break
                temp_lis.append(value)
                if len(temp_lis) == 8:
                    entered_notes.append(temp_lis)
                    temp_lis = []

        print(entered_notes)


        selections = {}
        for key, value in results:
            if key == 'sch_abi':
                selections['sch_abi'] = value
            if key == 'mun_abi':
                selections['mun_abi'] = value
            if key == 'mun2_abi':
                selections['mun2_abi'] = value
            if key == 'Mun1':
                selections['mun1'] = int(value)
            if key == 'Mun2' and selections['mun2_abi'] != 'non':
                selections['mun2'] = int(value)
        

        bestanden_check = True
        #print(entered_notes)

        for a in range(5):
            #print(entered_notes[a][6])
            if entered_notes[a][6] == '':
                continue

            if int(entered_notes[a][6]) == 0:
                #print("s????t??n aga")
                bestanden_check = False
                



        averages = calculate(entered_notes, selections)

        rounded_avg = round(averages, entered_notes, selections)

        sum_note = endnote(rounded_avg, selections)

        end_note = NC_(sum_note)

        toplam = 0
        for note in rounded_avg[0:3]:
            toplam += note
        
        for index, note in enumerate(rounded_avg[3:7]):

            if lessons[index + 3] == selections['sch_abi']:
                #print("eklendi")
                toplam += note


        if toplam < 20:
            bestanden_check = False

     
        for index, note in enumerate(rounded_avg[3:7]):

            if lessons[index + 3] == selections['mun_abi']:
                toplam += note

        if toplam < 30:
            bestanden_check = False

        sayac = 0
        dersler_4 = []
        for index,note in enumerate(rounded_avg):
            if note < 5:
                sayac += 1
                dersler_4.append(index)
        
        if sayac > 2:
            bestanden_check = False

        for i in rounded_avg:
            if i == 0:
                bestanden_check = False



        result = {}
        result['Englisch End Note'] = rounded_avg[0]
        result['Mathematik End Note'] = rounded_avg[1]
        result['Deutsch End Note'] = rounded_avg[2]
        result['Physik End Note'] = rounded_avg[3]
        result['Biologie End Note'] = rounded_avg[4]
        result['Chemie End Note'] = rounded_avg[5]
        result['Gesamptpunktzahl'] = sum_note
        if sum_note < 50:
            result['End Note'] = '--'
        else:

            result['End Note'] = end_note

        if end_note < 4.0 and bestanden_check:
            result['Bestanden ?'] = 'JA'
        else:
            result['Bestanden ?'] = 'NEIN'

        return render_template('results.html', result=result)


@app.route('/input_detailed')
def notes():
    return render_template('input_notes.html')


@app.route('/')
def results_halb():

    return render_template('input_notes_halb.html')


def weig_avg(numbers, weights):
    i = 0
    sum = 0

    for val in numbers:
        try:
            sum += int(val) * weights[i]
        except:
            print(0)
        i += 1

    return sum


def calculate(input_notes, selection):
    final_notes = []

    for index, not_lis in enumerate(input_notes):
        lesson = lessons[index]

        if(index <= 2 and selection['mun2_abi'] != lesson):
            final_notes.append(weig_avg(not_lis, sch_weights))

        if(index <= 2 and selection['mun2_abi'] == lesson):
            final_notes.append(
                (((weig_avg(not_lis, mun_sch_weights) + selection['mun2']) / 2) + int(not_lis[6])) / 2)

        if(index > 2 and (selection['sch_abi'] == lesson) and (selection['mun_abi'] != lesson) and (selection['mun2_abi'] != lesson)):
            final_notes.append(weig_avg(not_lis, sch_weights))

        if(index > 2 and (selection['sch_abi'] == lesson) and (selection['mun_abi'] == lesson)):
            final_notes.append((weig_avg(not_lis, mun_sch_weights) +
                               int(selection['mun1'])) + (2 * int(not_lis[6])) / 4)

        if(index > 2 and (selection['sch_abi'] == lesson) and (selection['mun2_abi'] == lesson)):
            final_notes.append((weig_avg(not_lis, mun_sch_weights) +
                               selection['mun2'] + (2 * int(not_lis[6]))) / 4)

        if(index > 2 and (selection['sch_abi'] != lesson) and (selection['mun_abi'] == lesson) and (selection['mun2_abi'] != lesson)):
            final_notes.append(
                (weig_avg(not_lis, mun_sch_weights) + selection['mun1']) / 2)

        if(index > 2 and (selection['sch_abi'] != lesson) and (selection['mun_abi'] != lesson) and (selection['mun2_abi'] == lesson)):
            final_notes.append(
                (weig_avg(not_lis, mun_sch_weights) + selection['mun2']) / 2)

        if(index > 2 and (selection['sch_abi'] != lesson) and (selection['mun_abi'] != lesson) and (selection['mun2_abi'] != lesson)):
            final_notes.append(weig_avg(not_lis, mun_sch_weights))

    #print(final_notes)
    return final_notes


def round(averages, input_notes, selection):
    rounded_avg = []

    for i, val in enumerate(averages[0:3]):
        if int(input_notes[i][6]) >= val:
            rounded_avg.append(math.ceil(val))
        if val > int(input_notes[i][6]):
            rounded_avg.append(math.floor(val))

        #print("Averaged Note : {} Abitur Note: : {}".format(
         #   val, int(input_notes[i][6])))

    for i, val in enumerate(averages[3:], start=3):
        if lessons[i] == selection['sch_abi']:
            if int(input_notes[i][6]) >= val:
                rounded_avg.append(math.ceil(val))
            if val > int(input_notes[i][6]):
                rounded_avg.append(math.floor(val))
        else:
            rounded_avg.append(math.ceil(val))

    #print(rounded_avg)
    return rounded_avg


def endnote(rounded_avg, selection):
    sum = 0

    for val in rounded_avg[0:3]:
        sum += val * 2

    for i, val in enumerate(rounded_avg[3:], start=3):
        if lessons[i] == selection['sch_abi']:
            sum += val * 2
        else:
            sum += val

    return sum


def NC_(sum_note):
    for i, val in enumerate(note_table):
        if sum_note >= val:
            return 1.0 + i / 10
