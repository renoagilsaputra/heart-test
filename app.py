from flask import Flask, request, render_template_string, Response, redirect, url_for, render_template, flash
import skfuzzy as fz
from skfuzzy import control as ctrl
import numpy as np
from config import *
from flask import Markup
import pandas as pd

app = Flask(__name__)

@app.route('/')
def main():
    return'<h1>Hello!</h1>' 