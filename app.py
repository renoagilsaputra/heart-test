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
            Rb1 = ctrl.Rule(Tekdar['Normal'] & Guldar['Normal'] & Koles['Normal'] & BMI['Obesitas'] & Riwa['Ada'], Hasil['Sedang'])
            Rb2 = ctrl.Rule(Tekdar['Normal'] & Guldar['Normal'] & Koles['Rendah'] & BMI['Obesitas'] & Riwa['Ada'], Hasil['Sedang'])
            Rb3 = ctrl.Rule(Tekdar['Normal'] & Guldar['Rendah'] & Koles['Normal'] & BMI['Obesitas'] & Riwa['Ada'], Hasil['Sedang'])
            Rb4 = ctrl.Rule(Tekdar['Normal'] & Guldar['Rendah'] & Koles['Rendah'] & BMI['Obesitas'] & Riwa['Ada'], Hasil['Sedang'])
            Rb5 = ctrl.Rule(Tekdar['Tinggi'] & Guldar['Normal'] & Koles['Normal'] & BMI['Obesitas'] & Riwa['Ada'], Hasil['Besar'])
            Rb6 = ctrl.Rule(Tekdar['Tinggi'] & Guldar['Normal'] & Koles['Rendah'] & BMI['Obesitas'] & Riwa['Ada'], Hasil['Besar'])
            Rb7 = ctrl.Rule(Tekdar['Tinggi'] & Guldar['Rendah'] & Koles['Normal'] & BMI['Obesitas'] & Riwa['Ada'], Hasil['Besar'])
            Rb8 = ctrl.Rule(Tekdar['Tinggi'] & Guldar['Rendah'] & Koles['Rendah'] & BMI['Obesitas'] & Riwa['Ada'], Hasil['Besar'])

            HS1 = ctrl.ControlSystem([Rb1,Rb2,Rb3,Rb4,Rb5,Rb6,Rb7,Rb8])
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
                elif ox <= 9:
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