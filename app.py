from flask import Flask, render_template, request, redirect, url_for, flash, render_template_string
from flask import Markup
import skfuzzy as fz
from skfuzzy import control as ctrl
import numpy as np
import pandas as pd
from datetime import datetime


app = Flask(__name__)
app.secret_key = '4907aba7a49517d29e8a08f52571dcd4'

@app.route('/', methods = ['GET','POST'])
def main():
    if request.method == 'POST':
        if request.form['tekanan-darah'] == "" or request.form['gula-darah'] == "" or request.form['kolesterol'] == "" or request.form['bmi'] == "" or request.form['riwayat'] == "":
            flash('Inputan tidak boleh kosong')
            return render_template('utama.html')
        else:
            #inisiasi variabel
            Tekdar = ctrl.Antecedent(np.arange(0,200,1),'Tekanan Darah')
            Guldar = ctrl.Antecedent(np.arange(0,200,1),'Gula Darah')
            Koles = ctrl.Antecedent(np.arange(0,300,1),'Kolesterol')
            BMI = ctrl.Antecedent(np.arange(0,30,1),'Body Mass Index') 
            Riwa = ctrl.Antecedent(np.arange(0,2,1),'Riwayat')
            Hasil = ctrl.Consequent(np.arange(0,10,1),'Hasil')

            #Fungsi Keanggotaan Tekanan Darah
            Tekdar['Rendah'] = fz.trapmf(Tekdar.universe,[0,0,110,120])
            Tekdar['Normal'] = fz.trimf(Tekdar.universe,[110,120,140])
            Tekdar['Tinggi'] = fz.trapmf(Tekdar.universe,[120,140,200,200])
            
            #Fungsi Keanggotaan Gula Darah
            Guldar['Rendah'] = fz.trapmf(Guldar.universe,[0,0,70,110])
            Guldar['Normal'] = fz.trimf(Guldar.universe,[70,110,140])
            Guldar['Tinggi'] = fz.trapmf(Guldar.universe,[110,140,200,200])
            

            #Fungsi Keanggotaan Kolesterol
            Koles['Rendah'] = fz.trapmf(Koles.universe,[0,0,200,240])
            Koles['Normal'] = fz.trimf(Koles.universe,[200,240,250])
            Koles['Tinggi'] = fz.trapmf(Koles.universe,[240,250,300,300])


            #Fungsi Keanggotaan Body Mass Index
            BMI['Kurus'] = fz.trapmf(BMI.universe,[0,0,18,23])
            BMI['Normal'] = fz.trimf(BMI.universe,[18,23,25])
            BMI['Obesitas'] = fz.trapmf(BMI.universe,[23,25,30,30])
            

            #Fungsi Keanggotaan Riwayat
            Riwa['Tidak'] = fz.trapmf(Riwa.universe,[0,0,0,1])
            Riwa['Ada'] = fz.trapmf(Riwa.universe,[1,1,1,1])
            

            #Fungsi Keanggotaan Hasil
            Hasil['Kecil'] = fz.trapmf(Hasil.universe,[0,0,4,7])
            Hasil['Sedang'] = fz.trimf(Hasil.universe,[4,7,9])
            Hasil['Besar'] = fz.trapmf(Hasil.universe,[7,9,10,10])


            #Rule
            Rb1 = ctrl.Rule(Tekdar['Rendah'] & Guldar['Rendah'] & Koles['Rendah'] & BMI['Kurus'] & Riwa['Ada'], Hasil['Sedang'])
            Rb2 = ctrl.Rule(Tekdar['Rendah'] & Guldar['Rendah'] & Koles['Rendah'] & BMI['Kurus'] & Riwa['Tidak'], Hasil['Kecil'])
            Rb3 = ctrl.Rule(Tekdar['Rendah'] & Guldar['Rendah'] & Koles['Rendah'] & BMI['Normal'] & Riwa['Ada'], Hasil['Sedang'])
            Rb4 = ctrl.Rule(Tekdar['Rendah'] & Guldar['Rendah'] & Koles['Rendah'] & BMI['Normal'] & Riwa['Tidak'], Hasil['Kecil'])
            Rb5 = ctrl.Rule(Tekdar['Rendah'] & Guldar['Rendah'] & Koles['Rendah'] & BMI['Obesitas'] & Riwa['Ada'], Hasil['Besar'])
            Rb6 = ctrl.Rule(Tekdar['Rendah'] & Guldar['Rendah'] & Koles['Rendah'] & BMI['Obesitas'] & Riwa['Tidak'], Hasil['Sedang'])
            Rb7 = ctrl.Rule(Tekdar['Rendah'] & Guldar['Rendah'] & Koles['Normal'] & BMI['Kurus'] & Riwa['Ada'], Hasil['Kecil'])
            Rb8 = ctrl.Rule(Tekdar['Rendah'] & Guldar['Rendah'] & Koles['Normal'] & BMI['Kurus'] & Riwa['Tidak'], Hasil['Kecil'])
            Rb9 = ctrl.Rule(Tekdar['Rendah'] & Guldar['Rendah'] & Koles['Normal'] & BMI['Normal'] & Riwa['Ada'], Hasil['Sedang'])
            Rb10 = ctrl.Rule(Tekdar['Rendah'] & Guldar['Rendah'] & Koles['Normal'] & BMI['Normal'] & Riwa['Tidak'], Hasil['Kecil'])
            Rb11 = ctrl.Rule(Tekdar['Rendah'] & Guldar['Rendah'] & Koles['Normal'] & BMI['Obesitas'] & Riwa['Ada'], Hasil['Besar'])
            Rb12 = ctrl.Rule(Tekdar['Rendah'] & Guldar['Rendah'] & Koles['Normal'] & BMI['Obesitas'] & Riwa['Tidak'], Hasil['Sedang'])
            Rb13 = ctrl.Rule(Tekdar['Rendah'] & Guldar['Rendah'] & Koles['Tinggi'] & BMI['Kurus'] & Riwa['Ada'], Hasil['Besar'])
            Rb14 = ctrl.Rule(Tekdar['Rendah'] & Guldar['Rendah'] & Koles['Tinggi'] & BMI['Kurus'] & Riwa['Tidak'], Hasil['Sedang'])
            Rb15 = ctrl.Rule(Tekdar['Rendah'] & Guldar['Rendah'] & Koles['Tinggi'] & BMI['Normal'] & Riwa['Ada'], Hasil['Besar'])
            Rb16 = ctrl.Rule(Tekdar['Rendah'] & Guldar['Rendah'] & Koles['Tinggi'] & BMI['Normal'] & Riwa['Tidak'], Hasil['Sedang'])
            Rb17 = ctrl.Rule(Tekdar['Rendah'] & Guldar['Rendah'] & Koles['Tinggi'] & BMI['Obesitas'] & Riwa['Ada'], Hasil['Besar'])
            Rb18 = ctrl.Rule(Tekdar['Rendah'] & Guldar['Rendah'] & Koles['Tinggi'] & BMI['Obesitas'] & Riwa['Tidak'], Hasil['Besar'])
            Rb19 = ctrl.Rule(Tekdar['Rendah'] & Guldar['Normal'] & Koles['Rendah'] & BMI['Kurus'] & Riwa['Ada'], Hasil['Sedang'])
            Rb20 = ctrl.Rule(Tekdar['Rendah'] & Guldar['Normal'] & Koles['Rendah'] & BMI['Kurus'] & Riwa['Tidak'], Hasil['Kecil'])
            Rb21 = ctrl.Rule(Tekdar['Rendah'] & Guldar['Normal'] & Koles['Rendah'] & BMI['Normal'] & Riwa['Ada'], Hasil['Sedang'])
            Rb22 = ctrl.Rule(Tekdar['Rendah'] & Guldar['Normal'] & Koles['Rendah'] & BMI['Normal'] & Riwa['Tidak'], Hasil['Kecil'])
            Rb23 = ctrl.Rule(Tekdar['Rendah'] & Guldar['Normal'] & Koles['Rendah'] & BMI['Obesitas'] & Riwa['Ada'], Hasil['Besar'])
            Rb24 = ctrl.Rule(Tekdar['Rendah'] & Guldar['Normal'] & Koles['Rendah'] & BMI['Obesitas'] & Riwa['Tidak'], Hasil['Sedang'])
            Rb25 = ctrl.Rule(Tekdar['Rendah'] & Guldar['Normal'] & Koles['Normal'] & BMI['Kurus'] & Riwa['Ada'], Hasil['Sedang'])
            Rb26 = ctrl.Rule(Tekdar['Rendah'] & Guldar['Normal'] & Koles['Normal'] & BMI['Kurus'] & Riwa['Tidak'], Hasil['Kecil'])
            Rb27 = ctrl.Rule(Tekdar['Rendah'] & Guldar['Normal'] & Koles['Normal'] & BMI['Normal'] & Riwa['Ada'], Hasil['Sedang'])
            Rb28 = ctrl.Rule(Tekdar['Rendah'] & Guldar['Normal'] & Koles['Normal'] & BMI['Normal'] & Riwa['Tidak'], Hasil['Kecil'])
            Rb29 = ctrl.Rule(Tekdar['Rendah'] & Guldar['Normal'] & Koles['Normal'] & BMI['Obesitas'] & Riwa['Ada'], Hasil['Besar'])
            Rb30 = ctrl.Rule(Tekdar['Rendah'] & Guldar['Normal'] & Koles['Normal'] & BMI['Obesitas'] & Riwa['Tidak'], Hasil['Sedang'])
            Rb31 = ctrl.Rule(Tekdar['Rendah'] & Guldar['Normal'] & Koles['Tinggi'] & BMI['Kurus'] & Riwa['Ada'], Hasil['Besar'])
            Rb32 = ctrl.Rule(Tekdar['Rendah'] & Guldar['Normal'] & Koles['Tinggi'] & BMI['Kurus'] & Riwa['Tidak'], Hasil['Sedang'])
            Rb33 = ctrl.Rule(Tekdar['Rendah'] & Guldar['Normal'] & Koles['Tinggi'] & BMI['Normal'] & Riwa['Ada'], Hasil['Besar'])
            Rb34 = ctrl.Rule(Tekdar['Rendah'] & Guldar['Normal'] & Koles['Tinggi'] & BMI['Normal'] & Riwa['Tidak'], Hasil['Sedang'])
            Rb35 = ctrl.Rule(Tekdar['Rendah'] & Guldar['Normal'] & Koles['Tinggi'] & BMI['Obesitas'] & Riwa['Ada'], Hasil['Besar'])
            Rb36 = ctrl.Rule(Tekdar['Rendah'] & Guldar['Normal'] & Koles['Tinggi'] & BMI['Obesitas'] & Riwa['Tidak'], Hasil['Besar'])
            Rb37 = ctrl.Rule(Tekdar['Rendah'] & Guldar['Tinggi'] & Koles['Rendah'] & BMI['Kurus'] & Riwa['Ada'], Hasil['Besar'])
            Rb38 = ctrl.Rule(Tekdar['Rendah'] & Guldar['Tinggi'] & Koles['Rendah'] & BMI['Kurus'] & Riwa['Tidak'], Hasil['Sedang'])
            Rb39 = ctrl.Rule(Tekdar['Rendah'] & Guldar['Tinggi'] & Koles['Rendah'] & BMI['Normal'] & Riwa['Ada'], Hasil['Besar'])
            Rb40 = ctrl.Rule(Tekdar['Rendah'] & Guldar['Tinggi'] & Koles['Rendah'] & BMI['Normal'] & Riwa['Tidak'], Hasil['Besar'])
            Rb41 = ctrl.Rule(Tekdar['Rendah'] & Guldar['Tinggi'] & Koles['Rendah'] & BMI['Obesitas'] & Riwa['Ada'], Hasil['Besar'])
            Rb42 = ctrl.Rule(Tekdar['Rendah'] & Guldar['Tinggi'] & Koles['Rendah'] & BMI['Obesitas'] & Riwa['Tidak'], Hasil['Besar'])
            Rb43 = ctrl.Rule(Tekdar['Rendah'] & Guldar['Tinggi'] & Koles['Normal'] & BMI['Kurus'] & Riwa['Ada'], Hasil['Besar'])
            Rb44 = ctrl.Rule(Tekdar['Rendah'] & Guldar['Tinggi'] & Koles['Normal'] & BMI['Kurus'] & Riwa['Tidak'], Hasil['Sedang'])
            Rb45 = ctrl.Rule(Tekdar['Rendah'] & Guldar['Tinggi'] & Koles['Normal'] & BMI['Normal'] & Riwa['Ada'], Hasil['Besar'])
            Rb46 = ctrl.Rule(Tekdar['Rendah'] & Guldar['Tinggi'] & Koles['Normal'] & BMI['Normal'] & Riwa['Tidak'], Hasil['Sedang'])
            Rb47 = ctrl.Rule(Tekdar['Rendah'] & Guldar['Tinggi'] & Koles['Normal'] & BMI['Obesitas'] & Riwa['Ada'], Hasil['Besar'])
            Rb48 = ctrl.Rule(Tekdar['Rendah'] & Guldar['Tinggi'] & Koles['Normal'] & BMI['Obesitas'] & Riwa['Tidak'], Hasil['Besar'])
            Rb49 = ctrl.Rule(Tekdar['Rendah'] & Guldar['Tinggi'] & Koles['Tinggi'] & BMI['Kurus'] & Riwa['Ada'], Hasil['Besar'])
            Rb50 = ctrl.Rule(Tekdar['Rendah'] & Guldar['Tinggi'] & Koles['Tinggi'] & BMI['Kurus'] & Riwa['Tidak'], Hasil['Besar'])
            Rb51 = ctrl.Rule(Tekdar['Rendah'] & Guldar['Tinggi'] & Koles['Tinggi'] & BMI['Normal'] & Riwa['Ada'], Hasil['Besar'])
            Rb52 = ctrl.Rule(Tekdar['Rendah'] & Guldar['Tinggi'] & Koles['Tinggi'] & BMI['Normal'] & Riwa['Tidak'], Hasil['Besar'])
            Rb53 = ctrl.Rule(Tekdar['Rendah'] & Guldar['Tinggi'] & Koles['Tinggi'] & BMI['Obesitas'] & Riwa['Ada'], Hasil['Besar'])
            Rb54 = ctrl.Rule(Tekdar['Rendah'] & Guldar['Tinggi'] & Koles['Tinggi'] & BMI['Obesitas'] & Riwa['Tidak'], Hasil['Besar'])
            Rb55 = ctrl.Rule(Tekdar['Normal'] & Guldar['Rendah'] & Koles['Rendah'] & BMI['Kurus'] & Riwa['Ada'], Hasil['Kecil'])
            Rb56 = ctrl.Rule(Tekdar['Normal'] & Guldar['Rendah'] & Koles['Rendah'] & BMI['Kurus'] & Riwa['Tidak'], Hasil['Kecil'])
            Rb57 = ctrl.Rule(Tekdar['Normal'] & Guldar['Rendah'] & Koles['Rendah'] & BMI['Normal'] & Riwa['Ada'], Hasil['Kecil'])
            Rb58 = ctrl.Rule(Tekdar['Normal'] & Guldar['Rendah'] & Koles['Rendah'] & BMI['Normal'] & Riwa['Tidak'], Hasil['Kecil'])
            Rb59 = ctrl.Rule(Tekdar['Normal'] & Guldar['Rendah'] & Koles['Rendah'] & BMI['Obesitas'] & Riwa['Ada'], Hasil['Sedang'])
            Rb60 = ctrl.Rule(Tekdar['Normal'] & Guldar['Rendah'] & Koles['Rendah'] & BMI['Obesitas'] & Riwa['Tidak'], Hasil['Kecil'])
            Rb61 = ctrl.Rule(Tekdar['Normal'] & Guldar['Rendah'] & Koles['Normal'] & BMI['Kurus'] & Riwa['Ada'], Hasil['Kecil'])
            Rb62 = ctrl.Rule(Tekdar['Normal'] & Guldar['Rendah'] & Koles['Normal'] & BMI['Kurus'] & Riwa['Tidak'], Hasil['Kecil'])
            Rb63 = ctrl.Rule(Tekdar['Normal'] & Guldar['Rendah'] & Koles['Normal'] & BMI['Normal'] & Riwa['Ada'], Hasil['Kecil'])
            Rb64 = ctrl.Rule(Tekdar['Normal'] & Guldar['Rendah'] & Koles['Normal'] & BMI['Normal'] & Riwa['Tidak'], Hasil['Kecil'])
            Rb65 = ctrl.Rule(Tekdar['Normal'] & Guldar['Rendah'] & Koles['Normal'] & BMI['Obesitas'] & Riwa['Ada'], Hasil['Sedang'])
            Rb66 = ctrl.Rule(Tekdar['Normal'] & Guldar['Rendah'] & Koles['Normal'] & BMI['Obesitas'] & Riwa['Tidak'], Hasil['Kecil'])
            Rb67 = ctrl.Rule(Tekdar['Normal'] & Guldar['Rendah'] & Koles['Tinggi'] & BMI['Kurus'] & Riwa['Ada'], Hasil['Sedang'])
            Rb68 = ctrl.Rule(Tekdar['Normal'] & Guldar['Rendah'] & Koles['Tinggi'] & BMI['Kurus'] & Riwa['Tidak'], Hasil['Kecil'])
            Rb69 = ctrl.Rule(Tekdar['Normal'] & Guldar['Rendah'] & Koles['Tinggi'] & BMI['Normal'] & Riwa['Ada'], Hasil['Sedang'])
            Rb70 = ctrl.Rule(Tekdar['Normal'] & Guldar['Rendah'] & Koles['Tinggi'] & BMI['Normal'] & Riwa['Tidak'], Hasil['Kecil'])
            Rb71 = ctrl.Rule(Tekdar['Normal'] & Guldar['Rendah'] & Koles['Tinggi'] & BMI['Obesitas'] & Riwa['Ada'], Hasil['Besar'])
            Rb72 = ctrl.Rule(Tekdar['Normal'] & Guldar['Rendah'] & Koles['Tinggi'] & BMI['Obesitas'] & Riwa['Tidak'], Hasil['Sedang'])
            Rb73 = ctrl.Rule(Tekdar['Normal'] & Guldar['Normal'] & Koles['Rendah'] & BMI['Kurus'] & Riwa['Ada'], Hasil['Kecil'])
            Rb74 = ctrl.Rule(Tekdar['Normal'] & Guldar['Normal'] & Koles['Rendah'] & BMI['Kurus'] & Riwa['Tidak'], Hasil['Kecil'])
            Rb75 = ctrl.Rule(Tekdar['Normal'] & Guldar['Normal'] & Koles['Rendah'] & BMI['Normal'] & Riwa['Ada'], Hasil['Kecil'])
            Rb76 = ctrl.Rule(Tekdar['Normal'] & Guldar['Normal'] & Koles['Rendah'] & BMI['Normal'] & Riwa['Tidak'], Hasil['Kecil'])
            Rb77 = ctrl.Rule(Tekdar['Normal'] & Guldar['Normal'] & Koles['Rendah'] & BMI['Obesitas'] & Riwa['Ada'], Hasil['Sedang'])
            Rb78 = ctrl.Rule(Tekdar['Normal'] & Guldar['Normal'] & Koles['Rendah'] & BMI['Obesitas'] & Riwa['Tidak'], Hasil['Kecil'])
            Rb79 = ctrl.Rule(Tekdar['Normal'] & Guldar['Normal'] & Koles['Normal'] & BMI['Kurus'] & Riwa['Ada'], Hasil['Kecil'])
            Rb80 = ctrl.Rule(Tekdar['Normal'] & Guldar['Normal'] & Koles['Normal'] & BMI['Kurus'] & Riwa['Tidak'], Hasil['Kecil'])
            Rb81 = ctrl.Rule(Tekdar['Normal'] & Guldar['Normal'] & Koles['Normal'] & BMI['Normal'] & Riwa['Ada'], Hasil['Kecil'])
            Rb82 = ctrl.Rule(Tekdar['Normal'] & Guldar['Normal'] & Koles['Normal'] & BMI['Normal'] & Riwa['Tidak'], Hasil['Kecil'])
            Rb83 = ctrl.Rule(Tekdar['Normal'] & Guldar['Normal'] & Koles['Normal'] & BMI['Obesitas'] & Riwa['Ada'], Hasil['Sedang'])
            Rb84 = ctrl.Rule(Tekdar['Normal'] & Guldar['Normal'] & Koles['Normal'] & BMI['Obesitas'] & Riwa['Tidak'], Hasil['Kecil'])
            Rb85 = ctrl.Rule(Tekdar['Normal'] & Guldar['Normal'] & Koles['Tinggi'] & BMI['Kurus'] & Riwa['Ada'], Hasil['Sedang'])
            Rb86 = ctrl.Rule(Tekdar['Normal'] & Guldar['Normal'] & Koles['Tinggi'] & BMI['Kurus'] & Riwa['Tidak'], Hasil['Kecil'])
            Rb87 = ctrl.Rule(Tekdar['Normal'] & Guldar['Normal'] & Koles['Tinggi'] & BMI['Normal'] & Riwa['Ada'], Hasil['Sedang'])
            Rb88 = ctrl.Rule(Tekdar['Normal'] & Guldar['Normal'] & Koles['Tinggi'] & BMI['Normal'] & Riwa['Tidak'], Hasil['Kecil'])
            Rb89 = ctrl.Rule(Tekdar['Normal'] & Guldar['Normal'] & Koles['Tinggi'] & BMI['Obesitas'] & Riwa['Ada'], Hasil['Besar'])
            Rb90 = ctrl.Rule(Tekdar['Normal'] & Guldar['Normal'] & Koles['Tinggi'] & BMI['Obesitas'] & Riwa['Tidak'], Hasil['Sedang'])
            Rb91 = ctrl.Rule(Tekdar['Normal'] & Guldar['Tinggi'] & Koles['Rendah'] & BMI['Kurus'] & Riwa['Ada'], Hasil['Sedang'])
            Rb92 = ctrl.Rule(Tekdar['Normal'] & Guldar['Tinggi'] & Koles['Rendah'] & BMI['Kurus'] & Riwa['Tidak'], Hasil['Kecil'])
            Rb93 = ctrl.Rule(Tekdar['Normal'] & Guldar['Tinggi'] & Koles['Rendah'] & BMI['Normal'] & Riwa['Ada'], Hasil['Sedang'])
            Rb94 = ctrl.Rule(Tekdar['Normal'] & Guldar['Tinggi'] & Koles['Rendah'] & BMI['Normal'] & Riwa['Tidak'], Hasil['Kecil'])
            Rb95 = ctrl.Rule(Tekdar['Normal'] & Guldar['Tinggi'] & Koles['Rendah'] & BMI['Obesitas'] & Riwa['Ada'], Hasil['Besar'])
            Rb96 = ctrl.Rule(Tekdar['Normal'] & Guldar['Tinggi'] & Koles['Rendah'] & BMI['Obesitas'] & Riwa['Tidak'], Hasil['Sedang'])
            Rb97 = ctrl.Rule(Tekdar['Normal'] & Guldar['Tinggi'] & Koles['Normal'] & BMI['Kurus'] & Riwa['Ada'], Hasil['Sedang'])
            Rb98 = ctrl.Rule(Tekdar['Normal'] & Guldar['Tinggi'] & Koles['Normal'] & BMI['Kurus'] & Riwa['Tidak'], Hasil['Kecil'])
            Rb99 = ctrl.Rule(Tekdar['Normal'] & Guldar['Tinggi'] & Koles['Normal'] & BMI['Normal'] & Riwa['Ada'], Hasil['Sedang'])
            Rb100 = ctrl.Rule(Tekdar['Normal'] & Guldar['Tinggi'] & Koles['Normal'] & BMI['Normal'] & Riwa['Tidak'], Hasil['Kecil'])
            Rb101 = ctrl.Rule(Tekdar['Normal'] & Guldar['Tinggi'] & Koles['Normal'] & BMI['Obesitas'] & Riwa['Ada'], Hasil['Besar'])
            Rb102 = ctrl.Rule(Tekdar['Normal'] & Guldar['Tinggi'] & Koles['Normal'] & BMI['Obesitas'] & Riwa['Tidak'], Hasil['Sedang'])
            Rb103 = ctrl.Rule(Tekdar['Normal'] & Guldar['Tinggi'] & Koles['Tinggi'] & BMI['Kurus'] & Riwa['Ada'], Hasil['Besar'])
            Rb104 = ctrl.Rule(Tekdar['Normal'] & Guldar['Tinggi'] & Koles['Tinggi'] & BMI['Kurus'] & Riwa['Tidak'], Hasil['Sedang'])
            Rb105 = ctrl.Rule(Tekdar['Normal'] & Guldar['Tinggi'] & Koles['Tinggi'] & BMI['Normal'] & Riwa['Ada'], Hasil['Besar'])
            Rb106 = ctrl.Rule(Tekdar['Normal'] & Guldar['Tinggi'] & Koles['Tinggi'] & BMI['Normal'] & Riwa['Tidak'], Hasil['Sedang'])
            Rb107 = ctrl.Rule(Tekdar['Normal'] & Guldar['Tinggi'] & Koles['Tinggi'] & BMI['Obesitas'] & Riwa['Ada'], Hasil['Besar'])
            Rb108 = ctrl.Rule(Tekdar['Normal'] & Guldar['Tinggi'] & Koles['Tinggi'] & BMI['Obesitas'] & Riwa['Tidak'], Hasil['Besar'])
            Rb109 = ctrl.Rule(Tekdar['Tinggi'] & Guldar['Rendah'] & Koles['Rendah'] & BMI['Kurus'] & Riwa['Ada'], Hasil['Sedang'])
            Rb110 = ctrl.Rule(Tekdar['Tinggi'] & Guldar['Rendah'] & Koles['Rendah'] & BMI['Kurus'] & Riwa['Tidak'], Hasil['Kecil'])
            Rb111 = ctrl.Rule(Tekdar['Tinggi'] & Guldar['Rendah'] & Koles['Rendah'] & BMI['Normal'] & Riwa['Ada'], Hasil['Sedang'])
            Rb112 = ctrl.Rule(Tekdar['Tinggi'] & Guldar['Rendah'] & Koles['Rendah'] & BMI['Normal'] & Riwa['Tidak'], Hasil['Kecil'])
            Rb113 = ctrl.Rule(Tekdar['Tinggi'] & Guldar['Rendah'] & Koles['Rendah'] & BMI['Obesitas'] & Riwa['Ada'], Hasil['Besar'])
            Rb114 = ctrl.Rule(Tekdar['Tinggi'] & Guldar['Rendah'] & Koles['Rendah'] & BMI['Obesitas'] & Riwa['Tidak'], Hasil['Sedang'])
            Rb115 = ctrl.Rule(Tekdar['Tinggi'] & Guldar['Rendah'] & Koles['Normal'] & BMI['Kurus'] & Riwa['Ada'], Hasil['Sedang'])
            Rb116 = ctrl.Rule(Tekdar['Tinggi'] & Guldar['Rendah'] & Koles['Normal'] & BMI['Kurus'] & Riwa['Tidak'], Hasil['Kecil'])
            Rb117 = ctrl.Rule(Tekdar['Tinggi'] & Guldar['Rendah'] & Koles['Normal'] & BMI['Normal'] & Riwa['Ada'], Hasil['Sedang'])
            Rb118 = ctrl.Rule(Tekdar['Tinggi'] & Guldar['Rendah'] & Koles['Normal'] & BMI['Normal'] & Riwa['Tidak'], Hasil['Kecil'])
            Rb119 = ctrl.Rule(Tekdar['Tinggi'] & Guldar['Rendah'] & Koles['Normal'] & BMI['Obesitas'] & Riwa['Ada'], Hasil['Besar'])
            Rb120 = ctrl.Rule(Tekdar['Tinggi'] & Guldar['Rendah'] & Koles['Normal'] & BMI['Obesitas'] & Riwa['Tidak'], Hasil['Sedang'])
            Rb121 = ctrl.Rule(Tekdar['Tinggi'] & Guldar['Rendah'] & Koles['Tinggi'] & BMI['Kurus'] & Riwa['Ada'], Hasil['Besar'])
            Rb122 = ctrl.Rule(Tekdar['Tinggi'] & Guldar['Rendah'] & Koles['Tinggi'] & BMI['Kurus'] & Riwa['Tidak'], Hasil['Sedang'])
            Rb123 = ctrl.Rule(Tekdar['Tinggi'] & Guldar['Rendah'] & Koles['Tinggi'] & BMI['Normal'] & Riwa['Ada'], Hasil['Besar'])
            Rb124 = ctrl.Rule(Tekdar['Tinggi'] & Guldar['Rendah'] & Koles['Tinggi'] & BMI['Normal'] & Riwa['Tidak'], Hasil['Sedang'])
            Rb125 = ctrl.Rule(Tekdar['Tinggi'] & Guldar['Rendah'] & Koles['Tinggi'] & BMI['Obesitas'] & Riwa['Ada'], Hasil['Besar'])
            Rb126 = ctrl.Rule(Tekdar['Tinggi'] & Guldar['Rendah'] & Koles['Tinggi'] & BMI['Obesitas'] & Riwa['Tidak'], Hasil['Besar'])
            Rb127 = ctrl.Rule(Tekdar['Tinggi'] & Guldar['Normal'] & Koles['Rendah'] & BMI['Kurus'] & Riwa['Ada'], Hasil['Sedang'])
            Rb128 = ctrl.Rule(Tekdar['Tinggi'] & Guldar['Normal'] & Koles['Rendah'] & BMI['Kurus'] & Riwa['Tidak'], Hasil['Kecil'])
            Rb129 = ctrl.Rule(Tekdar['Tinggi'] & Guldar['Normal'] & Koles['Rendah'] & BMI['Normal'] & Riwa['Ada'], Hasil['Sedang'])
            Rb130 = ctrl.Rule(Tekdar['Tinggi'] & Guldar['Normal'] & Koles['Rendah'] & BMI['Normal'] & Riwa['Tidak'], Hasil['Kecil'])
            Rb131 = ctrl.Rule(Tekdar['Tinggi'] & Guldar['Normal'] & Koles['Rendah'] & BMI['Obesitas'] & Riwa['Ada'], Hasil['Besar'])
            Rb132 = ctrl.Rule(Tekdar['Tinggi'] & Guldar['Normal'] & Koles['Rendah'] & BMI['Obesitas'] & Riwa['Tidak'], Hasil['Sedang'])
            Rb133 = ctrl.Rule(Tekdar['Tinggi'] & Guldar['Normal'] & Koles['Normal'] & BMI['Kurus'] & Riwa['Ada'], Hasil['Sedang'])
            Rb134 = ctrl.Rule(Tekdar['Tinggi'] & Guldar['Normal'] & Koles['Normal'] & BMI['Kurus'] & Riwa['Tidak'], Hasil['Kecil'])
            Rb135 = ctrl.Rule(Tekdar['Tinggi'] & Guldar['Normal'] & Koles['Normal'] & BMI['Normal'] & Riwa['Ada'], Hasil['Sedang'])
            Rb136 = ctrl.Rule(Tekdar['Tinggi'] & Guldar['Normal'] & Koles['Normal'] & BMI['Normal'] & Riwa['Tidak'], Hasil['Kecil'])
            Rb137 = ctrl.Rule(Tekdar['Tinggi'] & Guldar['Normal'] & Koles['Normal'] & BMI['Obesitas'] & Riwa['Ada'], Hasil['Besar'])
            Rb138 = ctrl.Rule(Tekdar['Tinggi'] & Guldar['Normal'] & Koles['Normal'] & BMI['Obesitas'] & Riwa['Tidak'], Hasil['Sedang'])
            Rb139 = ctrl.Rule(Tekdar['Tinggi'] & Guldar['Normal'] & Koles['Tinggi'] & BMI['Kurus'] & Riwa['Ada'], Hasil['Besar'])
            Rb140 = ctrl.Rule(Tekdar['Tinggi'] & Guldar['Normal'] & Koles['Tinggi'] & BMI['Kurus'] & Riwa['Tidak'], Hasil['Sedang'])
            Rb141 = ctrl.Rule(Tekdar['Tinggi'] & Guldar['Normal'] & Koles['Tinggi'] & BMI['Normal'] & Riwa['Ada'], Hasil['Besar'])
            Rb142 = ctrl.Rule(Tekdar['Tinggi'] & Guldar['Normal'] & Koles['Tinggi'] & BMI['Normal'] & Riwa['Tidak'], Hasil['Sedang'])
            Rb143 = ctrl.Rule(Tekdar['Tinggi'] & Guldar['Normal'] & Koles['Tinggi'] & BMI['Obesitas'] & Riwa['Ada'], Hasil['Besar'])
            Rb144 = ctrl.Rule(Tekdar['Tinggi'] & Guldar['Normal'] & Koles['Tinggi'] & BMI['Obesitas'] & Riwa['Tidak'], Hasil['Besar'])
            Rb145 = ctrl.Rule(Tekdar['Tinggi'] & Guldar['Tinggi'] & Koles['Rendah'] & BMI['Kurus'] & Riwa['Ada'], Hasil['Besar'])
            Rb146 = ctrl.Rule(Tekdar['Tinggi'] & Guldar['Tinggi'] & Koles['Rendah'] & BMI['Kurus'] & Riwa['Tidak'], Hasil['Sedang'])
            Rb147 = ctrl.Rule(Tekdar['Tinggi'] & Guldar['Tinggi'] & Koles['Rendah'] & BMI['Normal'] & Riwa['Ada'], Hasil['Besar'])
            Rb148 = ctrl.Rule(Tekdar['Tinggi'] & Guldar['Tinggi'] & Koles['Rendah'] & BMI['Normal'] & Riwa['Tidak'], Hasil['Sedang'])
            Rb149 = ctrl.Rule(Tekdar['Tinggi'] & Guldar['Tinggi'] & Koles['Rendah'] & BMI['Obesitas'] & Riwa['Ada'], Hasil['Besar'])
            Rb150 = ctrl.Rule(Tekdar['Tinggi'] & Guldar['Tinggi'] & Koles['Rendah'] & BMI['Obesitas'] & Riwa['Tidak'], Hasil['Besar'])
            Rb151 = ctrl.Rule(Tekdar['Tinggi'] & Guldar['Tinggi'] & Koles['Normal'] & BMI['Kurus'] & Riwa['Ada'], Hasil['Besar'])
            Rb152 = ctrl.Rule(Tekdar['Tinggi'] & Guldar['Tinggi'] & Koles['Normal'] & BMI['Kurus'] & Riwa['Tidak'], Hasil['Sedang'])
            Rb153 = ctrl.Rule(Tekdar['Tinggi'] & Guldar['Tinggi'] & Koles['Normal'] & BMI['Normal'] & Riwa['Ada'], Hasil['Besar'])
            Rb154 = ctrl.Rule(Tekdar['Tinggi'] & Guldar['Tinggi'] & Koles['Normal'] & BMI['Normal'] & Riwa['Tidak'], Hasil['Sedang'])
            Rb155 = ctrl.Rule(Tekdar['Tinggi'] & Guldar['Tinggi'] & Koles['Normal'] & BMI['Obesitas'] & Riwa['Ada'], Hasil['Besar'])
            Rb156 = ctrl.Rule(Tekdar['Tinggi'] & Guldar['Tinggi'] & Koles['Normal'] & BMI['Obesitas'] & Riwa['Tidak'], Hasil['Besar'])
            Rb157 = ctrl.Rule(Tekdar['Tinggi'] & Guldar['Tinggi'] & Koles['Tinggi'] & BMI['Kurus'] & Riwa['Ada'], Hasil['Besar'])
            Rb158 = ctrl.Rule(Tekdar['Tinggi'] & Guldar['Tinggi'] & Koles['Tinggi'] & BMI['Kurus'] & Riwa['Tidak'], Hasil['Besar'])
            Rb159 = ctrl.Rule(Tekdar['Tinggi'] & Guldar['Tinggi'] & Koles['Tinggi'] & BMI['Normal'] & Riwa['Ada'], Hasil['Besar'])
            Rb160 = ctrl.Rule(Tekdar['Tinggi'] & Guldar['Tinggi'] & Koles['Tinggi'] & BMI['Normal'] & Riwa['Tidak'], Hasil['Besar'])
            Rb161 = ctrl.Rule(Tekdar['Tinggi'] & Guldar['Tinggi'] & Koles['Tinggi'] & BMI['Obesitas'] & Riwa['Ada'], Hasil['Besar'])
            Rb162 = ctrl.Rule(Tekdar['Tinggi'] & Guldar['Tinggi'] & Koles['Tinggi'] & BMI['Obesitas'] & Riwa['Tidak'], Hasil['Besar'])

            HS1 = ctrl.ControlSystem([Rb1,Rb2,Rb3,Rb4,Rb5,Rb6,Rb7,Rb8,Rb9,Rb10,Rb11,Rb12,Rb13,Rb14,Rb15,Rb16,Rb17,Rb18,Rb19,Rb20,
            Rb21,Rb22,Rb23,Rb24,Rb25,Rb26,Rb27,Rb28,Rb29,Rb30,Rb31,Rb32,Rb33,Rb34,Rb35,Rb36,Rb37,Rb38,Rb39,Rb40,
            Rb41,Rb42,Rb43,Rb44,Rb45,Rb46,Rb47,Rb48,Rb49,Rb50,Rb51,Rb52,Rb53,Rb54,Rb55,Rb56,Rb57,Rb58,Rb59,Rb60,
            Rb61,Rb62,Rb63,Rb64,Rb65,Rb66,Rb67,Rb68,Rb69,Rb70,Rb71,Rb72,Rb73,Rb74,Rb75,Rb76,Rb77,Rb78,Rb79,Rb80,
            Rb81,Rb82,Rb83,Rb84,Rb85,Rb86,Rb87,Rb88,Rb89,Rb90,Rb91,Rb92,Rb93,Rb94,Rb95,Rb96,Rb97,Rb98,Rb99,Rb100,
            Rb101,Rb102,Rb103,Rb104,Rb105,Rb106,Rb107,Rb108,Rb109,Rb110,Rb111,Rb112,Rb113,Rb114,Rb115,Rb116,Rb117,Rb118,Rb119,Rb120,
            Rb121,Rb122,Rb123,Rb124,Rb125,Rb126,Rb127,Rb128,Rb129,Rb130,Rb131,Rb132,Rb133,Rb134,Rb135,Rb136,Rb137,Rb138,Rb139,Rb140,
            Rb141,Rb142,Rb143,Rb144,Rb145,Rb146,Rb147,Rb148,Rb149,Rb150,Rb151,Rb152,Rb153,Rb154,Rb155,Rb156,Rb157,Rb158,Rb159,Rb160,Rb161,Rb162])
            HS2 = ctrl.ControlSystemSimulation(HS1)

            TD = request.form['tekanan-darah']
            GD = request.form['gula-darah']
            KL = request.form['kolesterol']
            BM = request.form['bmi']
            RW = request.form['riwayat']

            HS2.input['Tekanan Darah'] = float(TD)
            HS2.input['Gula Darah'] = float(GD)
            HS2.input['Kolesterol'] = float(KL)
            HS2.input['Body Mass Index'] = float(BM)
            HS2.input['Riwayat'] = float(RW)
            try:
                HS2.compute()

                OP = ''
                ox = HS2.output['Hasil']
                
                if ox <= 4:
                    OP = 'Kecil'
                elif ox <= 7:
                    OP = 'Sedang'
                else:
                    OP = 'Besar'
                    
                today = datetime.now()
                dt_string = today.strftime("%d/%m/%Y %H:%M:%S")
                df = pd.DataFrame({
                    'Waktu' : [dt_string], 
                    'Tekanan Darah':[TD], 
                    'Gula Darah':[GD], 
                    'Kolesterol' :[KL], 
                    'Body Mass Index' :[BM], 
                    'Riwayat' :[RW], 
                    'Hasil' :[ox], 
                    'Status' :[OP]
                    })
                df = pd.read_csv("Hasil.csv")

                df1 = pd.DataFrame({
                    'Waktu' : [dt_string], 
                    'Tekanan Darah':[TD], 
                    'Gula Darah':[GD], 
                    'Kolesterol' :[KL], 
                    'Body Mass Index' :[BM], 
                    'Riwayat' :[RW], 
                    'Hasil' :[ox], 
                    'Status' :[OP]
                    })

                out = df.append(df1)
                out = out.dropna()
                out = out.reset_index(drop=True)
                out = out.sort_index(axis=0,ascending = False)
                out.to_csv('Hasil.csv', index=False)
                return render_template('utama.html', data = [out.to_html(justify='left', classes="table table-striped table-bordered table-hover table-sm table-responsive tables")])
            except:
                flash('Inputan Error')
                dffe = pd.read_csv("Hasil.csv")
                return render_template('utama.html', data = [dffe.to_html(justify='left', classes="table table-striped table-bordered table-hover table-sm table-responsive tables")])
            
            
    else:
        dff = pd.read_csv("Hasil.csv")
        return render_template('utama.html', data = [dff.to_html(justify='left', classes="table table-striped table-bordered table-hover table-sm table-responsive tables")])
    


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5001, debug=True)